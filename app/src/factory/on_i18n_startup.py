from aiogram import Dispatcher
from aiogram_i18n import I18nMiddleware
from dishka import AsyncContainer

from app.src.infrastructure.database.models_dto.locales_dto import LocalesDTO
from app.src.infrastructure.database.repositories import GeneralRepository


async def on_i18n_startup(dispatcher: Dispatcher):
	i18n: I18nMiddleware = dispatcher['i18n_middleware']
	dishka: AsyncContainer = dispatcher['dishka_container']

	async with dishka() as req_dishka:
		repository = await req_dishka.get(GeneralRepository)
		languages: LocalesDTO = await repository.settings.get_language_status()
		for locale in languages.get_disabled():
			if locale is False:
				i18n.core.locales.pop(locale)