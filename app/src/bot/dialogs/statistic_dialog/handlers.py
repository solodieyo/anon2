from datetime import date

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.kbd import ManagedCalendar, Button
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.bot.dialogs.statistic_dialog.text import get_statistic_text
from app.src.bot.dialogs.common.widgets import SELECTED_DAYS_KEY
from app.src.bot.states.dialog_states import StatisticStates, AdminStates
from app.src.infrastructure.database.repositories import GeneralRepository


@inject
async def on_common_statistic(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	date_type = dialog_manager.dialog_data.get('date_type', "today")
	dialog_manager.dialog_data['statistic_type'] = widget.widget_id
	await _button_process(
		dialog_manager=dialog_manager,
		widget_id=widget.widget_id,
		repository=repository,
		date_type=date_type,
	)


@inject
async def on_language_statistic(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	date_type = dialog_manager.dialog_data.get('date_type', "today")
	dialog_manager.dialog_data['statistic_type'] = widget.widget_id
	await _button_process(
		dialog_manager=dialog_manager,
		widget_id=widget.widget_id,
		repository=repository,
		date_type=date_type
	)


@inject
async def on_payments_statistic(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	date_type = dialog_manager.dialog_data.get('date_type', "today")
	dialog_manager.dialog_data['statistic_type'] = widget.widget_id
	await _button_process(
		dialog_manager=dialog_manager,
		widget_id=widget.widget_id,
		repository=repository,
		date_type=date_type
	)


async def on_date_select(
	callback: CallbackQuery,
	widget: ManagedCalendar,
	dialog_manager: DialogManager,
	selected_date: date, /,
):
	dialog_manager.dialog_data['date_type'] = widget.widget_id
	dialog_manager.dialog_data['selected_date'] = selected_date.isoformat()
	dialog_manager.dialog_data['statistic_text'] = None
	await dialog_manager.switch_to(state=StatisticStates.main_menu)


async def on_choice_stat_date(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
):
	dialog_manager.dialog_data['date_type'] = widget.widget_id
	dialog_manager.dialog_data['statistic_text'] = None
	await dialog_manager.switch_to(state=StatisticStates.main_menu)


async def on_date_selected(
	callback: ChatEvent,
	widget: ManagedCalendar,
	dialog_manager: DialogManager,
	clicked_date: date, /,
):
	selected = dialog_manager.dialog_data.setdefault(SELECTED_DAYS_KEY, [])
	serial_date = clicked_date.isoformat()
	if serial_date in selected:
		selected.remove(serial_date)
	elif len(selected) == 1:
		selected.append(serial_date)
		dialog_manager.dialog_data['date_type'] = widget.widget_id
		dialog_manager.dialog_data['statistic_text'] = None
		await dialog_manager.switch_to(StatisticStates.main_menu)
	elif len(selected) < 2:
		selected.append(serial_date)


async def _get_statistic(
	dialog_manager: DialogManager,
	repository: GeneralRepository,
	date_type: str,
	statistic_type: str,
	selected_date: date = None,
):
	if date_type == "period":
		dates = sorted(dialog_manager.dialog_data[SELECTED_DAYS_KEY])
		return await repository.statistic.get_statistic(
			statistic_type=statistic_type,
			date_type=date_type,
			start_date=dates[0],
			end_date=dates[1]

		)
	elif selected_date:
		return await repository.statistic.get_statistic(
			statistic_type=statistic_type,
			date_type=date_type,
			selected_date=selected_date

		)

	return await repository.statistic.get_statistic(
		statistic_type=statistic_type,
		date_type=date_type,
	)


async def _button_process(
	dialog_manager: DialogManager,
	widget_id: str,
	repository: GeneralRepository,
	date_type: str
):
	i18n: I18nContext = dialog_manager.middleware_data['i18n']
	selected_date = dialog_manager.dialog_data.get('selected_date')

	statistic = await _get_statistic(
		dialog_manager=dialog_manager,
		repository=repository,
		date_type=date_type,
		statistic_type=widget_id,
		selected_date=selected_date
	)

	text = get_statistic_text(
		i18n=i18n,
		statistic=statistic,
		statistic_type=widget_id
	)
	dialog_manager.dialog_data['statistic_text'] = text
	dialog_manager.dialog_data['date_type'] = date_type


