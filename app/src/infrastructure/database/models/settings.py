from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.src.infrastructure.database.models.base import Base


class Settings(Base):
	__tablename__ = 'settings'

	id: Mapped[int] = mapped_column(primary_key=True)
	premium_price_day_stars: Mapped[int] = mapped_column(default=1)
	premium_price_week_stars: Mapped[int] = mapped_column(default=1)
	premium_price_month_stars: Mapped[int] = mapped_column(default=1)
	premium_price_day_crypto: Mapped[int] = mapped_column(default=1)
	premium_price_week_crypto: Mapped[int] = mapped_column(default=1)
	premium_price_month_crypto: Mapped[int] = mapped_column(default=1)
	premium_price_forever_crypto: Mapped[int] = mapped_column(default=1)
	premium_price_forever_stars: Mapped[int] = mapped_column(default=1)
	locale_ru: Mapped[bool] = mapped_column(default=True)
	locale_en: Mapped[bool] = mapped_column(default=True)
	locale_de: Mapped[bool] = mapped_column(default=True)
	locale_uk: Mapped[bool] = mapped_column(default=True)
	start_picture: Mapped[Optional[str]]
