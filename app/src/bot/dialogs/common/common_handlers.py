from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Select
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.bot.dialogs.common.trash import get_file_id
from app.src.bot.dialogs.common.widgets import get_message_keyboard
from app.src.bot.dialogs.factory.callback import ReceivedCallbackData, BlockedCallbackData
from app.src.bot.states.dialog_states import SendAnonMessagesStates
from app.src.infrastructure.database.models import Message as Message_, User, Blocked
from app.src.infrastructure.database.models_dto.message_dto import MessageDTO
from app.src.infrastructure.database.repositories import GeneralRepository
from app.src.bot.senders import NewMessage, send_message


@inject
async def on_show_message(
	callback: CallbackQuery,
	widget: Select, dialog_manager: DialogManager,
	selected_item: str,
	repository: FromDishka[GeneralRepository],
	bot: FromDishka[Bot]
):
	i18n: I18nContext = dialog_manager.middleware_data.get('i18n')
	message: MessageDTO = await repository.messages.get_message(int(selected_item))

	file_id = message.media.file_id if message.media else None
	content_type = message.media.content_type if message.media else None

	text = i18n.get(
		'message-admin-text',
		message_id=message.message.id,
		from_user_id=message.from_user.user_id,
		to_user_id=message.to_user.user_id,
		message_date=message.message.created_at,
		message_text=message.message.message or '',
		from_user=message.from_user.username or message.from_user.full_name,
		to_user=message.to_user.username or message.to_user.full_name
	)

	chat = await bot.get_chat(chat_id=dialog_manager.event.from_user.id)
	await send_message(
		bot=dialog_manager.middleware_data['bot'],
		new_message=NewMessage(
			chat=chat,
			text=text,
			reply_markup=get_message_keyboard(message),
			media=file_id,
			media_content_type=content_type

		)
	)


async def reply_anon_message(
	message: Message,
	to_user: User,
	from_user: User,
	dialog_manager: DialogManager,
	repository: GeneralRepository,
	i18n: I18nContext,
	bot: Bot
):
	blocked: Blocked = await repository.blocked.get_blocked(
		user_id=to_user.id,
		blocked_user_id=from_user.id
	)

	if not blocked:
		media_id, media_name = get_file_id(message)
		user_message: Message_ = await repository.messages.add_message(
			from_user_id=from_user.id,
			to_user_id=to_user.id,
			message=message.text or message.caption,
			content_type=message.content_type,
			media_id=media_id,
			media_name=media_name,
		)

		keyboard = InlineKeyboardMarkup(
			inline_keyboard=
			[
				[InlineKeyboardButton(
					text=i18n.get('block-user-button'),
					callback_data=BlockedCallbackData(
						from_user_id=from_user.id,
						message_id=user_message.id
					).pack()
				)],
				[InlineKeyboardButton(
					text=i18n.get('answer-message-button'),
					callback_data=ReceivedCallbackData(
						message_id=user_message.id,
						from_user_id=dialog_manager.event.from_user.id,
						to_user_id=to_user.id
					).pack()
				)],

			]
		)

		if to_user.premium:

			if from_user.custom_username:
				username = from_user.custom_username
			elif from_user.username:
				username = f"@{from_user.username}"
			else:
				username = from_user.full_name

			if not to_user.show_premium_username:
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

		chat = await bot.get_chat(chat_id=to_user.user_id)
		sent_message: Message = await send_message(
			bot=bot,
			new_message=NewMessage(
				chat=chat,
				text=i18n.get('new-message-text', message_text=user_message.message or ""),
				reply_markup=keyboard,
				media_content_type=message.content_type,
				media=media_id
			)
		)
		await repository.messages.add_message_id(
			message_id=user_message.id,
			tg_message_id=sent_message.message_id
		)
	await dialog_manager.start(
		state=SendAnonMessagesStates.success_send,
		data={"to_user_id": to_user.user_id},
		show_mode=ShowMode.DELETE_AND_SEND
	)


async def ignore(_, __, dialog_manager: DialogManager):
	dialog_manager.show_mode = ShowMode.NO_UPDATE
