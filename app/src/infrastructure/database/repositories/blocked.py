from sqlalchemy import delete, and_, select
from aiogram_i18n import I18nContext

from app.src.infrastructure.database.models import User, Message, Media
from app.src.infrastructure.database.models.blocked import Blocked
from app.src.infrastructure.database.models_dto import BlockedDTO
from app.src.infrastructure.database.models_dto.ban_list_dto import BanListDTO
from app.src.infrastructure.database.repositories.base import BaseRepository


class BlockedRepository(BaseRepository):

	async def block_user(self, user_id: int, blocked_user_id: int, message_id: int):
		blocked = Blocked(
			user_id=user_id,
			blocked_user_id=blocked_user_id,
			message_id=message_id
		)
		self.session.add(blocked)
		await self.session.commit()

	async def unblock_user(self, user_id: int, blocked_user_id: int):
		await self.session.execute(
			delete(Blocked).where(and_(Blocked.user_id == user_id, Blocked.blocked_user_id == blocked_user_id))
		)
		await self.session.commit()

	async def get_user_ban_list(self, user_id: int, i18n: I18nContext):
		query = await self.session.execute(
			select(
				Blocked.message_id.label('message_id'),
				Message.message.label('text'),
				Message.media_id.label('media_id')
			)
			.select_from(Blocked)
			.join(Message, Blocked.message_id == Message.id)
			.where(Blocked.user_id == user_id)
		)

		result = []
		for message in query.fetchall():
			media = await self.session.scalar(
				select(Media)
				.where(Media.id == message.media_id)
			)
			result.append(
				BanListDTO(
					message_id=message.message_id,
					text=message.text,
					content_type=i18n.get(
						'ban-list-content-type',
						content_type=media.content_type
					) if media else " "
				)
			)

		return result

	async def get_blocked_message(self, blocked_id: int):
		blocked: Blocked | None = await self.session.scalar(
			select(Blocked)
			.where(Blocked.message_id == blocked_id)
		)
		message = await self.session.scalar(
			select(Message)
			.where(Message.id == blocked.message_id)
		)

		from_user = await self.session.scalar(
			select(User)
			.where(User.id == blocked.blocked_user_id)
		)

		to_user = await self.session.scalar(
			select(User)
			.where(User.id == blocked.user_id)
		)

		media = await self.session.scalar(
			select(Media)
			.where(Media.id == message.media_id)
		)

		return BlockedDTO(
			from_user=from_user,
			to_user=to_user,
			message=message,
			media=media
		)

	async def get_blocked(self, user_id: int, blocked_user_id: int):
		blocked: Blocked | None = await self.session.scalar(
			select(Blocked)
			.where(and_(Blocked.user_id == user_id, Blocked.blocked_user_id == blocked_user_id))
		)

		return blocked
