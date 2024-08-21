from aiogram.filters import Filter
from aiogram.types import Message


class NewUserFilter(Filter):

	async def __call__(self, message: Message, new_user: bool):
		return new_user