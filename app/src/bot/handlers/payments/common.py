import time

from redis.asyncio import Redis

from app.src.infrastructure.database.repositories import GeneralRepository


async def on_forever_payment(
	user_id: int,
	repository: GeneralRepository,
	redis: Redis
):
	payment_id = await redis.get(f"payment:payment_id:{user_id}")
	start_payment_time = await redis.get(f"payment:start_time:{user_id}")
	total_payment_time = int(time.time()) - int(start_payment_time)
	await repository.user.set_premium(user_id=user_id)
	await repository.payments.success_payment(
		payment_id=int(payment_id),
		payment_time=int(total_payment_time)
	)