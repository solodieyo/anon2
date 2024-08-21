from dataclasses import dataclass
from typing import Optional

from aiogram.enums import ParseMode
from aiogram.types import Chat
from aiogram_dialog.api.entities import MarkupVariant


@dataclass
class NewMessage:
	chat: Chat
	text: Optional[str] = None
	reply_markup: Optional[MarkupVariant] = None
	parse_mode: Optional[str] = ParseMode.HTML
	disable_web_page_preview: Optional[bool] = True
	media: Optional[str] = None
	media_content_type: Optional[str] = None