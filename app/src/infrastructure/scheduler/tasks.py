from datetime import datetime

from dishka import FromDishka
from dishka.integrations.taskiq import inject

from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository
from app.src.infrastructure.scheduler.broker import broker


@broker.task
@inject
async def delete_subscribe(
	user_id: int,
	repository: FromDishka[GeneralRepository]
):
	user: User = await repository.user.get_user_by_tg_id(user_id)
	if user.premium_date:
		if user.premium_date.date() == datetime.now().date():
			await repository.user.delete_premium(user_id)
	return