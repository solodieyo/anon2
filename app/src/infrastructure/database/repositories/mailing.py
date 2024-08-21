from datetime import datetime
from typing import Optional

from sqlalchemy import select, func, and_, update
from sqlalchemy.sql.operators import or_

from app.src.enums import MailingType, MailingStatus
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.models.mailing import Mailing
from app.src.infrastructure.database.repositories.base import BaseRepository


class MailingRepository(BaseRepository):

    async def create_mailing(
            self,
            text: Optional[str],
            mailing_type: MailingType,
            user_count: int,
            content_type_media: Optional[list[str]],
            media: Optional[list[str]],
            finish_date: datetime
    ):
        mail = Mailing(
            text=text,
            mailing_type=mailing_type,
            user_count=user_count,
            content_type_media=content_type_media,
            media=media,
            finish_date=finish_date
        )

        self.session.add(mail)
        await self.session.commit()

    async def get_active_mailing(self) -> Optional[Mailing]:
        result = await self.session.scalar(select(Mailing).where(Mailing.status == MailingStatus.PENDING))
        return result

    async def get_count_users_for_mailing(self, mailing_type: MailingType):
        query = {
            'default': select(func.count(User.id)).where(User.premium.is_(False)),
            'premium': select(func.count(User.id)).where(User.premium.is_(True)),
            'all': select(func.count(User.id)),
        }

        result = await self.session.scalar(query[mailing_type])
        return result

    async def get_users(self, mailing_type: MailingType, start_from: int = 0):
        query = {
            MailingType.DEFAULT:
                select(User.user_id, User.locale)
                .order_by(User.id.asc())
                .where(and_(
                    User.archive.is_(False),
                    User.premium.is_(False),
                    User.id > start_from
                )),

            MailingType.PREMIUM:
                select(User.user_id, User.locale)
                .order_by(User.id.asc())
                .where(and_(
                    User.archive.is_(False),
                    User.premium.is_(True),
                    User.id > start_from
                )),

            MailingType.ALL:
                select(User.user_id, User.locale)
                .order_by(User.id.asc())
                .where(and_(
                    User.archive.is_(False),
                    User.id > start_from
                ))
        }

        result = await self.session.execute(query[mailing_type])
        return result.fetchall()

    async def finish_mailing(self, success_sent: int, failed_sent: int, status: MailingStatus):
        await self.session.execute(
            update(Mailing)
            .where(Mailing.status == MailingStatus.PENDING)
            .values(
                status=status,
                success_sent=success_sent,
                failed_sent=failed_sent,
                finish_date=func.now(),
            )
        )
        await self.session.commit()

    async def get_mailings(self):
        result = await self.session.scalars(
            select(Mailing.id)
            .where(or_(
                Mailing.status == MailingStatus.FINISH,
                Mailing.status == MailingStatus.FAILED
            ))
        )

        return result.fetchall()

    async def get_mailing_by_id(self, mailing_id):
        result = await self.session.scalar(
            select(Mailing)
            .where(Mailing.id == mailing_id)
        )

        return result
