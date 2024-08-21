from typing import cast, Union

from aiogram.types import Update
from aiogram_dialog.api.entities import DialogStartEvent, DialogUpdate
from aiogram_i18n import I18nMiddleware, I18nContext
from aiogram_i18n.cores import FluentRuntimeCore
from aiogram_i18n.managers import BaseManager
from dishka import Provider, provide, Scope, from_context, AsyncContainer

from app.src.config import AppConfig
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository


class HuyManager(BaseManager):
    async def get_locale(self, **kwargs) -> str:
        user: User = kwargs.get('user')
        if user is not None:
            locale = user.locale
        else:
            dishka: AsyncContainer = kwargs.get('dishka_container')
            async with dishka() as req_dishka:
                event: Union[Update, DialogUpdate] = kwargs.get('event')
                aiogd_update: DialogStartEvent = kwargs.get("aiogd_update")
                user_id = None

                if aiogd_update:
                    user_id = aiogd_update.from_user.id
                elif isinstance(event, Update) and event.message:
                    user_id = event.message.from_user.id
                elif isinstance(event, Update) and event.callback_query:
                    user_id = event.callback_query.from_user.id
                elif isinstance(event, DialogUpdate) and event.aiogd_update:
                    user_id = event.aiogd_update.from_user.id
                elif isinstance(event, Update) and event.pre_checkout_query:
                    user_id = event.pre_checkout_query.from_user.id
                repository: GeneralRepository = await req_dishka.get(GeneralRepository)
                if user_id:
                    locale = await repository.user.get_user_locale(user_id) or 'ru'
                else:
                    locale = 'ru'
        return cast(str, locale)

    async def set_locale(self, locale: str): pass


class I18nProvider(Provider):
    scope = Scope.APP

    config = from_context(AppConfig)

    @provide
    def get_middleware(self, config: AppConfig) -> I18nMiddleware:
        i18n_middleware = I18nMiddleware(
            core=FluentRuntimeCore(
                path=config.tg.locales_path,
            ),
            manager=HuyManager(),
        )
        return i18n_middleware

    @provide(scope=Scope.REQUEST)
    def get_context(self, middleware: I18nMiddleware) -> I18nContext:
        return middleware.new_context(locale="ru", data={})
