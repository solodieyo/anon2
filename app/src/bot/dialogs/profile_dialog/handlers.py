import time
from datetime import datetime, UTC, timedelta

from aiocryptopay import AioCryptoPay
from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from redis.asyncio import Redis
from taskiq_redis import RedisScheduleSource

from app.src.bot.dialogs.factory.callback import UnblockCallbackData
from app.src.bot.senders import send_message, NewMessage
from app.src.bot.states.dialog_states import ProfileStates
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.models_dto import BlockedDTO
from app.src.infrastructure.database.repositories import GeneralRepository
from app.src.infrastructure.scheduler.tasks import delete_subscribe


@inject
async def on_input_new_hello_message(message: Message, widget: MessageInput, dialog_manager: DialogManager,
									 repository: FromDishka[GeneralRepository]):
	await repository.user.set_user_hello_message(user_id=message.from_user.id, text=message.text)
	await dialog_manager.switch_to(
		state=ProfileStates.change_hello,
		show_mode=ShowMode.DELETE_AND_SEND
	)


@inject
async def delete_user_hello_message(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager,
									repository: FromDishka[GeneralRepository]):
	await repository.user.set_user_hello_message(user_id=callback.from_user.id, text=None)


@inject
async def on_input_new_username(message: Message, widget: MessageInput, dialog_manager: DialogManager,
								repository: FromDishka[GeneralRepository]):
	exist_username = await repository.user.get_user_by_custom_username(custom_username=message.text)
	if exist_username:
		dialog_manager.dialog_data['exist_username'] = True
		await dialog_manager.switch_to(
			state=ProfileStates.create_username,
			show_mode=ShowMode.DELETE_AND_SEND,
		)
		return

	await repository.user.set_username(user_id=message.from_user.id, username=message.text)
	await dialog_manager.start(
		state=ProfileStates.settings,
		mode=StartMode.RESET_STACK,
		show_mode=ShowMode.DELETE_AND_SEND
	)


@inject
async def on_select_banned(
	callback: CallbackQuery,
	widget: Select,
	dialog_manager: DialogManager,
	selected_item: str,
	repository: FromDishka[GeneralRepository]
):
	i18n: I18nContext = dialog_manager.middleware_data["i18n"]
	bot: Bot = dialog_manager.middleware_data["bot"]
	blocked: BlockedDTO = await repository.blocked.get_blocked_message(
		blocked_id=int(selected_item),
	)

	keyboard = InlineKeyboardMarkup(
		inline_keyboard=[
			[InlineKeyboardButton(
				text=i18n.get('unblock-user-button'),
				callback_data=UnblockCallbackData(
					message_id=blocked.message.id,
					user_id=blocked.to_user.id,
					blocked_user_id=blocked.from_user.id,
					block_list=True
				).pack()
			)],
			[InlineKeyboardButton(
				text=i18n.get('delete'),
				callback_data="delete_message")
			]
		])

	await send_message(
		bot=bot,
		new_message=NewMessage(
			chat=callback.message.chat,
			text=i18n.get('message-text', message_text=blocked.message.message or ''),
			media=blocked.media.file_id if blocked.media else None,
			media_content_type=blocked.media.content_type if blocked.media else None,
			reply_markup=keyboard
		)
	)


@inject
async def on_delete_username(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository]
):
	await repository.user.set_username(
		user_id=dialog_manager.event.from_user.id,
		username=None
	)
	dialog_manager.middleware_data["user"].custom_username = None


@inject
async def change_tops_status(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository]
):
	show_in_tops = dialog_manager.middleware_data["user"].show_in_tops
	await repository.user.update_user_top_status(
		user_id=dialog_manager.event.from_user.id,
		status=not show_in_tops
	)
	dialog_manager.middleware_data["user"].show_in_tops = not show_in_tops


async def on_select_type_top(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
):
	dialog_manager.dialog_data['type_top'] = widget.widget_id


@inject
async def choice_premium_period(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	redis: FromDishka[Redis],
):
	user: User = dialog_manager.middleware_data['user']
	await redis.set(name=f'payment:payment_type:{user.user_id}', value=widget.widget_id)
	await dialog_manager.switch_to(state=ProfileStates.choice_pay)


@inject
async def delete_time(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	redis: FromDishka[Redis],
	repository: FromDishka[GeneralRepository],
):
	user: User = dialog_manager.middleware_data['user']
	payment_id = await redis.get(f"payment:payment_id:{user.user_id}")
	await repository.payments.cancel_payment(payment_id=int(payment_id))
	await redis.delete(f"payment:start_time:{user.user_id}")


@inject
async def change_show_status(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository]
):
	i18n: I18nContext = dialog_manager.middleware_data["i18n"]
	user: User = dialog_manager.middleware_data['user']

	if user.show_premium_username is None:
		user.show_premium_username = False
	else:
		user.show_premium_username = not user.show_premium_username

	await repository.user.update_premium_settings(
		user_id=user.user_id,
		value=user.show_premium_username
	)

	if not user.show_premium_username:
		await callback.answer(
			text=i18n.get('show-premium-username-callback-off'),
			show_alert=True
		)
	else:
		await callback.answer(
			text=i18n.get('show-premium-username-callback-on'),
			show_alert=True
		)

