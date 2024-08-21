from dataclasses import dataclass
from typing import Optional


@dataclass
class BanListDTO:
	message_id: int
	text: Optional[str] = None
	content_type: Optional[str] = None

	def __post_init__(self):
		if self.text is None:
			self.text = ' '

		elif len(self.text) > 8:
			self.text = self.text[:8] + '...'

		