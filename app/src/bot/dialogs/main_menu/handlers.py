from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.bot.states.dialog_states import SendAnonMessagesStates, MainMenuStates
from app.src.infrastructure.database.repositories import GeneralRepository


@inject
async def choice_language(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager,
						  repository: FromDishka[GeneralRepository]):
	i18n: I18nContext = dialog_manager.middleware_data['i18n']

	await repository.user.set_user_locale(
		user_id=callback.from_user.id,
		locale=widget.widget_id
	)

	await i18n.set_locale(widget.widget_id)

	await dialog_manager.start(
		state=MainMenuStates.main_menu,
		show_mode=ShowMode.DELETE_AND_SEND,
		mode=StartMode.RESET_STACK
	)
