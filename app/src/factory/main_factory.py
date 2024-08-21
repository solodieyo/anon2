from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage, DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_i18n import I18nMiddleware
from dishka import (
    Provider,
    Scope,
    provide,
    make_async_container,
    AsyncContainer, from_context
)
from redis.asyncio import Redis

from app.src.bot.dialogs import dialog_setups
from app.src.config import load_config
from app.src.infrastructure.di import BotProvider, DbProvider
from app.src.bot.handlers import setup_routers
from app.src.config.app_config import AppConfig
from app.src.factory.setup_middleware import (
    _setup_outer_middleware,
    _setup_inner_middleware
)
from app.src.infrastructure.di.broker import RedisSourceProvider
from app.src.infrastructure.di.crypto import CryptoProvider
from app.src.infrastructure.di.i18n import I18nProvider


def create_dishka(config: AppConfig) -> AsyncContainer:
    container = make_async_container(*get_providers(), context={AppConfig: config})
    return container


def get_providers():
    return [
        DpProvider(),
        DbProvider(),
        BotProvider(),
        CryptoProvider(),
        RedisSourceProvider(),
        I18nProvider()
    ]


class DpProvider(Provider):
    scope = Scope.APP

    config = from_context(provides=AppConfig, scope=Scope.APP)

    @provide
    async def get_dispatcher(
            self,
            dishka: AsyncContainer,
            storage: BaseStorage,
            config: AppConfig,
            i18n_middleware: I18nMiddleware
    ) -> Dispatcher:
        dp = Dispatcher(
            storage=storage
        )

        dp.include_routers(setup_routers(), dialog_setups(dishka=dishka))
        _setup_outer_middleware(dispatcher=dp, dishka=dishka, config=config, i18n_middleware=i18n_middleware)
        _setup_inner_middleware(dispatcher=dp)

        return dp

    @provide(scope=Scope.APP)
    def get_redis(self, config: AppConfig) -> Redis:
        return Redis(
            host=config.redis.host,
            port=config.redis.port,
            decode_responses=True
        )

    @provide(scope=Scope.APP)
    def get_storage(self, redis: Redis) -> BaseStorage:
        return RedisStorage(
            redis=redis,
            key_builder=DefaultKeyBuilder(
                with_destiny=True,
                with_bot_id=True
            )
        )


def get_config() -> AppConfig:
    return load_config(AppConfig)


def get_dishka(config: AppConfig) -> AsyncContainer:
    return create_dishka(config)
