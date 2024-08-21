from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from dishka.integrations.aiogram import inject, FromDishka
from aiogram_i18n import I18nContext

from app.src.bot.dialogs.common.trash import get_deep_link
from app.src.bot.keyboards.premium import get_premium_keyboard
from app.src.bot.utils.get_user_text import get_user_profile_text
from app.src.config import AppConfig
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.models_dto.prices_dto import PricesDTO
from app.src.infrastructure.database.repositories import GeneralRepository

router = Router()


@router.callback_query(F.data.startswith('user_faker_'))
@inject
async def message_answer(
	callback: CallbackQuery,
	i18n: I18nContext,
	bot: Bot,
	repository: FromDishka[GeneralRepository],
	config: FromDishka[AppConfig],
	user: User,
):
	from_user_id = callback.data.split('_')[2]
	from_user: User = await repository.user.get_user_by_tg_id(int(from_user_id))
	await callback.answer()

	if not user.premium:
		await premium_handler(
			callback=callback,
			bot=bot,
			i18n=i18n,
			user=user,
			config=config,
			repository=repository
		)
		return

	await bot.send_message(
		text=await get_user_profile_text(
			i18n=i18n,
			user=from_user,
			ask_user=user,
			repository=repository,
		),
		chat_id=callback.from_user.id,
		disable_web_page_preview=True,
		reply_markup=InlineKeyboardMarkup(
			inline_keyboard=[
				[
					InlineKeyboardButton(
						text=i18n.get('url-button'),
						url=await get_deep_link(
							user=from_user,
							bot=bot
						)
					)
				],
				[
					InlineKeyboardButton(
						text=i18n.get('delete'),
						callback_data='delete_message'
					)
				]
			]
		)
	)


@router.callback_query(F.data == 'faker')
@inject
async def faker_mailing(
	callback: CallbackQuery,
	i18n: I18nContext,
	user: User,
	bot: Bot,
	repository: FromDishka[GeneralRepository],
	config: FromDishka[AppConfig],
):
	await callback.answer()
	await premium_handler(
		callback=callback,
		bot=bot,
		i18n=i18n,
		user=user,
		config=config,
		repository=repository
	)


async def premium_handler(
	callback: CallbackQuery,
	bot: Bot,
	i18n: I18nContext,
	user: User,
	config: AppConfig,
	repository: GeneralRepository,
):
	if user.premium and user.premium_date:
		premium_active = user.premium_date
	elif user.premium and not user.premium_date:
		premium_active = 'adm'
	else:
		premium_active = 'no'

	text = i18n.get(
		'profile-premium',
		user.locale,
		premium_active=premium_active
	)
	prices: PricesDTO = await repository.settings.get_prices_stars()
	await bot.send_message(
		text=text,
		chat_id=callback.from_user.id,
		reply_markup=get_premium_keyboard(
			i18n=i18n, config=config,
			user=user,
			repository=repository,
			prices=prices
		)
	)