from aiogram_i18n import I18nContext
from aiogram import html

from app.src.enums import Roles
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository

PLACES = {
	1: "🥇",
	2: "🥈",
	3: "🥉",
	5: '🏆',
	6: '🏆',
	7: '🏆',
	8: '🏆',
	9: '🏆',
	10: '🏆'
}


async def get_user_profile_text(
	i18n: I18nContext,
	user: User,
	ask_user: User,
	repository: GeneralRepository,
	admin: bool = False,
) -> str:
	message_received_today = await repository.messages.get_received_messages_count_today(user_id=user.id)
	message_sent_today = await repository.messages.get_sent_messages_count_today(user_id=user.id)
	received_messages_count = await repository.messages.get_received_messages_count(user_id=user.id)
	sent_messages_count = await repository.messages.get_sent_messages_count(user_id=user.id)
	referral_username = await repository.user.get_user_username(user.referral_user_id)

	top_place = await repository.statistic.get_top_place(user_pk=user.id)
	link = f"<a href='t.me/{user.username}'>{user.full_name}</a>"

	locale = 'ru' if admin else ask_user.locale
	if user.referral_user_id:
		referral_text = f"<b>{referral_username}</b> <code>[ID: {user.referral_user_id}]</code>"
	else:
		referral_text = 'no'

	text = i18n.get(
		'premium-text-faker',
		locale,
		user_id=f"{user.user_id}",
		full_name=html.quote(user.full_name),
		username=user.username if user.username else 'no',
		role=user.rank,
		message_got_today=message_received_today,
		message_sent_today=message_sent_today,
		message_got=received_messages_count,
		message_sent=sent_messages_count,
		top_place=f"{PLACES.get(top_place, '')}#{top_place}",
		link=link if user.username else f"<a href='tg://user?id={user.user_id}'>{user.full_name}</a>",
		referral_text=referral_text,
		created_at=user.created_at,
		locale=user.locale
	)

	if ask_user.rank == Roles.ADMIN:
		text += f"\n{i18n.get(
			'last-activity',
			last_activity=user.last_activity.strftime("%d.%m.%Y %H:%M:%S"))}"

	return text
