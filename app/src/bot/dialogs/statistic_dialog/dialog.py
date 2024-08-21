from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo, Calendar, Row, Button
from aiogram_dialog.widgets.text import Format, Const, Case

from app.src.bot.dialogs.statistic_dialog.getters import getter_statistic_text, getter_selector
from app.src.bot.dialogs.statistic_dialog.handlers import (
	on_date_select,
	on_choice_stat_date,
	on_date_selected,
	on_common_statistic,
	on_language_statistic,
	on_payments_statistic
)
from app.src.bot.dialogs.common.widgets import (
	ADMIN_MENU_BUTTON,
	CustomCalendar,
	STATISTIC_MENU_BUTTON,
)
from app.src.bot.states.dialog_states import StatisticStates

statistic_menu = Window(
	Format("{statistic_text}"),
	Row(
		Button(
			text=Case(
				{
					'common_statistic': Const('🔸 🏛 ОБЩАЯ'),
					...: Const('🏛 ОБЩАЯ'),
				},
				selector='type'
			),
			id='common_statistic',
			on_click=on_common_statistic
		),
		Button(
			text=Case(
				{
					'languages_statistic': Const('🔸 🇺🇳 ЯЗЫКИ'),
					...: Const('🇺🇳 ЯЗЫКИ'),
				},
				selector='type'
			),
			id='languages_statistic',
			on_click=on_language_statistic
		)
	),
	Button(
		text=Case(
			{
				"payments_statistic": Const('🔸 💳 ПОПОЛНЕНИЯ'),
				...: Const('💳 ПОПОЛНЕНИЯ'),
			},
			selector='type'
		),
		id='payments_statistic',
		on_click=on_payments_statistic
	),
	SwitchTo(
		text=Const('📅 СМЕНИТЬ ДАТУ'),
		state=StatisticStates.choice_date,
		id='choice_date'
	),
	ADMIN_MENU_BUTTON,
	state=StatisticStates.main_menu,
	getter=getter_statistic_text
)

statistic_date = Window(
	Format("{statistic_text}"),
	Row(
		Button(
			text=Case({
				"today": Const('🔸 Сегодня'),
				...: Const('Сегодня'),
			},
				selector='date'
			),
			id='today',
			on_click=on_choice_stat_date,
		),
		Button(
			text=Case({
				"week": Const('🔸 Неделя'),
				...: Const('Неделя'),
			},
				selector='date'
			),
			id='week',
			on_click=on_choice_stat_date
		),
	),
	Row(
		SwitchTo(
			text=Case({
				"select_date": Const('🔸 Выбрать дату'),
				...: Const('Выбрать дату'),
			},
				selector='date'
			),
			state=StatisticStates.select_date,
			id='select_date'
		),
		SwitchTo(
			text=Case({
				"select_period": Const('🔸 Выбрать период'),
				...: Const('Выбрать период'),
			},
				selector='date'
			),
			state=StatisticStates.select_period,
			id='select_period'
		),
	),
	Button(
		text=Case({
			"month": Const('🔸 Месяц'),
			...: Const('Месяц'),
		},
			selector='date'
		),
		id='month',
		on_click=on_choice_stat_date
	),
	SwitchTo(
		text=Const('👈 Назад'),
		state=StatisticStates.main_menu,
		id='__switch_to_main__'
	),
	state=StatisticStates.choice_date,
	getter=(
		getter_statistic_text,
		getter_selector
	)
)

select_date = Window(
	Const('Выберите дату'),
	Calendar(
		id='select_date',
		on_click=on_date_select
	),
	STATISTIC_MENU_BUTTON,
	state=StatisticStates.select_date,
)

select_period = Window(
	Const('Выберите период'),
	CustomCalendar(
		id='period',
		on_click=on_date_selected
	),
	STATISTIC_MENU_BUTTON,
	state=StatisticStates.select_period,
)

statistic_dialog = Dialog(
	statistic_menu,
	statistic_date,
	select_date,
	select_period
)
