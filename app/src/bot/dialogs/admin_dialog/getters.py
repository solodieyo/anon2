from math import ceil

from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.infrastructure.database.models import Mailing
from app.src.infrastructure.database.models_dto import MessageDTO
from app.src.infrastructure.database.models_dto.statistic_dto import LanguageStatisticDTO, PreviewStatistic
from app.src.infrastructure.database.repositories import GeneralRepository


@inject
async def getter_main_admin_text(
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository], **_
) -> dict:
    statistic: PreviewStatistic = await repository.statistic.get_preview_statistic()
    return {
        "users_count": statistic.count_users,
        "messages_count": statistic.count_messages,
        "join_today": statistic.users_today,
        "message_today": statistic.message_today,
    }


@inject
async def getter_messages(
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository], **_
) -> dict:
    sort_type = dialog_manager.dialog_data.get("sort_type", True)
    message_count = await repository.messages.get_message_count()
    current_page = await dialog_manager.find("messages_scroll").get_page()

    if sort_type:
        result = await repository.messages.get_messages_new(current_page)
    else:
        result = await repository.messages.get_messages_old(current_page)
    return {
        'messages': result,
        'message_count': message_count,
        "sort_type": sort_type,
        'pages': ceil(message_count / 8),
        'current_page_': current_page + 1
    }


async def get_broadcast_content(
        dialog_manager: DialogManager,
        **_
):

    mail_group = dialog_manager.dialog_data.get("mail_group", 'all')
    faker = dialog_manager.dialog_data.get("faker", False)
    text = dialog_manager.dialog_data.get("text", '...')
    return {
        "faker": faker,
        "text": text,
        "mail_group": mail_group
    }


@inject
async def getter_previous_mailing(
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository], **_
):
    mailings = await repository.mailing.get_mailings()

    return {
        'mailings': mailings
    }


@inject
async def getter_message_content(
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository],
        i18n: I18nContext, **_
):
    message_id = dialog_manager.dialog_data.get("message_id")
    message: MessageDTO = await repository.messages.get_message(message_id)
    media = None

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

    if message.media:
        file_id = message.media.file_id
        content_type = message.media.content_type
        media = MediaAttachment(
            file_id=MediaId(file_id),
            type=content_type
        )

    return {
        'text': text,
        'media': media
    }


@inject
async def getter_previous_mailing_content(
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository],
        **_
):
    bot: Bot = dialog_manager.middleware_data['bot']
    mailing_id = dialog_manager.dialog_data['mailing_id']
    mailing_content: Mailing = await repository.mailing.get_mailing_by_id(mailing_id=mailing_id)
    link = await create_start_link(bot=bot, payload=f"mailing_{mailing_content.id}")

    return {
        "link": link,
        "count_users": mailing_content.user_count,
        "success_sent": mailing_content.success_sent,
        "failed_sent": mailing_content.failed_sent,
        "mailing_id": mailing_content.id,
        "mailing_date": mailing_content.created_at.strftime("%d.%m.%Y %H:%M:%S"),
        "status": mailing_content.status,
        "finish_date": mailing_content.finish_date.strftime(
            "%d.%m.%Y %H:%M:%S") if mailing_content.finish_date else 'no'
    }


async def get_mailing_group(
        dialog_manager: DialogManager,
        **_
):
    mail_group = dialog_manager.dialog_data.get("mail_group", 'all')
    return {
        "mail_group": mail_group
    }