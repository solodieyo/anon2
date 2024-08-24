import asyncio
import logging

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import (
    InputMediaAnimation,
    InputMediaDocument,
    InputMediaAudio,
    InputMediaPhoto,
    InputMediaVideo, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram_i18n import I18nContext
from dishka import AsyncContainer
from redis.asyncio import Redis

from app.src.infrastructure.database.repositories import GeneralRepository
from .. import NewMessage
from ..any_message import send_message
from app.src.enums import MailingType, MailingStatus
from ...dialogs.common.trash import get_content_types

INPUT_MEDIA_TYPES = {
    ContentType.ANIMATION: InputMediaAnimation,
    ContentType.DOCUMENT: InputMediaDocument,
    ContentType.AUDIO: InputMediaAudio,
    ContentType.VIDEO: InputMediaVideo,
    ContentType.PHOTO: InputMediaPhoto,
}

logger = logging.getLogger(__name__)


class Broadcast:

    def __init__(
            self,
            bot: Bot,
            dishka: AsyncContainer,
            redis: Redis,
            mailing_type: MailingType,
            mail_text: str,
            file_ids: list[str],
            content_type_media: list[str],
            start_from: int = 0,
            faker: bool = False,
            i18n: I18nContext = None
    ):
        self.bot = bot
        self.redis = redis
        self.dishka = dishka
        self.mailing_type = mailing_type
        self.mail_text = mail_text
        self.file_ids = file_ids
        self.content_type_media = content_type_media
        self.start_from = start_from
        self.users_ids = []
        self.faker = faker
        self.i18n = i18n

    async def start_mailing(self):
        await self.redis.set('mailing:active_mailing', 'y')
        await self._get_users()
        if len(self.file_ids) > 1:
            await self._start_album_mailing()
        else:
            await self._start_mailing()

    async def _start_album_mailing(self):
        sleep_duration = 0.25 if len(self.file_ids) == 10 else 0.2

        medias = [INPUT_MEDIA_TYPES[get_content_types(content_type)](media=file_id) for file_id, content_type in
                  zip(self.file_ids, self.content_type_media)]
        medias[0].caption = self.mail_text

        await self.redis.set(name='success_sent', value=0)
        await self.redis.set(name='failed_sent', value=0)

        for user_id in self.users_ids:
            user_id = user_id[0]
            cancel = await self.redis.get('mailing:cancel')
            if cancel == 'y':
                await self._end_mailing(status=MailingStatus.FAILED)
                return
            try:
                await self.bot.send_media_group(
                    chat_id=user_id,
                    media=medias,
                )
                await self.redis.incrby(name='mailing:success_sent', amount=1)
                await self.redis.set(name='mailing:last_user_id', value=user_id)
                await asyncio.sleep(sleep_duration)

            except Exception as e:
                logger.error(e)
                await asyncio.sleep(sleep_duration)
                await self.redis.set(name='mailing:last_user_id', value=user_id)
                await self.redis.incrby(name='mailing:failed_sent', amount=1)
        await self._end_mailing(status=MailingStatus.FINISH)

    async def _start_mailing(self):
        await self.redis.set(name='mailing:success_sent', value=0)
        await self.redis.set(name='mailing:failed_sent', value=0)

        for user_id in self.users_ids:
            if self.faker:
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(
                            text=self.i18n.get('checker-sender-not-premium', user_id[1]),
                            callback_data='faker'
                        )]
                    ]
                )
            else:
                keyboard = None
            user_id = user_id[0]
            cancel = await self.redis.get('mailing:cancel')
            if cancel == 'y':
                await self._end_mailing(status=MailingStatus.FAILED)
                return
            chat = await self.bot.get_chat(user_id)
            try:
                await send_message(
                    bot=self.bot,
                    new_message=NewMessage(
                        text=self.mail_text,
                        chat=chat,
                        reply_markup=keyboard,
                        media=self.file_ids[0][0],
                        media_content_type=get_content_types(self.content_type_media[0])
                    )
                )

                await self.redis.incrby(name='mailing:success_sent', amount=1)
                await self.redis.set(name='mailing:last_user_id', value=user_id)
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(e)
                await asyncio.sleep(0.09)
                await self.redis.incrby(name='mailing:failed_sent', amount=1)
                await self.redis.set(name='mailing:last_user_id', value=user_id)
        await self._end_mailing(status=MailingStatus.FINISH)

    async def _get_users(self):
        async with self.dishka() as req_dishka:
            repository = await req_dishka.get(GeneralRepository)
            if self.faker:
                self.mailing_type = MailingType.DEFAULT
            self.users_ids = await repository.mailing.get_users(
                self.mailing_type,
                start_from=int(self.start_from)
            )

    async def _end_mailing(self, status: MailingStatus):
        success_sent = await self.redis.get('mailing:success_sent') or 0
        failed_sent = await self.redis.get('mailing:failed_sent') or 0

        async with self.dishka() as req_dishka:
            repository = await req_dishka.get(GeneralRepository)
            await repository.mailing.finish_mailing(
                int(success_sent),
                int(failed_sent),
                status
            )

        await self.redis.delete('mailing:cancel')
        await self.redis.delete('mailing:last_user_id')
        await self.redis.delete('mailing:success_sent')
        await self.redis.delete('mailing:failed_sent')
