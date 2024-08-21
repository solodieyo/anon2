from operator import itemgetter

from aiogram import F
from aiogram_dialog import Window, Dialog, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
	Row,
	SwitchTo,
	Button,
	Select,
	ScrollingGroup,
	Start,
	Cancel,
	PrevPage,
	NextPage,
	Url
)
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Case

from app.src.bot.dialogs.admin_dialog.getters import getter_message_content
from app.src.bot.dialogs.admin_dialog.handlers import on_receiver, on_sender
from app.src.bot.dialogs.admin_users_dialog.getters import (
	getter_admin_user_text,
	getter_user_info,
	getter_user_sent_messages,
	getter_user_received_messages
)
from app.src.bot.dialogs.admin_users_dialog.handlers import on_input_user_data, on_manage_premium, on_manage_role, \
	on_change_sort, on_select_message
from app.src.bot.dialogs.common.widgets import (
	I18NFormat,
	ADMIN_MENU_BUTTON,
	MANAGE_USER_BACK_BUTTON,
	USER_PROFILE_BACK_BUTTON
)
from app.src.bot.states.dialog_states import AdminUsersStates

admin_user_main_menu = Window(
	I18NFormat('admin-users-main-text'),
	MessageInput(
		func=on_input_user_data
	),
	ADMIN_MENU_BUTTON,
	state=AdminUsersStates.main_menu,
	getter=getter_admin_user_text
)

no_user_found = Window(
	Const('Пользователь не найден'),
	USER_PROFILE_BACK_BUTTON,
	state=AdminUsersStates.no_user_found,
)

manage_user = Window(
	Format('{text}'),
	Row(
		SwitchTo(
			text=Const('Подписка'),
			state=AdminUsersStates.premium_manage,
			id='give_premium'
		),
		SwitchTo(
			text=Const("Роль"),
			state=AdminUsersStates.give_role,
			id='give_role'
		)
	),
	Row(
		SwitchTo(
			text=Const('Отправленные сообщения'),
			state=AdminUsersStates.user_sent_messages,
			id='sent_messages'
		),
		SwitchTo(
			text=Const('Полученные сообщения'),
			state=AdminUsersStates.user_got_messages,
			id='got_messages'
		)
	),
	Url(
		text=Const('🔗 Ссылка на анонимку'),
		url=Format('{url_link}'),
	),
	Start(
		text=I18NFormat('back'),
		id="__user_profile__",
		state=AdminUsersStates.main_menu,
		mode=StartMode.RESET_STACK,
		when=F['cancel'].is_(False)
	),
	Cancel(
		text=I18NFormat('back'),
		when=F['cancel'].is_(True)
	),
	state=AdminUsersStates.manage_user,
	getter=getter_user_info,
	disable_web_page_preview=True
)

# select
user_premium = Window(
	Const("Управление премиум подпиской"),
	Button(
		text=Const("1 День"),
		id='premium_1',
		on_click=on_manage_premium
	),
	Button(
		text=Const("7 Дней"),
		id='premium_7',
		on_click=on_manage_premium
	),
	Button(
		text=Const("30 Дней"),
		id='premium_30',
		on_click=on_manage_premium
	),
	Button(
		text=Const("Навсегда"),
		id='premium_forever',
		on_click=on_manage_premium
	),
	Button(
		text=Const('Удалить премиум'),
		id='delete_premium',
		on_click=on_manage_premium
	),
	MANAGE_USER_BACK_BUTTON,
	state=AdminUsersStates.premium_manage,
)

role_manage = Window(
	Const("Управление ролью"),
	Button(
		text=Const("Админ"),
		id='admin',
		on_click=on_manage_role
	),
	Button(
		text=Const("Пользователь"),
		id='member',
		on_click=on_manage_role
	),
	MANAGE_USER_BACK_BUTTON,
	state=AdminUsersStates.give_role
)

user_sent_messages = Window(
	Const(text='Последние 100 отправленных сообщений'),
	Button(
		text=Case(
			{
				True: Const('📅 СОРТИРОВКА: 🔻 НОВЫЕ'),
				False: Const('📅 СОРТИРОВКА: 🔺 СТАРЫЕ'),
			},
			selector='sort_type'
		),
		id='change_sort',
		on_click=on_change_sort
	),
	ScrollingGroup(
		Select(
			text=Format("🔸 {item[1]} #{item[0]}"),
			id='messages_select',
			items='messages',
			item_id_getter=itemgetter(0),
			on_click=on_select_message,
			type_factory=int
		),
		id='messages_scroll_senders',
		width=1,
		height=8,
		hide_pager=True
	),
	Row(
		PrevPage(
			scroll="messages_scroll_senders", text=Format("👈 Назад"),
			when=F["pages"] > 1 & F["current_page1"] != 1
		),
		NextPage(
			scroll="messages_scroll_senders", text=Format("👉 Вперед"),
			when=F["current_page1"] != F["pages"]
		),
	),
	SwitchTo(
		text=Const('🔙 Вернутся'),
		id="__manage_user__",
		state=AdminUsersStates.manage_user,
		show_mode=ShowMode.EDIT
	),
	state=AdminUsersStates.user_sent_messages,
	getter=getter_user_sent_messages
)

user_received_messages = Window(
	Const(text='Последние 100 полученных сообщений'),
	Button(
		text=Case(
			{
				True: Const('📅 СОРТИРОВКА: 🔻 НОВЫЕ'),
				False: Const('📅 СОРТИРОВКА: 🔺 СТАРЫЕ'),
			},
			selector='sort_type'
		),
		id='change_sort',
		on_click=on_change_sort
	),
	ScrollingGroup(
		Select(
			text=Format("🔸 {item[1]} #{item[0]}"),
			id='messages_select',
			items='messages',
			item_id_getter=itemgetter(0),
			on_click=on_select_message,
			type_factory=int
		),
		id='messages_scroll',
		width=1,
		height=8,
		hide_pager=True
	),
	Row(
		PrevPage(
			scroll="messages_scroll", text=Format("👈 Назад"),
			when=F["pages"] > 1 & F["current_page1"] != 1
		),
		NextPage(
			scroll="messages_scroll", text=Format("👉 Вперед"),
			when=F["current_page1"] != F["pages"]
		),
	),
	SwitchTo(
		text=Const('🔙 Вернутся'),
		id="__manage_user__",
		state=AdminUsersStates.manage_user,
		show_mode=ShowMode.EDIT
	),
	state=AdminUsersStates.user_got_messages,
	getter=getter_user_received_messages
)

select_message = Window(
	DynamicMedia(
		selector='media',
		when=F['media']
	),
	Format('{text}'),
	Row(
		Button(
			text=Const('🗣 ОТПРАВИТЕЛЬ'),
			id='sender',
			on_click=on_sender
		),
		Button(
			text=Const('👤 ПОЛУЧАТЕЛЬ'),
			id='receiver',
			on_click=on_receiver
		)
	),
	SwitchTo(
		Const('👈 Назад'),
		state=AdminUsersStates.manage_user,
		id='back'
	),
	state=AdminUsersStates.show_message_content,
	getter=getter_message_content
)

admin_user_dialog = Dialog(
	admin_user_main_menu,
	no_user_found,
	manage_user,
	user_premium,
	role_manage,
	user_sent_messages,
	user_received_messages,
	select_message,

)
