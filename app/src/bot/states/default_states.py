from aiogram.fsm.state import StatesGroup, State


class SendMessageStates(StatesGroup):
	input_anon_message = State()
