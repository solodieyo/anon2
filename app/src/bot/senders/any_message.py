from types import NoneType

from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog.manager.message_manager import SEND_METHODS

from app.src.bot.senders.model import NewMessage


# pomenyati naming
async def send_message(bot: Bot, new_message: NewMessage) -> Message:
	if isinstance(new_message.media, list) and new_message.media[0] is not None or not isinstance(new_message.media,
																								  NoneType):
		return await _send_media(bot, new_message)
	else:
		return await _send_text(bot, new_message)


async def _send_text(bot: Bot, new_message: NewMessage) -> Message:
	return await bot.send_message(
		new_message.chat.id,
		text=new_message.text,
		disable_web_page_preview=new_message.disable_web_page_preview,
		reply_markup=new_message.reply_markup,
	)


async def _send_media(bot: Bot, new_message: NewMessage) -> Message:
	method = getattr(bot, SEND_METHODS[new_message.media_content_type], None)
	if not method:
		raise ValueError(
			f"ContentType {new_message.media_content_type} is not supported",
		)
	return await method(
		new_message.chat.id,
		new_message.media,
		caption=new_message.text,
		reply_markup=new_message.reply_markup,
		parse_mode=new_message.parse_mode,
	)
