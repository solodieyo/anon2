from typing import Any, Awaitable, Callable, Union

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, TelegramObject

from app.src.infrastructure.database.models import Message


class ClearState(BaseMiddleware):

	async def __call__(
		self,
		handler: Callable[[TelegramObject, dict[str, any]], Awaitable[Any]],
		event: Union[Message, CallbackQuery],
		data: dict[str: Any]
	):

		state: FSMContext = data['state']
		await state.clear()
		return await handler(event, data)