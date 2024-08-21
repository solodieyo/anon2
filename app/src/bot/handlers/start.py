from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_i18n import I18nContext
from dishka import FromDishka, AsyncContainer
from dishka.integrations.aiogram import inject

from app.src.bot.dialogs.common.widgets import DELETE_KEYBOARD
from app.src.bot.filters.check_new_user import NewUserFilter
from app.src.bot.states.dialog_states import SendAnonMessagesStates, MainMenuStates
from app.src.infrastructure.database.models import User, Mailing
from app.src.infrastructure.database.repositories import GeneralRepository

router = Router()


@router.message(CommandStart(deep_link=True, magic=F.args.startswith("mailing")))
@inject
async def start_mailing(
	message: Message,
	dialog_manager: DialogManager,
	command: CommandObject,
	repository: FromDishka[GeneralRepository],
	i18n: I18nContext,
	bot: Bot
):
	mailing_id = command.args.split("_")[-1]
	mailing: Mailing = await repository.mailing.get_mailing_by_id(int(mailing_id))

	text = i18n.get(
		'broadcast-text',
		mailing_id=mailing.id,
		count_users=mailing.user_count,
		status=mailing.status,
		success_sent=mailing.success_sent,
		failed_sent=mailing.failed_sent,
		mailing_date=mailing.created_at.strftime("%d.%m.%Y %H:%M:%S"),
		finish_date=mailing.finish_date.strftime("%d.%m.%Y %H:%M:%S") if mailing.finish_date else 'no'
	)

	await bot.send_message(
		chat_id=message.from_user.id,
		text=text,
		reply_markup=DELETE_KEYBOARD
	)


@router.message(CommandStart(deep_link=True))
@inject
async def start_deep_link(
	message: Message,
	dialog_manager: DialogManager,
	command: CommandObject,
	repository: FromDishka[GeneralRepository],
	user: User,
	new_user: bool
):
	user_data = command.args
	from_user: User = await repository.user.get_user_start(user_data)
	if new_user:
		await repository.user.set_referral(user_id=user.user_id, referral_id=from_user.user_id)
	user.locale = from_user.locale
	dialog_manager.middleware_data["user"].locale = from_user.locale

	await repository.user.set_user_locale(
		user_id=dialog_manager.event.from_user.id,
		locale=from_user.locale
	)

	await dialog_manager.start(
		state=SendAnonMessagesStates.input_anon_msg,
		data={
			"from_user_id": message.from_user.id,
			"to_user_id": from_user.user_id,
		},
		mode=StartMode.RESET_STACK,
		show_mode=ShowMode.DELETE_AND_SEND
	)


@router.message(CommandStart(), NewUserFilter())
async def start_new_user(message: Message, dialog_manager: DialogManager):
	await dialog_manager.start(state=MainMenuStates.choice_language)


@router.message(CommandStart())
async def start_default(message: Message, dialog_manager: DialogManager):
	await dialog_manager.start(
		state=MainMenuStates.main_menu,
		show_mode=ShowMode.DELETE_AND_SEND,
		mode=StartMode.RESET_STACK
	)
