from typing import Dict, Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update
from dishka import AsyncContainer

from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository


class LastActivityMiddleware(BaseMiddleware):

	def __init__(self, dishka: AsyncContainer):
		super().__init__()
		self.dishka = dishka

	async def __call__(
		self,
		handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
		event: Update,
		data: Dict[str, Any]
	) -> Any:

		user: User = data['user']
		async with self.dishka() as req_dishka:
			repo = await req_dishka.get(GeneralRepository)
			await repo.user_updates.update_last_activity(user_id=user.user_id)

			if event.from_user.username != user.username:
				await repo.user.update_username(
					user_id=event.from_user.id,
					username=event.from_user.username
				)
				await repo.user_updates.update_username(
					before=user.username,
					after=event.from_user.username,
					user_id=user.user_id
				)
				user.username = event.from_user.username
			if event.from_user.full_name != user.full_name:
				await repo.user.update_full_name(
					user_id=event.from_user.id,
					full_name=event.from_user.full_name
				)
				await repo.user_updates.update_full_name(
					before=user.full_name,
					after=event.from_user.full_name,
					user_id=user.user_id
				)
				user.full_name = event.from_user.full_name
		data['user'] = user
		return await handler(event, data)