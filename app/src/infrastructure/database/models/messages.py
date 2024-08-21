from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.src.infrastructure.database.models.base import Base, TimestampMixin, Int16, Int64


class Message(Base, TimestampMixin):
	__tablename__ = 'messages'

	id: Mapped[Int16] = mapped_column(primary_key=True, autoincrement=True)
	message: Mapped[Optional[str]]
	from_user_id: Mapped[Int64] = mapped_column(ForeignKey('users.id'))
	to_user_id: Mapped[Int64] = mapped_column(ForeignKey('users.id'))
	media_id: Mapped[Optional[Int16]] = mapped_column(ForeignKey('media.id'))
