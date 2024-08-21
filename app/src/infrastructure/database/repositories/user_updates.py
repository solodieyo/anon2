from sqlalchemy import update, func

from app.src.enums import UserUpdate
from app.src.infrastructure.database.models import UserUpdates, User
from app.src.infrastructure.database.repositories.base import BaseRepository


class UserUpdatesRepository(BaseRepository):

	async def update_username(self, before: str, after: str, user_id: int):
		new_update = UserUpdates(
			user_id=user_id,
			before=before,
			after=after,
			update_type=UserUpdate.username
		)
		self.session.add(new_update)
		await self.session.commit()

	async def update_full_name(self, before: str, after: str, user_id: int):
		new_update = UserUpdates(
			user_id=user_id,
			before=before,
			after=after,
			update_type=UserUpdate.full_name
		)
		self.session.add(new_update)
		await self.session.commit()

	async def update_last_activity(self, user_id: int):
		await self.session.execute(update(User).values(last_activity=func.now()).where(User.user_id == user_id))
		await self.session.commit()
