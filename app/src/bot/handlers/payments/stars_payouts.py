from datetime import datetime, UTC, timedelta
from time import time

from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from redis.asyncio import Redis
from taskiq_redis import RedisScheduleSource

from app.src.bot.handlers.payments.common import on_forever_payment
from app.src.bot.states.dialog_states import ProfileStates
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository
from app.src.infrastructure.scheduler.tasks import delete_subscribe

router = Router()


@router.pre_checkout_query()
async def on_pre_checkout_query(query):
	await query.answer(ok=True)


@router.message(F.successful_payment)
@inject
async def on_successful_payment(
	message: Message,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	redis: FromDishka[Redis],
	redis_source: RedisScheduleSource,
	user: User
):

	payment_type = await redis.get(f"payment:payment_type:{user.user_id}")
	if payment_type == 'premium_price_forever':
		await on_forever_payment(
			user_id=message.from_user.id,
			repository=repository,
			redis=redis
		)
	else:
		days = {
			'premium_price_day': 1,
			'premium_price_week': 7,
			'premium_price_month': 30
		}
		start_payment_time = await redis.get(f"payment:start_time:{user.user_id}")
		total_payment_time = int(time()) - int(start_payment_time)
		payment_id = await redis.get(f"payment:payment_id:{user.user_id}")

		await repository.payments.success_payment(
			payment_id=int(payment_id),
			payment_time=total_payment_time
		)

		if user.premium and user.premium_date:
			date = user.premium_date.date() + timedelta(days=days[payment_type])
			await repository.user.update_premium_date(user_id=message.from_user.id, date=date)
		else:
			await repository.user.set_premium(user_id=message.from_user.id, count_days=days[payment_type])
		await delete_subscribe.schedule_by_time(
			redis_source,
			datetime.now(UTC) + timedelta(days=days[payment_type]),
			user_id=message.from_user.id
		)
	await dialog_manager.start(
		state=ProfileStates.success_payed,
		mode=StartMode.RESET_STACK,
		show_mode=ShowMode.DELETE_AND_SEND
	)