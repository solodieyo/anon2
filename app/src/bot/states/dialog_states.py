from aiogram.fsm.state import StatesGroup, State


class MainMenuStates(StatesGroup):
	choice_language = State()
	main_menu = State()
	statistic = State()
	profile = State()


class AdminStates(StatesGroup):
	main_menu = State()
	change_date = State()
	statistic = State()
	settings = State()
	languages = State()
	change_picture = State()
	change_price = State()
	messages = State()
	show_message_content = State()


class ProfileStates(StatesGroup):
	main_menu = State()
	premium = State()
	premium_stars = State()
	rating = State()
	settings = State()
	change_hello = State()
	create_username = State()
	change_language = State(),
	ban_list = State()
	choice_pay = State()
	buy_premium = State()
	premium_crypto = State()
	success_payed = State()


class SendAnonMessagesStates(StatesGroup):
	input_anon_msg = State()
	get_anon_msg = State()
	blocked_success = State()
	success_send = State()


class StatisticStates(StatesGroup):
	main_menu = State()
	choice_date = State()
	select_date = State()
	select_period = State()


class AdminSettingsStates(StatesGroup):
	main_menu = State()
	languages = State()
	select_price = State()
	change_picture = State()
	select_change_price_type = State()
	change_price = State()
	confirm_language = State()


class AdminUsersStates(StatesGroup):
	main_menu = State()
	manage_user = State()
	no_user_found = State()
	premium_manage = State()
	user_sent_messages = State()
	user_got_messages = State()
	give_role = State()
	show_message_content = State()


class BroadcastStates(StatesGroup):
	main_menu = State()
	input_message = State()
	default = State()
	premium = State()
	all = State()
	previous_mailing = State()
	confirm_start = State()
	show_previus_mailing_content = State()
	users_type = State()
