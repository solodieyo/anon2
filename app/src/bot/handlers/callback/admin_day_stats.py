from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.src.bot.dialogs.common.widgets import get_admin_day_keyboard
from app.src.bot.dialogs.factory.callback import AdminDayStatistic
from app.src.bot.dialogs.statistic_dialog.text import get_statistic_text
from app.src.infrastructure.database.repositories import GeneralRepository

router = Router()


@router.callback_query(AdminDayStatistic.filter())
@inject
async def admin_day_stats_callback(
	callback_query: CallbackQuery,
	callback_data: AdminDayStatistic,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
	i18n: I18nContext
):
	statistic = await repository.statistic.get_statistic(
		statistic_type=callback_data.now_state,
		selected_date=callback_data.date_num
	)
	await bot.edit_message_text(
		chat_id=callback_query.from_user.id,
		message_id=callback_query.message.message_id,
		text=get_statistic_text(
			i18n=i18n,
			statistic=statistic,
			statistic_type=callback_data.now_state,
		),
		reply_markup=get_admin_day_keyboard(
			date_num=callback_data.date_num,
			now_state=callback_data.now_state
		)
	)