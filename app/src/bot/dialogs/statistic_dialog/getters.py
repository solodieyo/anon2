from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.bot.dialogs.common.widgets import SELECTED_DAYS_KEY
from app.src.bot.dialogs.statistic_dialog.text import get_statistic_text
from app.src.infrastructure.database.models_dto.statistic_dto import CommonStatisticDTO
from app.src.infrastructure.database.repositories import GeneralRepository


@inject
async def getter_statistic_text(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	i18n: I18nContext, **_
) -> dict:

	text = dialog_manager.dialog_data.get('statistic_text')
	statistic_type = dialog_manager.dialog_data.get('statistic_type', 'common_statistic')
	selected_date, start_date, end_date = None, None, None

	if not text:
		date_type = dialog_manager.dialog_data.get('date_type', 'today')

		if date_type == 'period':
			start_date, end_date = sorted(dialog_manager.dialog_data[SELECTED_DAYS_KEY])
		elif date_type == 'select_date':
			selected_date = dialog_manager.dialog_data['selected_date']

		statistic = await repository.statistic.get_statistic(
			date_type=date_type,
			statistic_type=statistic_type,
			start_date=start_date,
			end_date=end_date,
			selected_date=selected_date
		)
		text = get_statistic_text(
			i18n=i18n,
			statistic=statistic,
			statistic_type=statistic_type,
		)

	return {
		'statistic_text': text,
		"type": statistic_type
	}


async def getter_selector(dialog_manager: DialogManager, **_) -> dict:
	return {
		"date": dialog_manager.dialog_data.get('date_type', 'today')
	}