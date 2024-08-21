from datetime import timedelta, datetime, UTC
from typing import Optional

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.bot.dialogs.common.trash import get_user
from app.src.bot.states.dialog_states import AdminUsersStates
from app.src.enums import Roles
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository
from app.src.infrastructure.scheduler.tasks import delete_subscribe

days = {
    'premium_1': 1,
    'premium_7': 7,
    'premium_30': 30
}


@inject
async def on_input_user_data(message: Message, widget: MessageInput, dialog_manager: DialogManager,
                             repository: FromDishka[GeneralRepository], **_):
    user: Optional[User] = await get_user(
        message=message,
        repository=repository
    )
    if user:
        dialog_manager.dialog_data['show_user'] = user.user_id
        await dialog_manager.switch_to(
            state=AdminUsersStates.manage_user,
            show_mode=ShowMode.DELETE_AND_SEND
        )
        return
    await dialog_manager.switch_to(state=AdminUsersStates.no_user_found)


@inject
async def on_manage_premium(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository],
):
    if widget.widget_id == "delete_premium":
        await repository.user.delete_premium(
            user_id=dialog_manager.dialog_data['show_user']
        )
        await callback.answer("Премиум удален")
        return

    redis_source = dialog_manager.middleware_data['redis_source']
    manage_premium = {
        'premium_forever': 'Установлен премиум навсегда',
        "premium_30": "Установлен премиум на 30 дней",
        'premium_1': "Установлен премиум на 1 день",
        'premium_7': "Установлен премиум на 7 дней"
    }

    if widget.widget_id == 'premium_forever':
        await repository.user.set_premium_forever(
            user_id=dialog_manager.dialog_data['show_user']
        )
    else:
        await repository.user.set_premium(
            user_id=dialog_manager.dialog_data['show_user'],
            count_days=days[widget.widget_id]
        )
        await delete_subscribe.schedule_by_time(
            redis_source,
            datetime.now(UTC) + timedelta(days=days[widget.widget_id]),
            user_id=dialog_manager.dialog_data['show_user']
        )
    await callback.answer(manage_premium[widget.widget_id])




@inject
async def on_manage_role(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository]
):
    roles = {
        "member": Roles.MEMBER,
        "admin": Roles.ADMIN
    }

    await repository.user.set_user_rank(
        user_id=dialog_manager.dialog_data['show_user'],
        rank=roles[widget.widget_id]
    )

    await dialog_manager.switch_to(state=AdminUsersStates.manage_user)


async def on_change_sort(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
):
    sort_type = dialog_manager.dialog_data.get("sort_type", True)
    dialog_manager.dialog_data["sort_type"] = not sort_type


async def on_select_message(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        selected_item: int
):
    dialog_manager.dialog_data["message_id"] = selected_item
    await dialog_manager.switch_to(AdminUsersStates.show_message_content)
