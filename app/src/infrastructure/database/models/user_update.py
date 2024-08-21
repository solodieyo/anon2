from sqlalchemy.orm import Mapped, mapped_column

from app.src.enums import UserUpdate
from app.src.infrastructure.database.models import Base
from app.src.infrastructure.database.models.base import TimestampMixin, Int64


class UserUpdates(Base, TimestampMixin):
	__tablename__ = "user_updates"
	id: Mapped[int] = mapped_column(primary_key=True)
	user_id: Mapped[Int64] = mapped_column(nullable=False)
	before: Mapped[str] = mapped_column(nullable=True)
	after: Mapped[str] = mapped_column(nullable=True)
	update_type: Mapped[UserUpdate] = mapped_column(nullable=False)