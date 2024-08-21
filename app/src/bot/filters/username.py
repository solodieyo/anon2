import re

from aiogram.filters import Filter
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode

from app.src.bot.states.dialog_states import ProfileStates


class UsernameFilter(Filter):
	async def __call__(self, message: Message, dialog_manager: DialogManager):
		username = dialog_manager.current_context().dialog_data.get("username")
		pattern = r'^[a-zA-Z][a-zA-Z0-9_]{4,31}$'
		dialog_manager.dialog_data['wrong_username'] = False
		dialog_manager.dialog_data['exist_username'] = False
		if 4 < len(message.text) < 32 and re.match(pattern, message.text) is not None:
			return True
		dialog_manager.dialog_data['wrong_username'] = True
		await dialog_manager.switch_to(
			state=ProfileStates.create_username,
			show_mode=ShowMode.DELETE_AND_SEND,
		)
		return False


class HelloMessageFilter(Filter):
	async def __call__(self, message: Message, dialog_manager: DialogManager):
		if 1 < len(message.text) < 1000:
			dialog_manager.dialog_data['wrong_hello'] = False
			return True
		dialog_manager.dialog_data['wrong_hello'] = True
		await dialog_manager.switch_to(
			state=ProfileStates.change_hello,
			show_mode=ShowMode.DELETE_AND_SEND,
		)
		return False
