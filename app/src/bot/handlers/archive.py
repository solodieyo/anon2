from typing import Any

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import JOIN_TRANSITION, ChatMemberUpdatedFilter, LEAVE_TRANSITION
from aiogram.types import ChatMemberUpdated
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.src.infrastructure.database.repositories import GeneralRepository

router = Router(name=__name__)
router.my_chat_member.filter(F.chat.type == ChatType.PRIVATE)


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
@inject
async def enable_notifications(
	update: ChatMemberUpdated,
	repository: FromDishka[GeneralRepository]
) -> Any:
	await repository.user.unarchive_user(update.from_user.id)


@router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
@inject
async def disable_notifications(
	update: ChatMemberUpdated,
	repository: FromDishka[GeneralRepository]
) -> Any:
	await repository.user.archive_user(update.from_user.id)
