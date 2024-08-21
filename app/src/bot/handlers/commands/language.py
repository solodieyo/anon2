from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from app.src.bot.states.dialog_states import MainMenuStates

router = Router()


@router.message(Command('language'))
async def select_language(message: Message, dialog_manager: DialogManager):
	await dialog_manager.start(
		state=MainMenuStates.choice_language,
		mode=StartMode.RESET_STACK,
		show_mode=ShowMode.DELETE_AND_SEND
	)

