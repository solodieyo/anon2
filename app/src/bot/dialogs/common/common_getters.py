from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository


@inject
async def getter_count_messages(dialog_manager: DialogManager, repository: FromDishka[GeneralRepository], **_):
	user: User = dialog_manager.middleware_data['user']

	received_messages_count = await repository.messages.get_received_messages_count(user_id=user.id)
	sent_messages_count = await repository.messages.get_sent_messages_count(user_id=user.id)

	return {
		"received_messages_count": received_messages_count,
		"sent_messages_count": sent_messages_count
	}