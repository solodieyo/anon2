from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_i18n import I18nContext
from redis.asyncio import Redis
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.src.bot.keyboards.premium import get_premium_keyboard
from app.src.bot.states.dialog_states import ProfileStates
from app.src.config import AppConfig
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.models_dto.prices_dto import PricesDTO
from app.src.infrastructure.database.repositories import GeneralRepository

router = Router()


@router.callback_query(F.data == 'premium_username')
@inject
async def premium_username(
	callback: CallbackQuery,
	repository: FromDishka[GeneralRepository],
	user: User,
	i18n: I18nContext,
	config: FromDishka[AppConfig]
):
	if user.show_premium_username is None:
		user.show_premium_username = False
	else:
		user.show_premium_username = not user.show_premium_username

	await repository.user.update_premium_settings(
		user_id=user.user_id,
		value=user.show_premium_username
	)

	if user.show_premium_username:
		key = 'show-premium-username-callback-on'
	else:
		key = 'show-premium-username-callback-off'
	await callback.answer(
		text=i18n.get(
			key
		),
		show_alert=True
	)
	prices: PricesDTO = await repository.settings.get_prices_stars()
	await callback.message.edit_reply_markup(
		reply_markup=get_premium_keyboard(
			i18n=i18n,
			config=config,
			user=user,
			repository=repository,
			prices=prices
		)
	)


@router.callback_query(F.data == 'premium_price_day')
@router.callback_query(F.data == 'premium_price_week')
@router.callback_query(F.data == 'premium_price_month')
@router.callback_query(F.data == 'premium_price_forever')
@inject
async def premium_date_handler(
	callback: CallbackQuery,
	dialog_manager: DialogManager,
	redis: FromDishka[Redis],
	user: User
):
	await redis.set(name=f'payment:payment_type:{user.user_id}', value=callback.data)
	await dialog_manager.start(
		ProfileStates.choice_pay,
		mode=StartMode.RESET_STACK,
		show_mode=ShowMode.EDIT,
	)


@router.message(Command('premium'))
@router.callback_query(F.data == 'start_prem')
async def prem_test(callback: CallbackQuery, dialog_manager: DialogManager):
	await dialog_manager.start(
		ProfileStates.premium,
		mode=StartMode.RESET_STACK,
		show_mode=ShowMode.DELETE_AND_SEND,
		data={'command': True}
	)
