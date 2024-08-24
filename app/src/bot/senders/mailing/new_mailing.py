import asyncio
from datetime import datetime, timedelta
from typing import Optional

from aiogram import Bot
from aiogram_i18n import I18nContext
from dishka import AsyncContainer
from redis.asyncio import Redis

from app.src.bot.senders.mailing.start_mailing import Broadcast
from app.src.enums import MailingType
from app.src.infrastructure.database.repositories import GeneralRepository

TASKS = set()


async def create_new_mailing(
        bot: Bot,
        text: Optional[str],
        dishka: AsyncContainer,
        mailing_type: MailingType,
        file_ids: Optional[list[str]],
        content_type_media: Optional[list[str]],
        faker: Optional[bool] = False,
        i18n: Optional[I18nContext] = None
):
    redis: Redis = await dishka.get(Redis)
    async with dishka() as req_dishka:
        repository = await req_dishka.get(GeneralRepository)

        count_users = await repository.mailing.get_count_users_for_mailing(mailing_type=mailing_type)
        time_broadcast = count_users * 0.15
        await repository.mailing.create_mailing(
            text=text,
            mailing_type=mailing_type,
            user_count=count_users,
            content_type_media=content_type_media,
            media=file_ids,
            finish_date=datetime.now() + timedelta(seconds=time_broadcast),
        )

    task = asyncio.create_task(
        Broadcast(
            bot=bot,
            dishka=dishka,
            redis=redis,
            mailing_type=mailing_type,
            mail_text=text,
            file_ids=file_ids,
            content_type_media=content_type_media,
            faker=faker,
            i18n=i18n
        ).start_mailing()
    )

    TASKS.add(task)
