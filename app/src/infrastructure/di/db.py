from typing import AsyncIterable

from dishka import Provider, Scope, provide, from_context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncEngine

from app.src.config.app_config import AppConfig
from app.src.infrastructure.database.base import create_pool, create_engine
from app.src.infrastructure.database.repositories import GeneralRepository


class DbProvider(Provider):
	scope = Scope.APP

	config = from_context(provides=AppConfig, scope=Scope.APP)

	@provide
	async def get_engine(self, config: AppConfig) -> AsyncIterable[AsyncEngine]:
		engine = create_engine(config)
		yield engine
		await engine.dispose(True)

	@provide
	def get_pool(self, engine: AsyncEngine) -> async_sessionmaker:
		return create_pool(engine)

	@provide(scope=Scope.REQUEST)
	async def get_session(self, pool: async_sessionmaker) -> AsyncIterable[AsyncSession]:
		async with pool() as session_pool:
			yield session_pool

	@provide(scope=Scope.REQUEST)
	async def get_db(self, session: AsyncSession) -> GeneralRepository:
		return GeneralRepository(session=session)
