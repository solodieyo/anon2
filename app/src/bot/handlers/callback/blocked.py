from aiogram import Router, Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.src.bot.dialogs.factory.callback import UnblockCallbackData, ReceivedCallbackData, BlockedCallbackData
from app.src.bot.states.dialog_states import ProfileStates
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository

router = Router()


@router.callback_query(UnblockCallbackData.filter())
@inject
async def unblock_user(
	callback: CallbackQuery,
	callback_data: UnblockCallbackData,
	repository: FromDishka[GeneralRepository],
	dialog_manager: DialogManager,
	user: User,
	i18n: I18nContext,
	bot: Bot
):
	await repository.blocked.unblock_user(
		user_id=callback_data.user_id,
		blocked_user_id=callback_data.blocked_user_id
	)

	if callback_data.block_list:
		await callback.message.delete()
		await bot.delete_message(chat_id=callback.from_user.id, message_id=dialog_manager.dialog_data['message_id'])
		await dialog_manager.start(
			state=ProfileStates.ban_list,
			mode=StartMode.RESET_STACK,
			show_mode=ShowMode.DELETE_AND_SEND
		)
		return

	from_user = await repository.user.get_user_by_id(user_pk=callback_data.blocked_user_id)
	keyboard = InlineKeyboardMarkup(inline_keyboard=
	[
		[InlineKeyboardButton(
			text=i18n.get('block-user-button'),
			callback_data=BlockedCallbackData(
				from_user_id=callback_data.blocked_user_id,
				message_id=callback_data.message_id
			).pack()
		)],
		[InlineKeyboardButton(
			text=i18n.get('answer-message-button'),
			callback_data=ReceivedCallbackData(
				message_id=callback_data.message_id,
				from_user_id=callback_data.user_id,
				to_user_id=callback_data.blocked_user_id
			).pack()
		)],
	]
	)

	if user.premium:
		if from_user.custom_username:
			username = from_user.custom_username
		elif from_user.username:
			username = f"@{from_user.username}"
		else:
			username = from_user.full_name

		if not user.show_premium_username:
			keyboard.inline_keyboard.insert(
				0, [InlineKeyboardButton(
					text=i18n.get("checker-sender-not-premium"),
					callback_data=f'user_faker_{from_user.user_id}'
				)], )
		else:
			keyboard.inline_keyboard.insert(
				0, [InlineKeyboardButton(
					text=i18n.get("checker-sender-premium", username=username),
					callback_data=f'user_faker_{from_user.user_id}'
				)], )
	else:
		keyboard.inline_keyboard.insert(
			0, [InlineKeyboardButton(
				text=i18n.get("checker-sender-not-premium"),
				callback_data=f'user_faker_{from_user.user_id}'
			)], )

	await callback.message.edit_reply_markup(reply_markup=keyboard)
