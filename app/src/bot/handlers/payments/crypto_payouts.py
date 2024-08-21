import time
from datetime import datetime, timedelta, UTC

from aiocryptopay.models.update import Update
from aiogram import Bot
from aiogram_dialog import BgManagerFactory, StartMode
from dishka import AsyncContainer
from redis.asyncio import Redis
from taskiq_redis import RedisScheduleSource

from app.src.bot.handlers.payments.common import on_forever_payment
from app.src.bot.states.dialog_states import ProfileStates
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository
from app.src.infrastructure.scheduler.tasks import delete_subscribe

days = {
    'premium_price_day': 1,
    'premium_price_week': 7,
    'premium_price_month': 30
}


async def invoice_paid(update: Update, app) -> None:

    dishka: AsyncContainer = app['dishka_container']
    redis_source: RedisScheduleSource = app['redis_source']
    bg: BgManagerFactory = app['bg']
    user_id = int(update.payload.payload)
    async with dishka() as req_dishka:
        repository: GeneralRepository = await req_dishka.get(GeneralRepository)
        redis: Redis = await req_dishka.get(Redis)
        bot: Bot = await req_dishka.get(Bot)
        payment_type = await redis.get(f"payment:payment_type:{user_id}")
        user: User = await repository.user.get_user_by_tg_id(user_id=user_id)

        if payment_type == 'premium_price_forever':
            await on_forever_payment(
                user_id=user_id,
                repository=repository,
                redis=redis
            )
        else:
            payment_id = await redis.get(f"payment:payment_id:{user_id}")
            start_payment_time = await redis.get(f"payment:start_time:{user_id}")
            total_payment_time = int(time.time()) - int(start_payment_time)
            await repository.payments.success_payment(
                payment_id=int(payment_id),
                payment_time=int(total_payment_time)
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
    await bg.bg(
        bot=bot,
        chat_id=user_id,
        user_id=user_id
    ).start(state=ProfileStates.success_payed, mode=StartMode.RESET_STACK)


