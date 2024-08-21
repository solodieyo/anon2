from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_i18n.context import I18nContext
from dishka.integrations.aiogram_dialog import inject
from dishka import FromDishka

from app.src.bot.dialogs.common.common_handlers import reply_anon_message
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository


@inject
async def on_input_anon_message(
	message: Message,
	widget: MessageInput,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository]
):
	i18n: I18nContext = dialog_manager.middleware_data['i18n']
	bot: Bot = dialog_manager.middleware_data['bot']
	to_user_id = dialog_manager.start_data["to_user_id"]
	from_user: User = dialog_manager.middleware_data['user']
	to_user: User = await repository.user.get_user_by_tg_id(user_id=to_user_id)

	await reply_anon_message(
		message=message,
		to_user=to_user,
		from_user=from_user,
		bot=bot,
		i18n=i18n,
		repository=repository,
		dialog_manager=dialog_manager
	)


async def cancel_sending(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
	await dialog_manager.done()
	await callback.message.delete()
