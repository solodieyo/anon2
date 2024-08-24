from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from redis.asyncio import Redis

from app.src.enums import MailingStatus
from app.src.infrastructure.database.models import Mailing
from app.src.infrastructure.database.repositories import GeneralRepository


@inject
async def getter_mailing_info(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	redis: FromDishka[Redis],
	bot: Bot,
	**_
):
	active_mailing: Mailing = await repository.mailing.get_active_mailing()
	if not active_mailing:
		return {
			'active_mailing': False
		}

	success_sent = await redis.get('mailing:success_sent') or 0
	failed_sent = await redis.get('mailing:failed_sent') or 0

	return {
		'active_mailing': dialog_manager.dialog_data.get('active_mailing', True),
		'count_users': active_mailing.user_count,
		'success_sent': success_sent,
		'failed_sent': failed_sent,
		'mailing_id': active_mailing.id,
		'mailing_date': active_mailing.created_at.strftime("%d.%m.%Y %H:%M:%S"),
		"link": await create_start_link(bot=bot, payload=f"mailing_{active_mailing.id}"),
		"status": active_mailing.status,
		"finish_date": active_mailing.finish_date.strftime("%d.%m.%Y %H:%M:%S") if active_mailing.finish_date else 'no'
	}
