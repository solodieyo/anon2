from datetime import date
from typing import Any, Dict, Protocol

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Start, SwitchTo
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarDaysView,
    CalendarScopeView,
    CalendarScope,
    DATE_TEXT,
    TODAY_TEXT,
    Calendar,
    CalendarMonthView,
    CalendarYearsView
)
from aiogram_dialog.widgets.text import Text, Format, Const
from babel.dates import get_month_names, get_day_names

from app.src.bot.dialogs.factory.callback import SenderCallbackData, GetterCallbackData, AdminDayStatistic
from app.src.bot.states.dialog_states import (
    MainMenuStates,
    AdminStates,
    StatisticStates,
    AdminUsersStates,
    AdminSettingsStates,
    ProfileStates, BroadcastStates,
)
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.models_dto.message_dto import MessageDTO

SELECTED_DAYS_KEY = "selected_dates"


class Values(Protocol):

    def __getitem__(self, item: Any) -> Any:
        raise NotImplementedError


def default_format_text(text: str, data: Values) -> str:
    return text.format_map(data)


class I18NFormat(Text):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when)
        self.text = text

    async def _render_text(self, data: Dict, dialog_manager: DialogManager) -> str:
        format_text = dialog_manager.middleware_data.get(
            "i18n", default_format_text,
        )
        return format_text(self.text, **data)


class WeekDay(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.middleware_data['user'].locale
        return get_day_names(
            width="short", context='stand-alone', locale=locale,
        )[selected_date.weekday()].title()


class MarkedDay(Text):
    def __init__(self, mark: str, other: Text):
        super().__init__()
        self.mark = mark
        self.other = other

    async def _render_text(self, data, manager: DialogManager) -> str:
        current_date: date = data["date"]
        serial_date = current_date.isoformat()
        selected = manager.dialog_data.get(SELECTED_DAYS_KEY, [])
        if serial_date in selected:
            return self.mark
        return await self.other.render_text(data, manager)


class Month(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.middleware_data['user'].locale
        return get_month_names(
            'wide', context='stand-alone', locale=locale,
        )[selected_date.month].title()


class CustomCalendar(Calendar):
    def _init_views(self) -> Dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: CalendarDaysView(
                self._item_callback_data,
                date_text=MarkedDay("🔴", DATE_TEXT),
                today_text=MarkedDay("⭕", TODAY_TEXT),
                header_text="~~~~~ " + Month() + " ~~~~~",
                weekday_text=WeekDay(),
                next_month_text=Month() + " >>",
                prev_month_text="<< " + Month(),
            ),
            CalendarScope.MONTHS: CalendarMonthView(
                self._item_callback_data,
                month_text=Month(),
                header_text="~~~~~ " + Format("{date:%Y}") + " ~~~~~",
                this_month_text="[" + Month() + "]",
            ),
            CalendarScope.YEARS: CalendarYearsView(
                self._item_callback_data,
            ),
        }


def get_message_keyboard(message: MessageDTO):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отправитель",
                callback_data=SenderCallbackData(
                    user_id=message.from_user.user_id
                ).pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="Получатель",
                callback_data=GetterCallbackData(
                    user_id=message.to_user.user_id
                ).pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ Закрыть",
                callback_data='delete_message'
            ),
        ],
    ])

    return keyboard


def get_admin_day_keyboard(
        date_num: str,
        now_state: str
):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🔸 🏛 ОБЩАЯ' if now_state == 'common_statistic' else '🏛 ОБЩАЯ',
                    callback_data=AdminDayStatistic(
                        date_num=date_num,
                        now_state='common_statistic'
                    ).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text='🔸 🇺🇳 ЯЗЫКИ' if now_state == 'languages_statistic' else '🇺🇳 ЯЗЫКИ',
                    callback_data=AdminDayStatistic(
                        date_num=date_num,
                        now_state='languages_statistic'
                    ).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text='🔸 💳 ПОПОЛНЕНИЯ' if now_state == 'payments_statistic' else '💳 ПОПОЛНЕНИЯ',
                    callback_data=AdminDayStatistic(
                        date_num=date_num,
                        now_state='payments_statistic'
                    ).pack()
                )
            ]
        ]
    )

    return keyboard


DELETE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="❌ Закрыть",
                callback_data='delete_message'
            ),
        ],
    ])


def get_broadcast_keyboard(url: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                url=url,
                text='Поделиться рассылкой'
            )],
            [InlineKeyboardButton(
                text="❌ Закрыть",
                callback_data='delete_message'
            )],
        ]
    )
    return keyboard


USER_BACK_TO_PROFILE = Start(
    text=I18NFormat('back'),
    id="__user_profile__",
    state=ProfileStates.main_menu,
    mode=StartMode.RESET_STACK
)

USER_PROFILE_SETTINGS_BACK_BUTTON = Start(
    text=I18NFormat('back'),
    id="__user_settings__",
    state=ProfileStates.settings,
    mode=StartMode.RESET_STACK
)
MAIN_MENU_BUTTON = Start(
    text=I18NFormat('to-menu'),
    id='__main__',
    state=MainMenuStates.main_menu,
    mode=StartMode.RESET_STACK
)

BROADCAST_BACK_BUTTON = Start(
    text=Const('👈 Назад'),
    id="__broadcast__",
    state=BroadcastStates.main_menu,
    mode=StartMode.RESET_STACK
)

ADMIN_MENU_BUTTON = Start(
    text=Const('В меню'),
    id='__admin__',
    state=AdminStates.main_menu,
    mode=StartMode.RESET_STACK
)

STATISTIC_MENU_BUTTON = Start(
    text=I18NFormat('back'),
    id="__statistic__",
    state=StatisticStates.main_menu,
    mode=StartMode.RESET_STACK
)

SETTINGS_MENU_BUTTON = Start(
    text=Const('👈 Назад'),
    id="__settings__",
    state=AdminSettingsStates.main_menu,
    mode=StartMode.RESET_STACK
)

MANAGE_USER_BACK_BUTTON = SwitchTo(
    text=I18NFormat('back'),
    id="__manage_user__",
    state=AdminUsersStates.manage_user,
    show_mode=ShowMode.EDIT
)

USER_PROFILE_BACK_BUTTON = Start(
    text=I18NFormat('back'),
    id="__user_profile__",
    state=AdminUsersStates.main_menu,
    mode=StartMode.RESET_STACK
)
