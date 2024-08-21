from dataclasses import dataclass

from sqlalchemy import URL


LOCALES_PATH = ''
CONFIG_PATH = r"/home/solo/PycharmProjects/anontg2/config.toml"


@dataclass
class Tg:
	token: str
	admin_id: int
	support_username: str
	locales_path: str
	premium_day: bool
	premium_week: bool
	premium_month: bool
	premium_forever: bool


@dataclass
class Webhook:
	web_server_host: str
	web_server_port: int
	webhook_path: str
	webhook_secret: str
	base_webhook_url: str


@dataclass
class Postgres:
	database: str
	user: str
	password: str
	host: str
	port: int

	def build_dsn(self) -> URL:
		return URL.create(
			drivername="postgresql+asyncpg",
			username=self.user,
			password=self.password,
			host=self.host,
			port=self.port,
			database=self.database,
		)


@dataclass
class Redis:
	host: str
	port: int


@dataclass
class Crypto:
	token: str
	webhook_path: str


@dataclass
class AppConfig:
	tg: Tg
	postgres: Postgres
	redis: Redis
	crypto: Crypto
	webhook: Webhook

