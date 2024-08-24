from datetime import datetime, timedelta

from aiogram_i18n import I18nMiddleware
from sqlalchemy import select, update

from app.src.enums import Roles
from app.src.infrastructure.database.models import Message
from app.src.infrastructure.database.models.user import User
from app.src.infrastructure.database.repositories.base import BaseRepository


class UserRepository(BaseRepository):

	async def get_or_create_user(
		self,
		user_id: int,
		username: str,
		locale: str,
		full_name: str,
		i18n_middleware: I18nMiddleware
	) -> tuple[User, bool]:
		user = await self.session.scalar(select(User).where(User.user_id == user_id))
		new_user = False

		if not user:
			if locale not in i18n_middleware.core.available_locales:
				locale = i18n_middleware.core.default_locale
			user = User(
				user_id=user_id,
				username=username,
				locale=locale,
				full_name=full_name,
			)
			self.session.add(user)
			await self.session.commit()
			new_user = True
		return user, new_user

	async def get_user_status(self, user_id: int):
		result = await self.session.scalar(select(User.premium).where(User.user_id == user_id))
		return result

	async def get_user_username(self, user_id: int):
		query = await self.session.execute(select(User.custom_username, User.username).where(User.user_id == user_id))

		result = query.fetchone()

		if result:
			if result[0]:
				return result[0]
			return result[1]
		return '...'

	async def get_user_rank(self, user_id: int):
		result = await self.session.scalar(select(User.rank).where(User.user_id == user_id))
		return result

	async def set_user_locale(self, user_id: int, locale: str):
		await self.session.execute(update(User).where(User.user_id == user_id).values(locale=locale))
		await self.session.commit()

	async def get_user_locale(self, user_id: int):
		result = await self.session.scalar(select(User.locale).where(User.user_id == user_id))
		return result

	async def get_user_by_tg_id(self, user_id: int):
		result: User | None = await self.session.scalar(select(User).where(User.user_id == user_id))
		return result

	async def get_user_by_id(self, user_pk: int):
		result: User | None = await self.session.scalar(select(User).where(User.id == user_pk))
		return result

	async def get_user_by_username(self, username: str):
		result: User | None = await self.session.scalar(select(User).where(User.username == username))
		return result

	async def get_user_by_custom_username(self, custom_username: str):
		result: int | None = await self.session.scalar(
			select(User.user_id).where(User.custom_username == custom_username))
		return result

	async def get_user_by_msg_id(self, message_id: int):
		result_user_id: int = await self.session.scalar(
			select(Message.from_user_id).where(Message.tg_message_id == message_id)
		)
		result_user = await self.get_user_by_id(result_user_id)
		return result_user

	async def get_user_start(self, user_data: str):
		if user_data[0].isalpha():
			result: User | None = await self.session.scalar(select(User).where(User.custom_username == user_data))
		else:
			result: User | None = await self.session.scalar(select(User).where(User.user_id == int(user_data)))
		return result

	async def get_user_by_full_name(self, full_name: str):
		result: User | None = await self.session.scalar(select(User).where(User.full_name == full_name))
		return result

	async def set_user_rank(self, user_id: int, rank: Roles):
		await self.session.execute(update(User).where(User.user_id == user_id).values(rank=rank))
		await self.session.commit()

	async def get_user_hello_message(self, user_id: int):
		result = await self.session.scalar(select(User.hello_message).where(User.user_id == user_id))
		return result

	async def set_user_hello_message(self, user_id: int, text: str):
		await self.session.execute(update(User).where(User.user_id == user_id).values(hello_message=text))
		await self.session.commit()

	async def set_username(self, user_id: int, username: str | None):
		await self.session.execute(update(User).where(User.user_id == user_id).values(custom_username=username))
		await self.session.commit()

	async def update_user_top_status(self, user_id: int, status: bool):
		await self.session.execute(update(User).where(User.user_id == user_id).values(show_in_tops=status))
		await self.session.commit()

	async def update_premium_settings(self, user_id: int, value: bool):
		await self.session.execute(update(User).where(User.user_id == user_id).values(show_premium_username=value))
		await self.session.commit()

	async def get_hello_message(self, user_id: int):
		result = await self.session.scalar(select(User.hello_message).where(User.user_id == user_id))
		return result

	async def delete_premium(self, user_id: int):
		await self.session.execute(update(User).where(User.user_id == user_id).values(
			premium=False, premium_date=None
		))
		await self.session.commit()

	async def set_premium(self, user_id: int, count_days: int):
		await self.session.execute(update(User).where(User.user_id == user_id).values(
			premium=True, premium_date=datetime.now() + timedelta(days=count_days)
		))
		await self.session.commit()

	async def update_premium_date(self, user_id: int, date: datetime):
		await self.session.execute(update(User).where(User.user_id == user_id).values(premium_date=date))
		await self.session.commit()

	async def set_premium_forever(self, user_id: int):
		await self.session.execute(update(User).where(User.user_id == user_id).values(
			premium=True
		))
		await self.session.commit()

	async def unarchive_user(self, user_id: int):
		await self.session.execute(update(User).where(User.user_id == user_id).values(
			archive=False
		))
		await self.session.commit()

	async def archive_user(self, user_id: int):
		await self.session.execute(update(User).where(User.user_id == user_id).values(
			archive=True
		))
		await self.session.commit()

	async def update_username(self, user_id, username):
		await self.session.execute(update(User).where(User.user_id == user_id).values(
			username=username
		))
		await self.session.commit()

	async def update_full_name(self, user_id, full_name):
		await self.session.execute(update(User).where(User.user_id == user_id).values(
			full_name=full_name
		))
		await self.session.commit()

	async def set_referral(self, user_id: int, referral_id: int):
		await self.session.execute(update(User).where(User.user_id == user_id).values(
			referral_user_id=referral_id
		))
		await self.session.commit()
