from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from app.src.config import AppConfig
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.models_dto.prices_dto import PricesDTO
from app.src.infrastructure.database.repositories import GeneralRepository


def get_premium_keyboard(
	config: AppConfig,
	i18n: I18nContext,
	user: User,
	repository: GeneralRepository,
	prices: PricesDTO,
):
	kb = InlineKeyboardBuilder()

	if user.premium and user.show_premium_username is None or user.premium and user.show_premium_username is True:
		kb.button(
			text=i18n.get('profile-premium-show-on'),
			callback_data='premium_username'
		)
	elif user.premium and user.show_premium_username is False:
		kb.button(
			text=i18n.get('profile-premium-show-off'),
			callback_data='premium_username'
		)
	if config.tg.premium_day:
		kb.button(
			text=i18n.get('day-premium-button', day_price=prices.price_day),
			callback_data='premium_price_day'
		)
	if config.tg.premium_week:
		kb.button(
			text=i18n.get('week-premium-button', week_price=prices.price_week),
			callback_data='premium_price_week'
		)

	if config.tg.premium_month:
		kb.button(
			text=i18n.get('month-premium-button', month_price=prices.price_month),
			callback_data='premium_price_forever'
		)

	if config.tg.premium_forever:
		kb.button(
			text=i18n.get('forever-premium-button', forever_price=prices.price_forever),
			callback_data='premium_forever'
		)
	kb.adjust(1)
	return kb.as_markup()