from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.src.bot.dialogs.common.common_handlers import reply_anon_message
from app.src.bot.states.default_states import SendMessageStates
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository

router = Router()


@router.message(F.reply_to_message)
@inject
async def message_reply_answer(
	message: Message,
	repository: FromDishka[GeneralRepository],
	dialog_manager: DialogManager,
	i18n: I18nContext,
	bot: Bot,
	user: User
):
	to_user: User = await repository.user.get_user_by_msg_id(message_id=message.reply_to_message.message_id)
	await reply_anon_message(
		message=message,
		to_user=to_user,
		from_user=user,
		bot=bot,
		i18n=i18n,
		repository=repository,
		dialog_manager=dialog_manager
	)


@router.message(SendMessageStates.input_anon_message)
@inject
async def input_message(
	message: Message,
	state: FSMContext,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	i18n: I18nContext,
	bot: Bot,
	user: User
):
	data = await state.get_data()
	to_user: User = await repository.user.get_user_by_tg_id(user_id=data['to_user_id'])
	await reply_anon_message(
		message=message,
		to_user=to_user,
		from_user=user,
		bot=bot,
		i18n=i18n,
		repository=repository,
		dialog_manager=dialog_manager
	)

	await state.clear()
