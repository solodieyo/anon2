import asyncio
from contextlib import suppress

import aiohttp
from aiocryptopay import AioCryptoPay
from aiogram import Bot, Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent
from aiohttp import web
from dishka.integrations.aiogram import setup_dishka as setup_dishka_aiogram

from app.src.bot.handlers.error import error_handler
from app.src.bot.handlers.payments.crypto_payouts import invoice_paid
from app.src.bot.senders.mailing.on_startup_bot import on_startup_mail
from app.src.factory.main_factory import get_config, get_dishka
from app.src.factory.on_i18n_startup import on_i18n_startup
from app.src.factory.set_commands import set_bot_commands
from app.src.factory.setup_log import setup_logging
from app.src.infrastructure.scheduler.broker import redis_source, broker
from app.src.infrastructure.scheduler.admin_tasks import admin_day_stats


async def main() -> None:
    await broker.startup()
    setup_logging()
    config = get_config()
    dishka = get_dishka(config)
    bot: Bot = await dishka.get(Bot)
    dp: Dispatcher = await dishka.get(Dispatcher)
    await set_bot_commands(bot)
    setup_dialogs(dp)

    try:
        setup_dishka_aiogram(router=dp, container=dishka)
        dp['dishka_container'] = dishka
        dp['redis_source'] = redis_source
        dp.startup.register(on_startup_mail)
        dp.startup.register(on_i18n_startup)
        dp.error.register(error_handler, ExceptionTypeFilter(UnknownIntent))
        await admin_day_stats.schedule_by_cron(
        	redis_source,
        	'1 15 * * *',
        )
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dishka.close()
        await broker.shutdown()


# async def main() -> aiohttp.web.Application:
#     await broker.startup()
#     setup_logging()
#     config = get_config()
#     dishka = get_dishka(config)
#     bot: Bot = await dishka.get(Bot)
#     dp: Dispatcher = await dishka.get(Dispatcher)
#     crypto: AioCryptoPay = await dishka.get(AioCryptoPay)
#     await set_bot_commands(bot)
#
#     bg = setup_dialogs(dp)
#     setup_dishka_aiogram(router=dp, container=dishka)
#
#     app = web.Application()
#     app['bg'] = bg
#     app['dishka_container'] = dishka
#     app['redis_source'] = redis_source
#     dp['dishka_container'] = dishka
#     dp['redis_source'] = redis_source
#     dp.startup.register(on_startup_mail)
#     dp.startup.register(on_i18n_startup)
#     dp.error.register(error_handler, ExceptionTypeFilter(UnknownIntent))
#     await admin_day_stats.schedule_by_cron(
#         redis_source,
#         '1 21 * * *',
#     )
#
#     await bot.delete_webhook(drop_pending_updates=True)
#     url = f"{config.webhook.base_webhook_url}{config.webhook.webhook_path}"
#     await bot.set_webhook(
#         url=url,
#         secret_token=config.webhook.webhook_secret
#     )
#
#     webhook_requests_handler = SimpleRequestHandler(
#         dispatcher=dp,
#         bot=bot,
#         secret_token=config.webhook.webhook_secret,
#     )
#     webhook_requests_handler.register(app, path=config.webhook.webhook_path)
#     app.add_routes([web.post(config.crypto.webhook_path, crypto.get_updates)])
#     crypto.register_pay_handler(invoice_paid)
#     setup_application(app, dp, bot=bot)
#
#     return app


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())


