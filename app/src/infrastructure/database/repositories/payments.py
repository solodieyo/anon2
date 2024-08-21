from sqlalchemy import update

from app.src.enums import PaymentsStatus, PaymentType
from app.src.infrastructure.database.models import User, Payments
from app.src.infrastructure.database.repositories.base import BaseRepository


class PaymentsRepository(BaseRepository):

	async def add_payment(
		self,
		user: User,
		amount: int,
		payment_type: PaymentType
	):
		payment = Payments(
			user_id=user.id,
			amount=amount,
			status=PaymentsStatus.PENDING,
			payment_type=payment_type,
			locale_payed=user.locale
		)

		self.session.add(payment)
		await self.session.commit()
		return payment.id

	async def success_payment(
		self,
		payment_id: int,
		payment_time: int
	):
		await self.session.execute(
			update(Payments).where(Payments.id == payment_id).values(
				status=PaymentsStatus.SUCCESS,
				payments_time=payment_time
			)
		)
		await self.session.commit()

	async def cancel_payment(
		self,
		payment_id: int
	):
		await self.session.execute(
			update(Payments).where(Payments.id == payment_id).values(
				status=PaymentsStatus.CANCEL
			)
		)
		await self.session.commit()
