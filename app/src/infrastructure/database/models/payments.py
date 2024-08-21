from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.src.enums import Locale, PaymentType, PaymentsStatus
from app.src.infrastructure.database.models.base import Base, TimestampMixin, Int16, Int64


class Payments(Base, TimestampMixin):
	__tablename__ = 'payments'

	id: Mapped[Int16] = mapped_column(primary_key=True)
	user_id: Mapped[Int64] = mapped_column(ForeignKey('users.id'))
	amount: Mapped[Int64]
	status: Mapped[PaymentsStatus]
	payment_type: Mapped[PaymentType]
	locale_payed: Mapped[Locale]
	payments_time: Mapped[Optional[int]]
