from typing import Optional

from aiogram.enums import ContentType
from sqlalchemy.orm import Mapped, mapped_column

from app.src.infrastructure.database.models.base import Base, Int16


class Media(Base):
	__tablename__ = 'media'

	id: Mapped[Int16] = mapped_column(primary_key=True, autoincrement=True)
	content_type: Mapped[ContentType]
	file_id: Mapped[str]
	file_name: Mapped[Optional[str]]

