from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
	SwitchTo,
	Button,
	ScrollingGroup,
	Select,
	Start,
	Row,
	Url,
	Back,
	PrevPage,
	NextPage
)
from aiogram_dialog.widgets.text import Format, Case, Const

from app.src.bot.dialogs.common.common_getters import getter_count_messages
from app.src.bot.dialogs.profile_dialog.getter import (
	getter_profile_menu_text,
	getter_profile_settings_text,
	getter_hello_menu,
	getter_ban_list,
	getter_top_type,
	getter_user_id,
	getter_invoice_stars_text,
	getter_invoice_crypto_text, getter_premium_sub, get_price, get_ban_list_id, getter_bot_username
)
from app.src.bot.dialogs.profile_dialog.handlers import (
	on_input_new_hello_message,
	delete_user_hello_message,
	on_input_new_username,
	on_select_banned,
	on_delete_username,
	change_tops_status,
	on_select_type_top,
	choice_premium_period,
	delete_time, change_show_status
)
from app.src.bot.dialogs.common.widgets import (
	I18NFormat,
	USER_PROFILE_SETTINGS_BACK_BUTTON,
	USER_BACK_TO_PROFILE, MAIN_MENU_BUTTON
)
from app.src.bot.filters.username import UsernameFilter, HelloMessageFilter
from app.src.bot.states.dialog_states import ProfileStates, MainMenuStates

profile_menu = Window(
	I18NFormat('profile-menu-user-kek'),
	SwitchTo(
		I18NFormat('profile-menu-premium'),
		'switch_premium',
		state=ProfileStates.premium
	),
	SwitchTo(
		I18NFormat('profile-menu-rating'),
		'switch_rating',
		state=ProfileStates.rating),
	SwitchTo(
		I18NFormat('profile-menu-settings'),
		'switch_settings',
		state=ProfileStates.settings
	),
	MAIN_MENU_BUTTON,
	state=ProfileStates.main_menu,
	getter=(
		getter_profile_menu_text,
		getter_count_messages
	),
	disable_web_page_preview=True
)

profile_settings = Window(
	I18NFormat('profile-settings'),
	SwitchTo(
		I18NFormat('profile-settings-hello'),
		'change_hello',
		state=ProfileStates.change_hello
	),
	SwitchTo(
		I18NFormat('profile-settings-username'),
		'create_username',
		state=ProfileStates.create_username
	),
	Start(
		I18NFormat('profile-settings-language'),
		'change_language',
		state=MainMenuStates.choice_language,
		data={"profile": True}
	),
	SwitchTo(
		I18NFormat('ban-list'),
		'ban_list',
		state=ProfileStates.ban_list
	),
	USER_BACK_TO_PROFILE,
	state=ProfileStates.settings,
	getter=getter_profile_settings_text
)

# тут оплату потом прикрутить в старсах или еще какойто хуйне
profile_premium = Window(
	I18NFormat('profile-premium'),
	Button(
		text=Case(
			{
				False: I18NFormat('profile-premium-show-off'),
				True: I18NFormat('profile-premium-show-on')
			},
			selector='show_username'
		),
		id='show_username_premium',
		on_click=change_show_status,
		when=F['middleware_data']['user'].premium.is_(True),
	),
	Button(
		text=I18NFormat('day-premium-button'),
		id='premium_price_day',
		on_click=choice_premium_period,
		when=F['day'].is_(True),
	),
	Button(
		text=I18NFormat('week-premium-button'),
		id='premium_price_week',
		on_click=choice_premium_period,
		when=F['week'].is_(True),
	),
	Button(
		text=I18NFormat('month-premium-button'),
		id='premium_price_month',
		on_click=choice_premium_period,
		when=F['month'].is_(True),
	),
	Button(
		text=I18NFormat('forever-premium-button'),
		id='premium_price_forever',
		on_click=choice_premium_period,
		when=F['forever'].is_(True),
	),
	Start(
		text=I18NFormat('back'),
		id="__user_profile__",
		state=ProfileStates.main_menu,
		mode=StartMode.RESET_STACK,
		when=F['command'].is_not(True)
	),
	state=ProfileStates.premium,
	getter=getter_premium_sub
)

premium_choice_pay = Window(
	I18NFormat('premium-choose-pay'),
	SwitchTo(
		text=Const('Telegram Stars'),
		id='premium_stars',
		state=ProfileStates.premium_stars
	),
	SwitchTo(
		text=Const('Crypto-Bot'),
		id='premium_crypto',
		state=ProfileStates.premium_crypto
	),
	Back(
		text=I18NFormat('back'),
	),
	state=ProfileStates.choice_pay,
	getter=get_price
)

premium_crypto_pay = Window(
	I18NFormat('premium-pay-finish'),
	Url(
		text=I18NFormat('stars-invoice-title'),
		url=Format('{link}')
	),
	SwitchTo(
		text=I18NFormat('back'),
		id='__back_to_choice__',
		state=ProfileStates.choice_pay,
		on_click=delete_time
	),
	state=ProfileStates.premium_crypto,
	getter=getter_invoice_crypto_text,
	disable_web_page_preview=True
)

premium_stars_pay = Window(
	I18NFormat('premium-pay-finish'),
	Url(
		text=I18NFormat('stars-invoice-title'),
		url=Format('{link}')
	),
	SwitchTo(
		text=I18NFormat('back'),
		id='__back_to_choice__',
		state=ProfileStates.choice_pay,
		on_click=delete_time
	),
	state=ProfileStates.premium_stars,
	getter=getter_invoice_stars_text,
	disable_web_page_preview=True
)

success_payment = Window(
	I18NFormat('success-payment'),
	SwitchTo(
		text=I18NFormat('to-menu'),
		id='__back_to_menu__',
		state=ProfileStates.main_menu
	),
	state=ProfileStates.success_payed
)

profile_change_hello = Window(
	I18NFormat('profile-change-hello'),
	I18NFormat(
		text='wrong-hello-message',
		when=F['wrong_hello'].is_(True)
	),
	MessageInput(
		content_types=ContentType.TEXT,
		func=on_input_new_hello_message,
		filter=HelloMessageFilter()
	),
	Button(
		text=I18NFormat('delete-hello'),
		id='check_hello',
		on_click=delete_user_hello_message,
		when=F['hello_message'] != 'no'
	),
	USER_PROFILE_SETTINGS_BACK_BUTTON,
	state=ProfileStates.change_hello,
	getter=getter_hello_menu,
)

ban_list = Window(
	I18NFormat(
		'ban-list-menu-text',
		when=F['ban_list'].len() == 0
	),
	I18NFormat(
		'ban-list',
		when=F['ban_list'].len() > 0
	),
	ScrollingGroup(
		Select(
			text=Format("{item.text} {item.content_type}"),
			id='blocked_select',
			items='ban_list',
			item_id_getter=get_ban_list_id,
			on_click=on_select_banned
		),
		id='ban_list_scroll',
		width=1,
		height=8,
		hide_pager=True
	),
	Row(
		PrevPage(
			scroll="ban_list_scroll", text=Format("👈 Назад"),
			when=F["pages"] > 1 & F["current_page1"] != 1
		),
		NextPage(
			scroll="ban_list_scroll", text=Format("👉 Вперед"),
			when=F["current_page1"] != F["pages"]
		),
		when=F["ban_list"].len() > 0
	),
	USER_PROFILE_SETTINGS_BACK_BUTTON,
	state=ProfileStates.ban_list,
	getter=getter_ban_list
)

create_username = Window(
	I18NFormat('profile-create-username'),
	I18NFormat(
		'profile-wrong-input-username',
		when=F['dialog_data']['wrong_username'].is_(True)
	),
	I18NFormat(
		text='username-exist-already',
		when=F['exist_username'].is_(True)
	),
	MessageInput(
		content_types=ContentType.TEXT,
		func=on_input_new_username,
		filter=UsernameFilter()
	),
	Button(
		I18NFormat('delete-username'),
		id='delete_username',
		on_click=on_delete_username,
		when=F["middleware_data"]['user'].custom_username.is_not(None)

	),
	USER_PROFILE_SETTINGS_BACK_BUTTON,
	state=ProfileStates.create_username,
	getter=(
		getter_user_id,
		getter_bot_username
	)
)

rating_window = Window(
	I18NFormat('ratings-text'),
	Row(
		Button(
			text=Case(
				{
					"senders": I18NFormat('senders-button-active'),
					"getters": I18NFormat('senders-button-disabled'),

				},
				selector='type'
			),
			id='senders',
			on_click=on_select_type_top,
		),
		Button(
			Case(
				{
					"getters": I18NFormat('getters-button-active'),
					"senders": I18NFormat('getters-button-disabled'),
				},
				selector='type'
			),
			id='getters',
			on_click=on_select_type_top,
		),
	),
	Button(
		Case(
			{
				True: I18NFormat('hide-in-tops'),
				False: I18NFormat('show_in_tops')
			},
			selector=F['middleware_data']['user'].show_in_tops,
		),
		id='show_in_tops',
		on_click=change_tops_status
	),
	USER_BACK_TO_PROFILE,
	state=ProfileStates.rating,
	getter=getter_top_type
)

profile_dialog = Dialog(
	profile_menu,
	profile_settings,
	profile_premium,
	premium_choice_pay,
	premium_stars_pay,
	premium_crypto_pay,
	success_payment,
	profile_change_hello,
	ban_list,
	create_username,
	rating_window
)
