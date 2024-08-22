from datetime import date, timedelta, datetime
from typing import Union

from sqlalchemy import select, func, and_, cast, Float, extract

from app.src.enums import Locale, PaymentsStatus, PaymentType
from ..models_dto.rating_dto import RatingDTO
from ..models_dto.statistic_dto import (
	CommonStatisticDTO,
	LanguageStatisticDTO,
	UsersStatisticDTO,
	UserMessageStatisticDTO, PreviewStatistic, PaymentsDTO
)
from app.src.infrastructure.database.models import Message, User, Payments
from app.src.infrastructure.database.repositories.base import BaseRepository


class StatisticRepository(BaseRepository):
	wheres = {
		"today": {
			"date_type": "СЕГОДНЯ",
			"selected_date": lambda **kwargs: f"[{date.today()}]",
			'where': lambda **kwargs: func.date(kwargs['x']) == date.today(),

		},
		"week": {
			"date_type": "ЗА НЕДЕЛЮ",
			"selected_date": lambda **kwargs: f"[{date.today() - timedelta(days=7)} - {date.today()}]",
			'where': lambda **kwargs: func.date(kwargs['x']).between(date.today() - timedelta(days=7), date.today()),
		},
		"month": {
			"date_type": "ЗА МЕСЯЦ",
			"selected_date": lambda **kwargs: f"[{date.today() - timedelta(days=30)} - {date.today()}]",
			'where': lambda **kwargs: func.date(kwargs['x']).between(date.today() - timedelta(days=30), date.today()),
		},
		"select_date": {
			"date_type": "ЗА ДАТУ",
			"selected_date": lambda **kwargs: f"[{kwargs['selected_date']}]",
			'where': lambda **kwargs: func.date(kwargs['x']) == kwargs['selected_date'],
		},
		"period": {
			"date_type": "ЗА ПЕРИОД",
			"selected_date": lambda **kwargs: f"[{kwargs['start_date']} - {kwargs['end_date']}]",
			'where': lambda **kwargs: func.date(kwargs['x']).between(kwargs['start_date'], kwargs['end_date']),
		}
	}

	async def get_statistic(
		self,
		statistic_type: str = "common_statistic",
		date_type: str = "today",
		selected_date: str = None,
		start_date: str = None,
		end_date: str = None,
	) -> Union[CommonStatisticDTO, LanguageStatisticDTO, PaymentsDTO]:

		if start_date and end_date:
			start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
			end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

		if selected_date:
			selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

		if statistic_type == "common_statistic":
			return await self._get_common_statistic(
				date_type=date_type,
				selected_date=selected_date,
				start_date=start_date,
				end_date=end_date
			)
		elif statistic_type == "languages_statistic":
			return await self._get_language_statistic(
				date_type=date_type,
				selected_date=selected_date,
				start_date=start_date,
				end_date=end_date
			)
		else:
			return await self._get_payments_statistic(
				date_type=date_type,
				selected_date=selected_date,
				start_date=start_date,
				end_date=end_date
			)

	async def _get_language_statistic(
		self,
		date_type: str,
		**kwargs
	) -> LanguageStatisticDTO:

		new_users = await self.session.scalar(
			select(func.count(User.id))
			.where(self.wheres[date_type]['where'](x=User.created_at, **kwargs))
		)

		ru_payments = await self.session.execute(
			select(func.sum(Payments.amount), func.count(Payments.id))
			.where(and_(
				self.wheres[date_type]['where'](x=Payments.created_at, **kwargs, ),
				Payments.locale_payed == Locale.RU,
				Payments.status == PaymentsStatus.SUCCESS
			))
		)
		ru_payments_sum, ru_payments_count = ru_payments.first()

		en_payments = await self.session.execute(
			select(func.sum(Payments.amount), func.count(Payments.id))
			.where(and_(
				self.wheres[date_type]['where'](x=Payments.created_at, **kwargs, ),
				Payments.locale_payed == Locale.EN,
				Payments.status == PaymentsStatus.SUCCESS
			))
		)
		en_payments_sum, en_payments_count = en_payments.first()

		uk_payments = await self.session.execute(
			select(func.sum(Payments.amount), func.count(Payments.id))
			.where(and_(
				self.wheres[date_type]['where'](x=Payments.created_at, **kwargs, ),
				Payments.locale_payed == Locale.UK,
				Payments.status == PaymentsStatus.SUCCESS
			))
		)
		uk_payments_sum, uk_payments_count = uk_payments.first()

		de_payments = await self.session.execute(
			select(func.sum(Payments.amount), func.count(Payments.id))
			.where(and_(
				self.wheres[date_type]['where'](x=Payments.created_at, **kwargs, ),
				Payments.locale_payed == Locale.DE,
				Payments.status == PaymentsStatus.SUCCESS
			))
		)
		de_payments_sum, de_payments_count = de_payments.first()

		new_ru_users_count = await self.session.scalar(
			select(func.count(User.id))
			.where(self.wheres[date_type]['where'](x=User.created_at, **kwargs),
				   User.locale == Locale.RU)
		)

		new_en_users_count = await self.session.scalar(
			select(func.count(User.id))
			.where(self.wheres[date_type]['where'](x=User.created_at, **kwargs),
				   User.locale == Locale.EN)
		)

		new_uk_users_count = await self.session.scalar(
			select(func.count(User.id))
			.where(self.wheres[date_type]['where'](x=User.created_at, **kwargs),
				   User.locale == Locale.UK)
		)

		new_de_users_count = await self.session.scalar(
			select(func.count(User.id))
			.where(self.wheres[date_type]['where'](x=User.created_at, **kwargs),
				   User.locale == Locale.DE)
		)

		sent_message_count = await self.session.scalar(
			select(func.count(Message.id))
			.where(self.wheres[date_type]['where'](x=Message.created_at, **kwargs))
		)

		ru_sent_message_count = await self.session.scalar(
			select(func.count(Message.id))
			.where(and_(self.wheres[date_type]['where'](x=Message.created_at, **kwargs),
						Message.from_user_id.in_(
							select(User.id)
							.where(User.locale == Locale.RU)
						))
				   )
		)

		en_sent_message_count = await self.session.scalar(
			select(func.count(Message.id))
			.where(and_(self.wheres[date_type]['where'](x=Message.created_at, **kwargs),
						Message.from_user_id.in_(
							select(User.id)
							.where(User.locale == Locale.EN)
						))
				   )
		)

		uk_sent_message_count = await self.session.scalar(
			select(func.count(Message.id))
			.where(and_(self.wheres[date_type]['where'](x=Message.created_at, **kwargs),
						Message.from_user_id.in_(
							select(User.id)
							.where(User.locale == Locale.UK)
						))
				   )
		)

		de_sent_message_count = await self.session.scalar(
			select(func.count(Message.id))
			.where(and_(self.wheres[date_type]['where'](x=Message.created_at, **kwargs),
						Message.from_user_id.in_(
							select(User.id)
							.where(User.locale == Locale.DE)
						))
				   )
		)

		ru_received_message_count = await self.session.scalar(
			select(func.count(Message.id))
			.where(and_(self.wheres[date_type]['where'](x=Message.created_at, **kwargs),
						Message.to_user_id.in_(
							select(User.id)
							.where(User.locale == Locale.RU)
						))
				   )
		)

		en_received_message_count = await self.session.scalar(
			select(func.count(Message.id))
			.where(and_(self.wheres[date_type]['where'](x=Message.created_at, **kwargs),
						Message.to_user_id.in_(
							select(User.id)
							.where(User.locale == Locale.EN)
						))
				   )
		)

		de_received_message_count = await self.session.scalar(
			select(func.count(Message.id))
			.where(and_(self.wheres[date_type]['where'](x=Message.created_at, **kwargs),
						Message.to_user_id.in_(
							select(User.id)
							.where(User.locale == Locale.DE)
						))
				   )
		)

		uk_received_message_count = await self.session.scalar(
			select(func.count(Message.id))
			.where(and_(self.wheres[date_type]['where'](x=Message.created_at, **kwargs),
						Message.to_user_id.in_(
							select(User.id)
							.where(User.locale == Locale.UK)
						))
				   )
		)

		received_message_count = await self.session.scalar(
			select(func.count(Message.id))
			.where(self.wheres[date_type]['where'](x=Message.created_at, **kwargs))
		)

		payments_count = await self.session.scalar(
			select(func.count(Payments.id))
			.where(and_(self.wheres[date_type]['where'](x=Payments.created_at, **kwargs),
						Payments.status == PaymentsStatus.SUCCESS))
		)

		statistic = LanguageStatisticDTO(
			date_type=self.wheres[date_type]['date_type'],
			selected_date=self.wheres[date_type]['selected_date'](**kwargs),
			new_users=new_users,
			ru_payments_sum=ru_payments_sum / 100 if ru_payments_sum else 0,
			ru_payments_count=ru_payments_count,
			en_payments_sum=en_payments_sum / 100 if en_payments_sum else 0,
			en_payments_count=en_payments_count,
			uk_payments_sum=uk_payments_sum / 100 if uk_payments_sum else 0,
			uk_payments_count=uk_payments_count,
			de_payments_sum=de_payments_sum / 100 if de_payments_sum else 0,
			de_payments_count=de_payments_count,
			new_ru_users_count=new_ru_users_count,
			new_en_users_count=new_en_users_count,
			new_uk_users_count=new_uk_users_count,
			new_de_users_count=new_de_users_count,
			sent_message_count=sent_message_count,
			ru_sent_message_count=ru_sent_message_count,
			en_sent_message_count=en_sent_message_count,
			uk_sent_message_count=uk_sent_message_count,
			de_sent_message_count=de_sent_message_count,
			ru_received_message_count=ru_received_message_count,
			en_received_message_count=en_received_message_count,
			uk_received_message_count=uk_received_message_count,
			de_received_message_count=de_received_message_count,
			received_message_count=received_message_count,
			payments_count=payments_count
		)
		return statistic

	async def _get_common_statistic(
		self,
		date_type: str,
		**kwargs
	) -> CommonStatisticDTO:
		new_users = await self.session.scalar(
			select(func.count(User.id))
			.where(self.wheres[date_type]['where'](x=User.created_at, **kwargs))
		)

		blocked_users_count = await self.session.scalar(
			select(func.count(User.id))
			.where(and_(User.archive is True,
						self.wheres[date_type]['where'](x=User.updated_at, **kwargs)))
		)

		payments = await self.session.execute(
			select(func.sum(Payments.amount), func.count(Payments.id))
			.where(and_(self.wheres[date_type]['where'](x=Payments.created_at, **kwargs),
						Payments.status == PaymentsStatus.SUCCESS))
		)

		payments_amount, payments_count = payments.first()

		return CommonStatisticDTO(
			date_type=self.wheres[date_type]['date_type'],
			selected_date=self.wheres[date_type]['selected_date'](**kwargs),
			users_count=await self._get_users_count(),
			new_users=new_users,
			blocked_users=await self._get_blocked_users_count(),
			blocked_users_count=blocked_users_count,
			payments_count=payments_count,
			payments_sum=payments_amount / 100 if payments_amount else 0

		)

	async def _get_users_count(self):
		result = await self.session.scalar(select(func.count(User.id)))
		return result

	async def _get_blocked_users_count(self):
		blocked_users = await self.session.scalar(
			select(func.count(User.id))
			.where(func.date(User.archive) is True)
		)
		return blocked_users

	async def _get_payments_statistic(
		self,
		date_type: str,
		**kwargs
	) -> PaymentsDTO:
		payments_success = await self.session.execute(
			select(func.sum(Payments.amount), func.count(Payments.id))
			.where(and_(
				self.wheres[date_type]['where'](x=Payments.created_at, **kwargs),
				Payments.status == PaymentsStatus.SUCCESS)
			)
		)

		success_payments_sum, success_payments_count = payments_success.first()

		payments_pending = await self.session.execute(
			select(func.sum(Payments.amount), func.count(Payments.id))
			.where(and_(
				self.wheres[date_type]['where'](x=Payments.created_at, **kwargs),
				Payments.status == PaymentsStatus.PENDING)
			))

		pending_payments_sum, pending_payments_count = payments_pending.first()

		payments_time = await self.session.scalar(
			select(func.avg(Payments.payments_time))
			.where(and_(self.wheres[date_type]['where'](x=Payments.created_at, **kwargs),
						Payments.status == PaymentsStatus.SUCCESS)))

		payments_star = await self.session.execute(
			select(func.sum(Payments.amount), func.count(Payments.id))
			.where(and_(
				self.wheres[date_type]['where'](x=Payments.created_at, **kwargs),
				Payments.payment_type == PaymentType.STARS,
				Payments.status == PaymentsStatus.SUCCESS)
			))

		payments_stars_sum, payments_stars_count = payments_star.first()

		payments_crypto = await self.session.execute(
			select(func.sum(Payments.amount), func.count(Payments.id))
			.where(and_(
				self.wheres[date_type]['where'](x=Payments.created_at, **kwargs),
				Payments.payment_type == PaymentType.CRYPTO_BOT,
				Payments.status == PaymentsStatus.SUCCESS)
			))

		payments_sum_crypto, payments_count_crypto = payments_crypto.first()

		statistic = PaymentsDTO(
			date_type=self.wheres[date_type]['date_type'],
			selected_date=self.wheres[date_type]['selected_date'](**kwargs),
			payments_sum=success_payments_sum / 100 if success_payments_sum else 0,
			payments_count=success_payments_count,
			payments_not_success_sum=pending_payments_sum / 100 if pending_payments_sum else 0,
			payments_not_success_count=pending_payments_count,
			payments_time=seconds_to_minutes_and_seconds(payments_time) if payments_time else 0,
			stars_sum=payments_stars_sum / 100 if payments_stars_sum else 0,
			stars_count=payments_stars_count,
			crypto_bot_sum=payments_sum_crypto / 100 if payments_sum_crypto else 0,
			crypto_bot_count=payments_count_crypto
		)
		return statistic

	async def get_preview_statistic(self):
		count_users = await self.session.scalar(select(func.count(User.id)))
		count_messages = await self.session.scalar(select(func.count(Message.id)))
		users_today = await self.session.scalar(
			select(func.count(User.id))
			.where(func.date(User.created_at) == date.today())
		)
		message_today = await self.session.scalar(
			select(func.count(Message.id))
			.where(func.date(Message.created_at) == date.today())
		)
		return PreviewStatistic(
			count_users,
			count_messages,
			users_today,
			message_today
		)

	async def get_users_statistic(self):
		total_users_count = await self.session.scalar(select(func.count(User.id)))

		total_ru_users = await self.session.scalar(
			select(func.count(User.id))
			.where(
				User.locale == "ru"
			)
		)

		total_ua_users = await self.session.scalar(
			select(func.count(User.id))
			.where(
				User.locale == "uk"
			)
		)

		total_en_users = await self.session.scalar(
			select(func.count(User.id))
			.where(
				User.locale == "en"
			)
		)

		total_de_users = await self.session.scalar(
			select(func.count(User.id))
			.where(
				User.locale == "de"
			)
		)

		return UsersStatisticDTO(
			total_users_count,
			total_ru_users,
			total_ua_users,
			total_en_users,
			total_de_users
		)

	async def get_user_message_statistic(self, user_id: int):
		message_sent_count = await self.session.scalar(
			select(func.count(Message.id))
			.where(Message.from_user_id == user_id)
		)
		message_sent_today = await self.session.scalar(
			select(func.count(Message.id))
			.where(and_(
				Message.from_user_id == user_id,
				func.date(Message.created_at) == date.today()
			))
		)

		message_received_count = await self.session.scalar(
			select(func.count(Message.id))
			.where(Message.to_user_id == user_id)
		)
		message_received_today = await self.session.scalar(
			select(func.count(Message.id))
			.where(and_(
				Message.to_user_id == user_id,
				func.date(Message.created_at) == date.today())
			)
		)
		return UserMessageStatisticDTO(
			message_sent_count,
			message_sent_today,
			message_received_count,
			message_received_today
		)

	async def get_senders_top(self, user_id: int):
		result_top = await self.session.execute(
			select(User).order_by(User.count_send_message.desc()).limit(10)
		)

		rank_query = (
			select(
				User.id,
				User.count_send_message.label('message_count'),
				func.row_number().over(order_by=[User.count_send_message.desc(), User.id]).label('place')
			)
			.subquery()
		)

		result_user_info = await self.session.execute(
			select(
				rank_query.c.message_count,
				rank_query.c.place
			)
			.where(rank_query.c.id == user_id)
		)

		user_info = result_user_info.first()
		return RatingDTO(
			users=result_top.all(),
			from_user_place=user_info.place,
			from_user_count=user_info.message_count
		)

	async def get_top_place(self, user_pk: int):

		rank_query = (
			select(
				User.id,
				User.count_send_message.label('message_count'),
				func.row_number().over(order_by=[User.count_send_message.desc(), User.id]).label('place')
			)
			.subquery()
		)

		# Затем фильтруем результаты по конкретному пользователю
		result = await self.session.execute(
			select(
				rank_query.c.message_count,
				rank_query.c.place
			)
			.where(rank_query.c.id == user_pk)
		)

		user_place = result.first()
		return user_place.place if user_place.message_count > 0 else 'xxx'

	async def get_getters_top(self, user_id: int):

		result_top = await self.session.execute(
			select(User).order_by(User.count_received_message.desc()).limit(10)
		)

		rank_query = (
			select(
				User.id,
				User.count_received_message.label('message_count'),
				func.row_number().over(order_by=[User.count_received_message.desc(), User.id]).label('place')
			)
			.subquery()
		)

		result_user_info = await self.session.execute(
			select(
				rank_query.c.message_count,
				rank_query.c.place
			)
			.where(rank_query.c.id == user_id)
		)

		user_info = result_user_info.first()
		return RatingDTO(
			users=result_top.all(),
			from_user_place=user_info.place,
			from_user_count=user_info.message_count
		)


def seconds_to_minutes_and_seconds(seconds):
	minutes = seconds // 60
	seconds = seconds % 60
	return f"{int(minutes)}м.{int(seconds)}с"
