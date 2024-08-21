
from aiogram import html
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import I18nContext

from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.models_dto.statistic_dto import UserMessageStatisticDTO
from app.src.infrastructure.database.repositories import GeneralRepository


async def get_user_message(
	bot: Bot,
	i18n: I18nContext,
	user_id: int,
	repository: GeneralRepository,
	chat_id: int,
):
	user: User = await repository.user.get_user_by_tg_id(user_id=user_id)
	user_statistic: UserMessageStatisticDTO = await repository.statistic.get_user_message_statistic(
		user_id=user.id)

	keyboard = InlineKeyboardMarkup(
		inline_keyboard=[
			[InlineKeyboardButton(
				text="❌ Закрыть",
				callback_data='delete_message'
			)]
		]

	)
	text = i18n.get(
		'admin-user-info-text',
		from_user_id=user.user_id,
		locale=user.locale,
		created_at=user.created_at,
		full_name=html.quote(user.full_name),
		username=user.custom_username or user.username,
		role=user.rank,
		message_sent=user_statistic.message_sent_count,
		message_sent_today=user_statistic.message_sent_today,
		message_got=user_statistic.message_got_count,
		message_got_today=user_statistic.message_got_today
	)

	await bot.send_message(
		text=text,
		reply_markup=keyboard,
		chat_id=chat_id
	)