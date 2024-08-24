import time

from aiocryptopay.models.update import Update
from aiogram import Bot
from aiogram_dialog import BgManagerFactory, StartMode
from dishka import AsyncContainer
from redis.asyncio import Redis
from taskiq_redis import RedisScheduleSource

from app.src.bot.handlers.payments.common import on_forever_payment, on_default_payment
from app.src.bot.states.dialog_states import ProfileStates
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository


async def invoice_paid(update: Update, app) -> None:

    dishka: AsyncContainer = app['dishka_container']
    redis_source: RedisScheduleSource = app['redis_source']
    bg: BgManagerFactory = app['bg']
    payment_id = int(update.payload.payload)
    async with dishka() as req_dishka:
        repository: GeneralRepository = await req_dishka.get(GeneralRepository)
        redis: Redis = await req_dishka.get(Redis)
        bot: Bot = await req_dishka.get(Bot)
        payment_type = await redis.get(f"payment:payment_type:{payment_id}")
        user_id = await redis.get(f"payment:user_id:{payment_id}")
        user_id = int(user_id)
        user: User = await repository.user.get_user_by_tg_id(user_id=user_id)
        start_payment_time = await redis.get(f"payment:start_time:{user_id}")
        total_payment_time = int(time.time()) - int(start_payment_time)

        if payment_type == 'premium_price_forever':
            await on_forever_payment(
                user_id=user_id,
                repository=repository,
                payment_id=int(payment_id),
                payment_time=total_payment_time
            )
        else:
            await on_default_payment(
                repository=repository,
                user=user,
                user_id=user_id,
                redis=redis,
                redis_source=redis_source,
                payment_type=payment_type,
                payment_time=total_payment_time
            )

    await bg.bg(
        bot=bot,
        chat_id=user_id,
        user_id=user_id
    ).start(state=ProfileStates.success_payed, mode=StartMode.RESET_STACK)


