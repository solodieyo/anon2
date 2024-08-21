from operator import itemgetter

from aiogram import F
from aiogram_dialog import Window, Dialog, StartMode
from aiogram_dialog.widgets.kbd import (
	SwitchTo,
	Row,
	ScrollingGroup,
	Select,
	Start,
	PrevPage,
	NextPage,
	Button,
	Back,
	StubScroll, Group, NumberedPager, CurrentPage
)
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const, Case

from app.src.bot.dialogs.admin_dialog.handlers import on_change_sort, on_select_message, on_sender, on_receiver
from app.src.bot.dialogs.admin_dialog.getters import (
	getter_main_admin_text,
	getter_messages, getter_message_content
)
from app.src.bot.dialogs.common.widgets import ADMIN_MENU_BUTTON, I18NFormat
from app.src.bot.states.dialog_states import (
	AdminStates,
	AdminSettingsStates,
	StatisticStates,
	AdminUsersStates,
	BroadcastStates,
	MainMenuStates,
)

main_admin_window = Window(
	I18NFormat('admin-start-text'),
	Row(
		Start(
			text=Const('Рассылка'),
			state=BroadcastStates.main_menu,
			id='broadcast'
		),
		Start(
			text=Const('Аналитика'),
			state=StatisticStates.main_menu,
			id='statistic'
		),
	),
	Row(
		Start(
			text=Const('Настройки'),
			state=AdminSettingsStates.main_menu,
			id='settings'
		),
		SwitchTo(
			text=Const('Сообщения'),
			state=AdminStates.messages,
			id='messages'
		),
	),
	Start(
		text=Const('Пользователи'),
		state=AdminUsersStates.main_menu,
		id='users'
	),
	Start(
		text=Const('👈 Назад'),
		state=MainMenuStates.main_menu,
		id='back_menu',
		mode=StartMode.RESET_STACK
	),
	getter=getter_main_admin_text,
	state=AdminStates.main_menu
)

messages = Window(
	I18NFormat('all-messages-text'),
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
	Group(
		Select(
			text=Format("🔸 {item[1]} #{item[0]}"),
			id='messages_select',
			items='messages',
			item_id_getter=itemgetter(0),
			on_click=on_select_message,
			type_factory=int
		),
		width=1
	),
	StubScroll(
		id='messages_scroll',
		pages='pages'
	),
	Row(
		PrevPage(
			scroll="messages_scroll", text=Format("👈 Назад"),
			when=F["current_page"] != 0
		),
		NextPage(
			scroll="messages_scroll", text=Format("👉 Вперед"),
			when=F["current_page"] != F["pages"] - 1
		),
	),
	Button(
			text=Format("[{current_page_}]"),
			id='current_page',
		),
	ADMIN_MENU_BUTTON,
	state=AdminStates.messages,
	getter=getter_messages
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
	Back(Const('👈 Назад')),
	state=AdminStates.show_message_content,
	getter=getter_message_content
)

admin_dialog = Dialog(
	main_admin_window,
	messages,
	select_message
)
