from aiogram import Bot
from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.bot.dialogs.common.trash import get_deep_link
from app.src.config import AppConfig
from app.src.enums import Roles
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.models_dto.locales_dto import LocalesDTO
from app.src.infrastructure.database.repositories import GeneralRepository


async def getter_main_menu_text(dialog_manager: DialogManager, bot: Bot, **_):
	user: User = dialog_manager.middleware_data['user']

	return {
		"link": await get_deep_link(
			user=user,
			bot=bot
		)
	}


@inject
async def getter_start_picture(dialog_manager: DialogManager, repository: FromDishka[GeneralRepository], **_):
	image = None
	file_id = await repository.settings.get_start_picture()
	if file_id:
		image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(file_id))

	return {
		"start_photo": image
	}


@inject
async def admin_getter(
	dialog_manager: DialogManager,
	user: User,
	config: FromDishka[AppConfig],
	**_):
	return {
		"is_admin": user.rank == Roles.ADMIN or user.user_id == config.tg.admin_id
	}


@inject
async def getter_languages_statuses(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	**_
):
	languages: LocalesDTO = await repository.settings.get_language_status()
	return {
		"en": languages.locale_en,
		"de": languages.locale_de,
		"uk": languages.locale_uk
	}
