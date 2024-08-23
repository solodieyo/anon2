from aiogram.enums import ContentType
from aiogram_dialog import Window, ShowMode, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo, Start
from aiogram_dialog.widgets.text import Format

from app.src.bot.dialogs.common.common_handlers import ignore
from app.src.bot.dialogs.send_message_dialog.getters import start_hello_message
from app.src.bot.dialogs.send_message_dialog.handlers import (
	on_input_anon_message
)
from app.src.bot.dialogs.common.widgets import I18NFormat, MAIN_MENU_BUTTON
from app.src.bot.states.dialog_states import SendAnonMessagesStates, MainMenuStates

input_anon_msg = Window(
	Format("{text}"),
	MessageInput(
		func=on_input_anon_message,
		content_types=[
			ContentType.TEXT,
			ContentType.AUDIO,
			ContentType.DOCUMENT,
			ContentType.PHOTO,
			ContentType.STICKER,
			ContentType.VIDEO,
			ContentType.VIDEO_NOTE,
			ContentType.VOICE
		]
	),
	Start(
		Format('{text_back}'),
		id='cancel_sending',
		state=MainMenuStates.main_menu,
		show_mode=ShowMode.DELETE_AND_SEND
	),
	state=SendAnonMessagesStates.input_anon_msg,
	getter=start_hello_message,
)


success_sent = Window(
	I18NFormat('success-send'),
	SwitchTo(
		I18NFormat('send-again-message'),
		id='send_again_message',
		state=SendAnonMessagesStates.input_anon_msg
	),
	MessageInput(func=ignore),
	MAIN_MENU_BUTTON,
	state=SendAnonMessagesStates.success_send
)


anon_msg_dialog = Dialog(
	input_anon_msg,
	success_sent,
)
