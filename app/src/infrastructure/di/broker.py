from dishka import Provider, provide, Scope
from taskiq_redis import RedisScheduleSource

redis_source = RedisScheduleSource("redis://localhost:6379/1")


class RedisSourceProvider(Provider):
	scope = Scope.APP

	@provide
	async def get_crypto_bot(self) -> RedisScheduleSource:
		return RedisScheduleSource("redis://localhost:6379/1")
