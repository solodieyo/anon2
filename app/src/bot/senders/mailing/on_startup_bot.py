import asyncio

from aiogram import Bot, Dispatcher
from aiogram_i18n import I18nContext, I18nMiddleware
from redis.asyncio import Redis

from app.src.bot.senders.mailing.start_mailing import Broadcast
from app.src.infrastructure.database.repositories import GeneralRepository

TASKS = set()


async def on_startup_mail(
	dispatcher: Dispatcher,
):
	dishka = dispatcher.get("dishka_container")
	bot: Bot = await dishka.get(Bot)
	redis = await dishka.get(Redis)
	i18n: I18nMiddleware = dispatcher['i18n_middleware']

	async with dishka() as req_dishka:
		repository = await req_dishka.get(GeneralRepository)
		check_mail = await repository.mailing.get_active_mailing()

		if not check_mail:
			return

		start_from = await redis.get(name='mailing:last_user_id')

	task = asyncio.create_task(
		Broadcast(
			bot=bot,
			dishka=dishka,
			redis=redis,
			mailing_type=check_mail.mailing_type,
			mail_text=check_mail.text,
			file_ids=check_mail.media,
			content_type_media=check_mail.content_type_media,
			start_from=start_from if start_from else 0,
			i18n=i18n.new_context(data=dispatcher.workflow_data, locale='ru')
		).start_mailing()
	)

	TASKS.add(task)
