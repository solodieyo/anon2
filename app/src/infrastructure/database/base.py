from sqlalchemy import URL, make_url
from sqlalchemy.ext.asyncio import (
	create_async_engine,
	AsyncEngine,
	AsyncSession,
	async_sessionmaker
)

from app.src.config import AppConfig


def create_pool(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
	return async_sessionmaker(engine, expire_on_commit=False)


def create_engine(config: AppConfig) -> AsyncEngine:
	return create_async_engine(config.postgres.build_dsn())
