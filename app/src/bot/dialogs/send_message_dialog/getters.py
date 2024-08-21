from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository


@inject
async def getter_user_status(dialog_manager: DialogManager, repository: FromDishka[GeneralRepository], **_):
	status = await repository.user.get_user_status(user_id=dialog_manager.event.from_user.id)
	return {
		"status": status
	}


@inject
async def getter_user_status(dialog_manager: DialogManager, repository: FromDishka[GeneralRepository], **_):
	status = await repository.user.get_user_status()
	return {
		"premium": status
	}


@inject
async def start_hello_message(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	i18n: I18nContext,
	user: User, **_
):
	to_user_id = dialog_manager.start_data["to_user_id"]
	message = await repository.user.get_hello_message(user_id=to_user_id)
	text_back = i18n.get(
		'delete',
		user.locale
	)
	text = i18n.get(
		'input-anon-msg',
		user.locale,
		hello_message=f"{message}" if message else "no"
	)
	return {
		"text": text,
		'text_back': text_back
	}
