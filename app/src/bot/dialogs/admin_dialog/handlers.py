from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.bot.states.dialog_states import AdminStates, AdminUsersStates
from app.src.infrastructure.database.models_dto import MessageDTO
from app.src.infrastructure.database.repositories import GeneralRepository


async def on_change_sort(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
):
	sort_type = dialog_manager.dialog_data.get("sort_type", True)
	dialog_manager.dialog_data["sort_type"] = not sort_type


async def on_select_message(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	selected_item: int
):
	dialog_manager.dialog_data["message_id"] = selected_item
	await dialog_manager.switch_to(AdminStates.show_message_content)


@inject
async def on_sender(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository]
):
	message_id = dialog_manager.dialog_data["message_id"]
	message: MessageDTO = await repository.messages.get_message(message_id)
	await dialog_manager.start(
		state=AdminUsersStates.manage_user,
		data={"user_id": message.from_user.user_id}
	)


@inject
async def on_receiver(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository]
):
	message_id = dialog_manager.dialog_data["message_id"]
	message: MessageDTO = await repository.messages.get_message(message_id)
	await dialog_manager.start(
		state=AdminUsersStates.manage_user,
		data={"user_id": message.to_user.user_id}
	)
