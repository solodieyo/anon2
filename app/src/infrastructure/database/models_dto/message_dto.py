from dataclasses import dataclass
from typing import Optional

from ..models import User, Message, Media


@dataclass
class MessageDTO:
	from_user: User
	to_user: User
	message: Message
	media: Optional[Media] = None


@dataclass
class BlockedDTO:
	from_user: User
	to_user: User
	message: Message
	media: Optional[Media] = None





