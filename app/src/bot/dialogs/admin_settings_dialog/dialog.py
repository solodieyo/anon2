from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo, Row, Button, Back, Column
from aiogram_dialog.widgets.text import Const, Format, Case

from app.src.bot.dialogs.admin_settings_dialog.getters import (
	getter_start_picture,
	getter_lang_statuses,
	getter_language_confirm, getter_prices
)
from app.src.bot.dialogs.admin_settings_dialog.handlers import (
	on_select_price,
	on_input_start_picture,
	delete_start_picture,
	on_input_new_price,
	confirm_language,
	manage_language, on_select_pay_type
)
from app.src.bot.dialogs.common.widgets import ADMIN_MENU_BUTTON, SETTINGS_MENU_BUTTON
from app.src.bot.states.dialog_states import AdminSettingsStates

settings = Window(
	Const(text='Настройки'),
	Row(
		SwitchTo(
			text=Const('Языки'),
			state=AdminSettingsStates.languages,
			id='languages'
		),
		SwitchTo(
			text=Const('Установить начальное фото'),
			state=AdminSettingsStates.change_picture,
			id='change_picture'
		),
	),
	Row(
		SwitchTo(
			text=Const('Изменить цены'),
			state=AdminSettingsStates.select_change_price_type,
			id='change_price'
		)
	),
	ADMIN_MENU_BUTTON,
	state=AdminSettingsStates.main_menu
)

start_picture = Window(
	Const(text='<b>Установить начальное фото\nОтправьте картинку которую будут видеть пользователи</b>'),
	Format(
		'\n\nФотография успешно установлена',
		when=F["dialog_data"]['start_picture']
	),
	MessageInput(
		content_types=ContentType.PHOTO,
		func=on_input_start_picture
	),
	Button(
		text=Const('Удалить фото'),
		id='delete_picture',
		on_click=delete_start_picture,
		when=F['start_picture']
	),
	SETTINGS_MENU_BUTTON,
	state=AdminSettingsStates.change_picture,
	getter=getter_start_picture
)


select_change_type = Window(
	Const(text='<b>Выберете платежку</b>'),
	Button(
		text=Const('Crypto bot'),
		id='crypto',
		on_click=on_select_pay_type
	),
	Button(
		text=Const('Stars'),
		id='stars',
		on_click=on_select_pay_type
	),
	SETTINGS_MENU_BUTTON,
	state=AdminSettingsStates.select_change_price_type,
)



change_price = Window(
	Const(text='<b>💳 Выберите цену для изменения</b>'),
	Button(
		text=Format("1 ДЕНЬ - {prices.price_day}"),
		id='premium_price_day',
		on_click=on_select_price
	),
	Button(
		text=Format("7 ДНЕЙ - {prices.price_week}"),
		id='premium_price_week',
		on_click=on_select_price
	),
	Button(
		text=Format("30 ДНЕЙ - {prices.price_month}"),
		id='premium_price_month',
		on_click=on_select_price
	),
	Button(
		text=Format("НАВСЕГДА - {prices.price_forever}"),
		id='premium_price_forever',
		on_click=on_select_price
	),
	SETTINGS_MENU_BUTTON,
	state=AdminSettingsStates.select_price,
	getter=getter_prices
)

input_new_price = Window(
	Const(text='Введите новую цену (число)'),
	MessageInput(
		content_types=ContentType.TEXT,
		filter=F.text.isdigit(),
		func=on_input_new_price
	),
	Back(
		text=Const('Назад'),
	),
	state=AdminSettingsStates.change_price
)

language_manage = Window(
	Const(text='Языки'),
	Column(
		Button(
			text=Case(
				{
					False: Const('❌ Английский'),
					True: Const('✅ Английский'),
				},
				selector='en'
			),
			id='locale_en',
			on_click=manage_language
		),
		Button(
			text=Case(
				{
					False: Const('❌ Немецкий'),
					True: Const('✅ Немецкий'),
				},
				selector='de'
			),
			id='locale_de',
			on_click=manage_language,
		),
		Button(
			text=Case(
				{
					False: Const('❌ Украинский'),
					True: Const('✅ Украинский'),
				},
				selector='uk'
			),
			id='locale_uk',
			on_click=manage_language,
		)
	),
	SETTINGS_MENU_BUTTON,
	state=AdminSettingsStates.languages,
	getter=getter_lang_statuses

)

confirm_dialog = Window(
	Case(
		{
			True: Format(text='Вы уверены что хотите отключить {language} язык?'),
			False: Format(text='Вы уверены что хотите включить {language} язык?')
		},
		selector='language_state'
	),
	Button(
		text=Const('Да'),
		id='confirm',
		on_click=confirm_language
	),
	Back(
		text=Const('Нет'),
		id='cancel',
	),
	state=AdminSettingsStates.confirm_language,
	getter=getter_language_confirm
)


admin_dialog_settings = Dialog(
	settings,
	start_picture,
	select_change_type,
	change_price,
	input_new_price,
	language_manage,
	confirm_dialog
)
