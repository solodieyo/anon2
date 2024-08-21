from datetime import date
from typing import Optional

from aiogram.enums import ContentType
from sqlalchemy import select, and_
from sqlalchemy.sql.functions import func

from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.models.media import Media
from app.src.infrastructure.database.models.messages import Message
from app.src.infrastructure.database.models_dto.message_dto import MessageDTO
from app.src.infrastructure.database.repositories.base import BaseRepository


class MessagesRepository(BaseRepository):

	async def add_message(
		self,
		from_user_id: int,
		to_user_id: int,
		message: str,
		content_type: Optional[ContentType],
		media_id: Optional[str],
		media_name: Optional[str]
	) -> Message:

		new_message = Message(
			from_user_id=from_user_id,
			to_user_id=to_user_id,
			message=message,
		)
		if media_id:
			media = Media(
				content_type=content_type,
				file_id=media_id,
				file_name=media_name
			)
			self.session.add(media)
			await self.session.flush()
			new_message.media_id = media.id

		self.session.add(new_message)
		await self.session.commit()
		return new_message

	async def get_message(self, message_id: int) -> MessageDTO:
		print(message_id, type(message_id))
		message = await self.session.scalar(
			select(
				Message
			).where(Message.id == message_id)
		)
		media = await self.session.scalar(select(Media).where(Media.id == message.media_id))

		from_user = await self.session.scalar(select(User).where(User.id == message.from_user_id))
		to_user = await self.session.scalar(select(User).where(User.id == message.to_user_id))

		return MessageDTO(
			from_user=from_user,
			to_user=to_user,
			message=message,
			media=media
		)

	async def get_received_messages_count(self, user_id: int):
		result = await self.session.scalar(select(func.count(Message.id)).where(Message.to_user_id == user_id))
		return result

	async def get_sent_messages_count(self, user_id: int):
		result = await self.session.scalar(select(func.count(Message.id)).where(Message.from_user_id == user_id))
		return result

	async def get_received_messages_count_today(self, user_id: int):
		result = await self.session.scalar(
			select(func.count(Message.id)).where(and_(
				Message.to_user_id == user_id,
				func.date(Message.created_at) == date.today()
			)))

		return result

	async def get_sent_messages_count_today(self, user_id: int):
		result = await self.session.scalar(
			select(func.count(Message.id)).where(and_(
				Message.from_user_id == user_id,
				func.date(Message.created_at) == date.today()
			)))

		return result

	async def get_messages_new(self, current_page: int):
		result = await self.session.execute(
			select(Message.id, User.full_name)
			.select_from(Message)
			.join(User, User.id == Message.from_user_id)
			.offset(current_page * 8)
			.limit(8)
			.order_by(Message.id.desc())
		)

		result = result.fetchall() or None
		return result

	async def get_messages_old(self, current_page: int):
		result = await self.session.execute(
			select(Message.id, User.full_name)
			.select_from(Message)
			.join(User, User.id == Message.from_user_id)
			.offset(current_page * 8)
			.limit(8)
			.order_by(Message.id.asc())

		)

		result = result.fetchall() or None
		return result

	async def get_user_sent_messages(self, user_id: int):
		result = await self.session.execute(
			select(Message.id, User.full_name)
			.select_from(Message)
			.join(User, User.id == Message.to_user_id)
			.order_by(Message.id.desc())
			.where(Message.from_user_id == user_id)
			.limit(100)
		)
		return result.fetchall()

	async def get_user_sent_old_messages(self, user_id: int):
		result = await self.session.execute(
			select(Message.id, User.full_name)
			.select_from(Message)
			.join(User, User.id == Message.to_user_id)
			.order_by(Message.id.asc())
			.where(Message.from_user_id == user_id)
			.limit(100)
		)
		return result.fetchall()

	async def get_user_received_old_messages(self, user_id: int):
		result = await self.session.execute(
			select(Message.id, User.full_name)
			.select_from(Message)
			.join(User, User.id == Message.from_user_id)
			.order_by(Message.id.asc())
			.where(Message.to_user_id == user_id)
			.limit(100)
		)
		return result.fetchall()

	async def get_user_received_messages(self, user_id: int):
		result = await self.session.execute(
			select(Message.id, User.full_name)
			.select_from(Message)
			.join(User, User.id == Message.from_user_id)
			.order_by(Message.id.asc())
			.where(Message.to_user_id == user_id)
			.limit(100)
		)
		return result.fetchall()

	async def get_message_count(self):
		result = await self.session.scalar(select(func.count(Message.id)))
		return result