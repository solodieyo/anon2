from sqlalchemy import update, select

from app.src.enums import Locale
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.models.settings import Settings
from app.src.infrastructure.database.models_dto.locales_dto import LocalesDTO
from app.src.infrastructure.database.models_dto.prices_dto import PricesDTO
from app.src.infrastructure.database.repositories.base import BaseRepository


class SettingsRepository(BaseRepository):

	async def update_start_picture(self, file_id: str):
		await self.session.execute(update(Settings).where(Settings.id == 1).values(start_picture=file_id))
		await self.session.commit()

	async def get_start_picture(self):
		result = await self.session.scalar(select(Settings.start_picture).where(Settings.id == 1))
		return result

	async def delete_start_picture(self):
		await self.session.execute(update(Settings).where(Settings.id == 1).values(start_picture=None))
		await self.session.commit()

	async def update_price(self, date_type: str, price: int):
		await self.session.execute(update(Settings).where(Settings.id == 1).values({date_type: price}))
		await self.session.commit()

	async def get_language_status(self):
		result = await self.session.execute(
			select(Settings.locale_en, Settings.locale_de, Settings.locale_uk)
		)

		return LocalesDTO(*result.first())

	async def update_language_status(self, locale: str, status: bool):
		await self.session.execute(
			update(Settings)
			.values({locale: status})
			.where(Settings.id == 1)
		)

		if status is False:
			locales = {
				"locale_en": Locale.EN,
				"locale_de": Locale.DE,
				'locale_uk': Locale.UK
			}
			await self.session.execute(
				update(User)
				.values(locale=Locale.DEFAULT_LOCALE)
				.where(User.locale == locales[locale])
			)

		await self.session.commit()

	async def get_prices_stars(self):
		result = await self.session.execute(
			select(
				Settings.premium_price_day_stars,
				Settings.premium_price_week_stars,
				Settings.premium_price_month_stars,
				Settings.premium_price_forever_stars
			)
		)

		return PricesDTO(*result.first())

	async def get_prices_crypto(self):
		result = await self.session.execute(
			select(
				Settings.premium_price_day_crypto,
				Settings.premium_price_week_crypto,
				Settings.premium_price_month_crypto,
				Settings.premium_price_forever_crypto
			)
		)

		return PricesDTO(*result.first())

	async def get_price_by_type_stars(self, date_type: str):
		column_map = {
			'premium_price_day': Settings.premium_price_day_stars,
			'premium_price_week': Settings.premium_price_week_stars,
			'premium_price_month': Settings.premium_price_month_stars,
			'premium_price_forever': Settings.premium_price_forever_stars
		}
		result = await self.session.scalar(
			select(column_map[date_type])
		)

		return result

	async def get_price_by_type_crypto(self, payment_type):
		column_map = {
			'premium_price_day': Settings.premium_price_day_crypto,
			'premium_price_week': Settings.premium_price_week_crypto,
			'premium_price_month': Settings.premium_price_month_crypto,
			'premium_price_forever': Settings.premium_price_forever_crypto
		}
		result = await self.session.scalar(
			select(column_map[payment_type])
		)

		return result