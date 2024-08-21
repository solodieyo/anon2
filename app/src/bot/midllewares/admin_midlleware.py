from typing import Any, Callable, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram_i18n import I18nMiddleware, I18nContext
from dishka import AsyncContainer

from app.src.config import AppConfig
from app.src.enums import Roles
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository


class AdminMiddleware(BaseMiddleware):

	def __init__(self, dishka: AsyncContainer):
		super().__init__()
		self.dishka = dishka

	async def __call__(
		self,
		handler: Callable[[TelegramObject, dict[str, any]], Awaitable[Any]],
		event: Union[Message, CallbackQuery],
		data: dict[str: Any]
	):

		user: User = data['user']
		config: AppConfig = await self.dishka.get(AppConfig)
		async with self.dishka() as req_dishka:
			repo = await req_dishka.get(GeneralRepository)

			user_role = await repo.user.get_user_rank(
				user_id=user.user_id
			)

		if user_role == Roles.ADMIN or user.user_id == config.tg.admin_id:
			return await handler(event, data)
		return