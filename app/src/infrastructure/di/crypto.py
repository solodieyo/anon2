from aiocryptopay import AioCryptoPay, Networks
from dishka import Provider, Scope, from_context, provide

from app.src.config import AppConfig


class CryptoProvider(Provider):
	scope = Scope.APP

	config = from_context(provides=AppConfig)

	@provide
	def get_crypto_bot(self, config: AppConfig) -> AioCryptoPay:
		crypto = AioCryptoPay(
			token=config.crypto.token,
			network=Networks.MAIN_NET
		)
		return crypto
