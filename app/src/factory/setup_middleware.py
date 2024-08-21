from aiogram import Dispatcher
from aiogram_album.lock_middleware import LockAlbumMiddleware
from aiogram_i18n import I18nMiddleware
from dishka import AsyncContainer

from app.src.bot.midllewares.last_activity import LastActivityMiddleware
from app.src.bot.midllewares.user_middleware import UserMiddleware
from app.src.config import AppConfig


def _setup_outer_middleware(
	dispatcher: Dispatcher,
	dishka: AsyncContainer,
	config: AppConfig,
	i18n_middleware: I18nMiddleware
) -> None:
	i18n_middleware.setup(dispatcher=dispatcher)
	dispatcher.message.outer_middleware(UserMiddleware(dishka=dishka, i18n_middleware=i18n_middleware))
	dispatcher.callback_query.outer_middleware(UserMiddleware(dishka=dishka, i18n_middleware=i18n_middleware))
	LockAlbumMiddleware(router=dispatcher)
	dispatcher.message.outer_middleware(LastActivityMiddleware(dishka=dishka))
	dispatcher.callback_query.outer_middleware(LastActivityMiddleware(dishka=dishka))


def _setup_inner_middleware(dispatcher: Dispatcher) -> None:
	pass
