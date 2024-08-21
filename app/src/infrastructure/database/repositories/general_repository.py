from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from .blocked import BlockedRepository
from .mailing import MailingRepository
from .messages import MessagesRepository
from .payments import PaymentsRepository
from .settings import SettingsRepository
from .statistic import StatisticRepository
from .user import UserRepository
from .user_updates import UserUpdatesRepository


class GeneralRepository(BaseRepository):
	def __init__(self, session: AsyncSession) -> None:
		super().__init__(session=session)
		self.user = UserRepository(session=session)
		self.messages = MessagesRepository(session=session)
		self.payments = PaymentsRepository(session=session)
		self.blocked = BlockedRepository(session=session)
		self.statistic = StatisticRepository(session=session)
		self.settings = SettingsRepository(session=session)
		self.mailing = MailingRepository(session=session)
		self.user_updates = UserUpdatesRepository(session=session)