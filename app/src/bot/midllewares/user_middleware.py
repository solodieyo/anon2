from typing import Any, Callable, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, CallbackQuery, Message
from aiogram_i18n import I18nMiddleware, I18nContext
from dishka import AsyncContainer

from app.src.infrastructure.database.repositories import GeneralRepository


class UserMiddleware(BaseMiddleware):

	def __init__(self, dishka: AsyncContainer, i18n_middleware: I18nMiddleware):
		super().__init__()
		self.dishka = dishka
		self.i18n_middleware = i18n_middleware

	async def __call__(
		self,
		handler: Callable[[TelegramObject, dict[str, any]], Awaitable[Any]],
		event: Union[Message, CallbackQuery],
		data: dict[str: Any]
	):

		i18n: I18nContext = data['i18n']
		async with self.dishka() as req_dishka:
			repo = await req_dishka.get(GeneralRepository)

			user, new_user = await repo.user.get_or_create_user(
				user_id=event.from_user.id,
				username=event.from_user.username,
				locale=event.from_user.language_code,
				full_name=event.from_user.full_name,
				i18n_middleware=self.i18n_middleware
			)

		data['user'] = user
		data["new_user"] = new_user
		await i18n.set_locale(user.locale)
		return await handler(event, data)
