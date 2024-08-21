from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from app.src.bot.states.dialog_states import AdminStates

router = Router()


@router.message(Command('admin'))
async def start_admin(message: Message, dialog_manager: DialogManager):
	await dialog_manager.start(
		state=AdminStates.main_menu,
		mode=StartMode.RESET_STACK,
		show_mode=ShowMode.DELETE_AND_SEND
	)

