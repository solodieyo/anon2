from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from app.src.bot.states.dialog_states import ProfileStates

router = Router()


@router.message(Command('profile'))
async def start_profile(message: Message, dialog_manager: DialogManager):
	await dialog_manager.start(
		state=ProfileStates.main_menu,
		mode=StartMode.RESET_STACK,
		show_mode=ShowMode.DELETE_AND_SEND
	)

