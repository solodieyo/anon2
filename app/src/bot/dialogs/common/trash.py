from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link

from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.models.messages import Message as Message_
from app.src.infrastructure.database.repositories import GeneralRepository


def get_album_file_ids(message: Message):
	if message.photo:
		return message.photo[-1].file_id
	elif message.photo:
		return message.photo[-1].file_id
	elif message.audio:
		return message.audio.file_id
	elif message.video:
		return message.video.file_id


def get_file_id(message: Message):
	if message.voice:
		return message.voice.file_id, None
	elif message.photo:
		return message.photo[-1].file_id, None
	elif message.sticker:
		return message.sticker.file_id, None
	elif message.document:
		return message.document.file_id, message.document.file_name
	elif message.video_note:
		return message.video_note.file_id, None
	elif message.audio:
		return message.audio.file_id, message.audio.file_name
	elif message.video:
		return message.video.file_id, message.video.file_name
	else:
		return None, None


async def get_deep_link(user: User, bot: Bot):
	payload = user.custom_username if user.custom_username else user.user_id
	link = await create_start_link(
		bot=bot,
		payload=f'{payload}',
	)
	return link


async def get_user(message: Message, repository: GeneralRepository):
	if message.forward_origin:
		user = await repository.user.get_user_by_full_name(
			full_name=message.forward_origin.sender_user.full_name
		)
	elif message.text.isdigit():
		user = await repository.user.get_user_by_tg_id(user_id=int(message.text))
	else:
		user = await repository.user.get_user_by_username(username=message.text[1:])
	return user


def get_content_types(media_type: str):
	content_types = {
		'photo': ContentType.PHOTO,
		'animation': ContentType.ANIMATION,
		'document': ContentType.DOCUMENT,
		'video': ContentType.VIDEO,
		'audio': ContentType.AUDIO,
		'voice': ContentType.VOICE,
		'video_note': ContentType.VIDEO_NOTE,
		'text': ContentType.TEXT,
		"sticker": ContentType.STICKER,

	}

	return content_types[media_type]