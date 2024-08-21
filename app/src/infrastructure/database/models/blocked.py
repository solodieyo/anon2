from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.src.infrastructure.database.models.base import Base, Int16, Int64, TimestampMixin


class Blocked(Base, TimestampMixin):
	__tablename__ = 'blocked'

	id: Mapped[Int16] = mapped_column(primary_key=True, autoincrement=True)

	user_id: Mapped[Int64] = mapped_column(
		ForeignKey('users.id', ondelete='CASCADE'),
		primary_key=True
	)
	blocked_user_id: Mapped[Int64] = mapped_column(
		ForeignKey('users.id', ondelete='CASCADE'),
		primary_key=True
	)

	message_id: Mapped[Int16] = mapped_column(
		ForeignKey('messages.id', ondelete='CASCADE'),
		primary_key=True
	)
