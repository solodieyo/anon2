from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.infrastructure.database.models_dto.locales_dto import LocalesDTO
from app.src.infrastructure.database.models_dto.prices_dto import PricesDTO
from app.src.infrastructure.database.repositories import GeneralRepository


@inject
async def getter_start_picture(repository: FromDishka[GeneralRepository], **_):
	start_picture = await repository.settings.get_start_picture()
	return {
		'start_picture': start_picture
	}


@inject
async def getter_lang_statuses(dialog_manager: DialogManager, repository: FromDishka[GeneralRepository], **_):
	languages: LocalesDTO = await repository.settings.get_language_status()
	dialog_manager.dialog_data.update(
		locale_en_status=languages.locale_en,
		locale_de_status=languages.locale_de,
		locale_uk_status=languages.locale_uk
	)

	data = {
		'en': languages.locale_en,
		'de': languages.locale_de,
		'uk': languages.locale_uk
	}
	return data


async def getter_language_confirm(dialog_manager: DialogManager, **_):
	languages_text = {
		'locale_en': 'Английский',
		'locale_de': 'Немецкий',
		'locale_uk': 'Украинский'
	}
	language = dialog_manager.dialog_data['language']
	language_state = dialog_manager.dialog_data[f"{language}_status"]

	return {
		'language': languages_text[language],
		"language_state": language_state
	}


@inject
async def getter_prices(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	**_
):
	prices_type = {
		"crypto": repository.settings.get_prices_crypto,
		'stars': repository.settings.get_prices_stars
	}
	prices: PricesDTO = await prices_type[dialog_manager.dialog_data['pay_type']]()

	return {
		'prices': prices
	}
