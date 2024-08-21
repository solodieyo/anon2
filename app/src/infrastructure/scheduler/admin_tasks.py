from datetime import timedelta, datetime

from aiogram import Bot
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.taskiq import inject

from app.src.bot.dialogs.common.widgets import get_admin_day_keyboard
from app.src.config import AppConfig
from app.src.infrastructure.database.repositories import GeneralRepository
from app.src.infrastructure.scheduler.broker import broker


@broker.task
@inject
async def admin_day_stats(
        repository: FromDishka[GeneralRepository],
        bot: FromDishka[Bot],
        config: FromDishka[AppConfig],
):
    date = datetime.now() - timedelta(hours=5)
    date_str = date.date().isoformat()
    default_statistic = await repository.statistic.get_statistic(
        selected_date=date_str
    )

    await bot.send_message(
        chat_id=config.tg.admin_id,
        text=get_statistic_text(
            statistic=default_statistic,
        ),
        reply_markup=get_admin_day_keyboard(
            date_num=date_str,
            now_state="common_statistic"
        )
    )


def get_statistic_text(statistic) -> str:
    text = f"""
🏛 <b>{statistic.date_type}</b> <code>{statistic.selected_date}</code>

👥 Пользователей в боте — <code>{statistic.users_count}</code> — <code>+{statistic.new_users}</code>
💣 Заблокировавших бота — <code>{statistic.blocked_users}</code> — <code>+{statistic.blocked_users_count}</code>
💳 Пополнения — <code>{statistic.payments_sum}₽</code> — <code>{statistic.payments_count} шт.</code>"""

    return text
