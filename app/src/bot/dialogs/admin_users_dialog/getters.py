from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from aiogram_i18n import I18nContext
from aiogram import Bot

from app.src.bot.dialogs.common.trash import get_deep_link
from app.src.bot.utils.get_user_text import get_user_profile_text
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.models_dto.statistic_dto import UsersStatisticDTO, UserMessageStatisticDTO
from app.src.infrastructure.database.repositories import GeneralRepository

PLACES = {
	1: "🥇",
	2: "🥈",
	3: "🥉",
	5: '🏆',
	6: '🏆',
	7: '🏆',
	8: '🏆',
	9: '🏆',
	10: '🏆'
}


@inject
async def getter_admin_user_text(
	repository: FromDishka[GeneralRepository], **_
):
	users_statistic: UsersStatisticDTO = await repository.statistic.get_users_statistic()
	return {
		"users_count": users_statistic.users_count,
		"ru_total_users": users_statistic.ru_count,
		"ua_total_users": users_statistic.ua_count,
		"en_total_users": users_statistic.en_count,
		"de_total_users": users_statistic.de_count,
		"ru_percent": users_statistic.ru_percent,
		"ua_percent": users_statistic.ua_percent,
		"en_percent": users_statistic.en_percent,
		"de_percent": users_statistic.de_percent
	}


@inject
async def getter_user_info(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	i18n: I18nContext,
	bot: Bot,
	user: User,
	**_
):
	if dialog_manager.start_data:
		user_id = dialog_manager.start_data.get('user_id')
		dialog_manager.dialog_data['show_user'] = user_id
		cancel = True
	else:
		user_id = dialog_manager.dialog_data['show_user']
		cancel = False

	from_user: User = await repository.user.get_user_by_tg_id(user_id=user_id)

	text = await get_user_profile_text(
		i18n=i18n,
		user=from_user,
		ask_user=user,
		repository=repository,
		admin=True
	)

	return {
		"text": text,
		"cancel": cancel,
		"url_link": await get_deep_link(
			user=user,
			bot=bot
		)
	}


@inject
async def getter_user_sent_messages(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository], **_
):
	user_id = dialog_manager.dialog_data['show_user']
	user: User = await repository.user.get_user_by_tg_id(user_id=user_id)
	sort_type = dialog_manager.dialog_data.get("sort_type", True)

	if sort_type:
		messages = await repository.messages.get_user_sent_messages(user_id=user.id)
	else:
		messages = await repository.messages.get_user_sent_old_messages(user_id=user.id)

	return {
		"messages": messages,
		"sort_type": sort_type
	}


@inject
async def getter_user_received_messages(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	**_
):
	user_id = dialog_manager.dialog_data['show_user']
	user: User = await repository.user.get_user_by_tg_id(user_id=user_id)
	sort_type = dialog_manager.dialog_data.get("sort_type", True)

	if sort_type:
		messages = await repository.messages.get_user_received_messages(user_id=user.id)
	else:
		messages = await repository.messages.get_user_received_old_messages(user_id=user.id)

	return {
		"messages": messages,
		"sort_type": sort_type
	}
