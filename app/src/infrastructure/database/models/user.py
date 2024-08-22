from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.src.enums import Roles, Locale
from app.src.infrastructure.database.models.base import Base, TimestampMixin, Int16, Int64


class User(Base, TimestampMixin):
	__tablename__ = 'users'

	id: Mapped[Int16] = mapped_column(primary_key=True)
	user_id: Mapped[Int64] = mapped_column(nullable=False)
	full_name: Mapped[str]
	username: Mapped[Optional[str]]
	custom_username: Mapped[Optional[str]]
	premium: Mapped[bool] = mapped_column(default=False)
	premium_date: Mapped[datetime] = mapped_column(nullable=True)
	rank: Mapped[Roles] = mapped_column(default=Roles.MEMBER)
	show_in_tops: Mapped[bool] = mapped_column(default=False)
	locale: Mapped[Locale] = mapped_column(default=Locale.RU)
	super_premium: Mapped[bool] = mapped_column(default=False)
	archive: Mapped[bool] = mapped_column(default=False)
	hello_message: Mapped[Optional[str]]
	referral_user_id: Mapped[Optional[Int64]]
	last_activity: Mapped[datetime] = mapped_column(nullable=True)
	show_premium_username: Mapped[bool] = mapped_column(default=True)
	count_send_message: Mapped[int] = mapped_column(default=0)
	count_received_message: Mapped[int] = mapped_column(default=0)