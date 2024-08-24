import time
from datetime import timedelta, datetime, UTC

from redis.asyncio import Redis
from taskiq_redis import RedisScheduleSource

from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository
from app.src.infrastructure.scheduler.tasks import delete_subscribe

days = {
	'premium_price_day': 1,
	'premium_price_week': 7,
	'premium_price_month': 30
}


async def on_forever_payment(
	user_id: int,
	repository: GeneralRepository,
	payment_id: int,
	payment_time: int
):
	await repository.user.set_premium(user_id=user_id)
	await repository.payments.success_payment(
		payment_id=int(payment_id),
		payment_time=payment_time
	)


async def on_default_payment(
	user_id: int,
	repository: GeneralRepository,
	redis: Redis,
	payment_type: str,
	payment_time: int,
	user: User,
	redis_source: RedisScheduleSource
):
	payment_id = await redis.get(f"payment:payment_id:{user_id}")
	await repository.payments.success_payment(
		payment_id=int(payment_id),
		payment_time=payment_time
	)
	if user.premium and user.premium_date:
		date = user.premium_date.date() + timedelta(days=days[payment_type])
		await repository.user.update_premium_date(user_id=user_id, date=date)
	else:
		await repository.user.set_premium(user_id=user_id, count_days=days[payment_type])
	await delete_subscribe.schedule_by_time(
		redis_source,
		datetime.now(UTC) + timedelta(days=days[payment_type]),
		user_id=user_id
	)
