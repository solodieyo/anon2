from typing import AsyncIterable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from dishka import Scope, Provider, provide, from_context

from app.src.bot.midllewares.retry import RetryRequestMiddleware
from app.src.config.app_config import AppConfig


class BotProvider(Provider):
	scope = Scope.APP

	config = from_context(provides=AppConfig)

	@provide
	async def get_bot(self, config: AppConfig) -> AsyncIterable[Bot]:
		session: AiohttpSession = AiohttpSession()
		session.middleware(RetryRequestMiddleware())

		async with Bot(
			token=config.tg.token,
			default=DefaultBotProperties(parse_mode=ParseMode.HTML),
			session=session
		) as bot:
			yield bot