from aiogram import F
from aiogram_dialog import Window, Dialog, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Start, Button, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const

from app.src.bot.dialogs.main_menu.handlers import choice_language
from app.src.bot.dialogs.main_menu.getters import getter_main_menu_text, getter_start_picture, admin_getter, \
	getter_languages_statuses
from app.src.bot.dialogs.common.widgets import I18NFormat, MAIN_MENU_BUTTON
from app.src.bot.states.dialog_states import MainMenuStates, ProfileStates, AdminStates

choice_language = Window(
	I18NFormat('choice-language-text'),
	Row(
		Button(
			text=I18NFormat('ru-button'),
			id='ru',
			on_click=choice_language
		),
		Button(
			text=I18NFormat('en-button'),
			id='en',
			on_click=choice_language,
			when=F['en'].is_not(False)
		),
	),
	Row(
		Button(
			text=I18NFormat('de-button'),
			id='de',
			on_click=choice_language,
			when=F['de'].is_not(False)
		),
		Button(
			text=I18NFormat('ua-button'),
			id='uk',
			on_click=choice_language,
			when=F['uk'].is_not(False)
		)
	),
	Start(
		text=I18NFormat('back'),
		id='back_profile',
		state=ProfileStates.settings,
		when=F['start_data']['profile'].is_(True),
		mode=StartMode.RESET_STACK
	),
	state=MainMenuStates.choice_language,
	getter=getter_languages_statuses
)


main_menu = Window(
	DynamicMedia('start_photo', when=F['start_photo']),
	I18NFormat('main-menu-text'),
	Start(
		I18NFormat('profile-button'),
		state=ProfileStates.main_menu,
		id='start_profile'
	),
	Start(
		text=Const('🅰️ Админ панель'),
		state=AdminStates.main_menu,
		id='start_admin',
		when=F['is_admin'].is_(True),
		show_mode=ShowMode.DELETE_AND_SEND
	),
	state=MainMenuStates.main_menu,
	getter=(
		getter_main_menu_text,
		getter_start_picture,
		admin_getter
	)
)


main_menu_dialog = Dialog(
	choice_language,
	main_menu
)
