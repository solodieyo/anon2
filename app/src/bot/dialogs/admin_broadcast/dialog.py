from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, ScrollingGroup, Select, Back, Url, Row
from aiogram_dialog.widgets.text import Const, Format, Case

from app.src.bot.dialogs.admin_broadcast.getters import getter_mailing_info
from app.src.bot.dialogs.admin_broadcast.handlers import (
    on_input_album,
    on_input_message,
    choice_mailing_group,
    cancel_mailing,
    show_mailing_content,
    show_previous_mailing,
    start_broadcast,
    on_faker_click,
    show_previous_mailing_content
)
from app.src.bot.dialogs.admin_dialog.getters import (
    getter_previous_mailing,
    get_broadcast_content,
    getter_previous_mailing_content, get_mailing_group
)
from app.src.bot.dialogs.common.widgets import ADMIN_MENU_BUTTON, I18NFormat, BROADCAST_BACK_BUTTON
from app.src.bot.states.dialog_states import BroadcastStates

broadcast_menu = Window(
    Const('Рассылка',
          when=F['active_mailing'].is_(False)
          ),
    I18NFormat(
        'broadcast-text',
        when=F['active_mailing'].is_(True)
    ),
    Button(
        text=Const('Отменить рассылку'),
        id='cancel_mailing',
        on_click=cancel_mailing,
        when=F['active_mailing'].is_(True)
    ),
    SwitchTo(
        text=Const('✉️ Создать рассылку'),
        id='start_mailing',
        when=F['active_mailing'].is_(False),
        state=BroadcastStates.input_message
    ),
    SwitchTo(
        text=Const('📅 История рассылок'),
        id='previous_mailing',
        state=BroadcastStates.previous_mailing
    ),
    Button(
        text=Const('Содержание рассылки'),
        id='show_mailing_content',
        on_click=show_mailing_content,
        when=F['active_mailing'].is_(True)
    ),
    Url(
        text=Const('Поделиться рассылкой'),
        url=Format("{link}"),
        when=F['active_mailing'].is_(True)
    ),
    ADMIN_MENU_BUTTON,
    state=BroadcastStates.main_menu,
    getter=getter_mailing_info
)

input_message_to_broadcast = Window(
    Const('Отправьте сообщение для рассылки'),
    MessageInput(
        func=on_input_album,
        filter=F.media_group_id
    ),
    MessageInput(
        func=on_input_message
    ),
    BROADCAST_BACK_BUTTON,
    state=BroadcastStates.input_message
)

previous_mailing = Window(
    Const('Прошлые рассылки'),
    ScrollingGroup(
        Select(
            text=Format("🔸 {item}"),
            id='previous_mailing',
            items='mailings',
            item_id_getter=lambda x: x,
            on_click=show_previous_mailing
        ),
        id='messages_scroll',
        width=1,
        height=5,
        hide_on_single_page=True
    ),
    BROADCAST_BACK_BUTTON,
    state=BroadcastStates.previous_mailing,
    getter=getter_previous_mailing
)


show_previous_mailing_window = Window(
    I18NFormat('broadcast-text'),
    Button(
        text=Const('Содержимое рассылки'),
        id='mailing_content',
        on_click=show_previous_mailing_content,
    ),
    Url(
        text=Const('Поделиться рассылкой'),
        url=Format("{link}"),
    ),
    Back(
        text=Const('👈 Назад')
    ),
    state=BroadcastStates.show_previus_mailing_content,
    getter=getter_previous_mailing_content
)

confirm_broadcast = Window(
    Format('{text}'),
    Row(
        SwitchTo(
            text=Case(
                {
                    'premium': Const('👤 Кому: Премиум'),
                    'default': Const('👤 Кому: Обычным'),
                    'all': Const('👤 Кому: Всем')
                },
                selector="mail_group"
            ),
            id='type_maling_button',
            state=BroadcastStates.users_type
        ),
        Button(
            text=Case(
                {
                    True: Const('💬 Готова'),
                    False: Const('💬 Не готова')
                },
                selector="faker"
            ),
            id='faker_switch',
            on_click=on_faker_click
        )
    ),
    Button(
        text=Const('✅ Начать рассылку'),
        id='start_broadcast',
        on_click=start_broadcast
    ),
    Back(I18NFormat('back')),
    state=BroadcastStates.confirm_start,
    getter=get_broadcast_content
)


users_type = Window(
    Const('👥 <b>Выберите, кому вы хотите отправить сообщение:</b>'),
    Button(
        text=Case(
            {
                'default': Const('🔸 Обычным пользователям'),
                ...: Const('Обычным пользователям'),
            },
            selector="mail_group"
        ),
        id='default',
        on_click=choice_mailing_group,
    ),
    Button(
        text=Case(
            {
                'premium': Const('🔸 Премиум пользователям'),
                ...: Const('Премиум пользователям'),
            },
            selector="mail_group"
        ),
        id='premium',
        on_click=choice_mailing_group,
    ),
    Button(
        text=Case(
            {
                'all': Const('🔸 Всем'),
                ...: Const('Всем'),
            },
            selector="mail_group"
        )
        ,
        id='all',
        on_click=choice_mailing_group,
    ),
    SwitchTo(
        text=Const('👈 Назад'),
        state=BroadcastStates.confirm_start,
        id='__back_broadcust___'
    ),
    state=BroadcastStates.users_type,
    getter=get_mailing_group
)

mailing_dialog = Dialog(
    users_type,
    broadcast_menu,
    input_message_to_broadcast,
    confirm_broadcast,
    previous_mailing,
    show_previous_mailing_window,
)
