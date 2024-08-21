from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.src.bot.dialogs.factory.callback import SenderCallbackData, GetterCallbackData
from app.src.bot.senders.user_message import get_user_message
from app.src.infrastructure.database.repositories import GeneralRepository

router = Router()


@router.callback_query(SenderCallbackData.filter())
@inject
async def get_user_admin(
	callback: CallbackQuery,
	callback_data: SenderCallbackData,
	repository: FromDishka[GeneralRepository],
	i18n: I18nContext,
	bot: Bot
):
	await get_user_message(
		user_id=callback_data.user_id,
		i18n=i18n,
		repository=repository,
		bot=bot,
		chat_id=callback.from_user.id
	)


@router.callback_query(GetterCallbackData.filter())
@inject
async def get_user_by_id(
	callback: CallbackQuery,
	callback_data: GetterCallbackData,
	repository: FromDishka[GeneralRepository],
	i18n: I18nContext,
	bot: Bot
):
	await get_user_message(
		user_id=callback_data.user_id,
		i18n=i18n,
		repository=repository,
		bot=bot,
		chat_id=callback.from_user.id
	)
