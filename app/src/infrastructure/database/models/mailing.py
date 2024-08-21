from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import array, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.src.enums import MailingStatus, MailingType
from ..models.base import TimestampMixin, Base, Int16, Int64


class Mailing(Base, TimestampMixin):
	__tablename__ = "mailing"

	id: Mapped[Int16] = mapped_column(primary_key=True, autoincrement=True)
	status: Mapped[MailingStatus] = mapped_column(default=MailingStatus.PENDING)
	mailing_type: Mapped[MailingType]
	user_count: Mapped[Int64] = mapped_column(default=0)
	success_sent: Mapped[Int64] = mapped_column(default=0)
	failed_sent: Mapped[Int64] = mapped_column(default=0)
	text: Mapped[Optional[str]]
	content_type_media = mapped_column(ARRAY(String), nullable=True)
	media = mapped_column(ARRAY(String), nullable=True)
	finish_date: Mapped[Optional[datetime]]
