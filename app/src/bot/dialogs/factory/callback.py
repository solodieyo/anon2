from aiogram.filters.callback_data import CallbackData


class ReceivedCallbackData(CallbackData, prefix='msg'):
	message_id: int
	from_user_id: int
	to_user_id: int


class BlockedCallbackData(CallbackData, prefix='bl'):
	from_user_id: int
	message_id: int


class SenderCallbackData(CallbackData, prefix='sender'):
	user_id: int


class GetterCallbackData(CallbackData, prefix='getter'):
	user_id: int


class UnblockCallbackData(CallbackData, prefix='ul'):
	message_id: int
	user_id: int
	blocked_user_id: int
	block_list: bool = False


class AdminDayStatistic(CallbackData, prefix='ads'):
	date_num: str
	now_state: str
