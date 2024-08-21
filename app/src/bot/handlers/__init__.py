from aiogram import Router

from .start import router as start_router
from .callback.delete_message import router as delete_message_router
from .callback.get_message import router as get_message_router
from .callback.blocked import router as blocked_router
from .callback.get_user import router as get_user_router
from .commands.admin import router as admin_router
from .commands.language import router as language_router
from .commands.profile import router as profile_router
from .payments.stars_payouts import router as stars_router
from .message_answer import router as message_answer
from .callback.username_ignore import router as ignore_router
from .archive import router as archive_router
from .commands.premium import router as premium_router
from .callback.admin_day_stats import router as admin_day_stats_router


def setup_routers():
	router = Router()
	router.include_routers(
		admin_day_stats_router,
		archive_router,
		ignore_router,
		start_router,
		delete_message_router,
		get_message_router,
		admin_router,
		language_router,
		profile_router,
		blocked_router,
		get_user_router,
		stars_router,
		message_answer,
		premium_router
	)
	return router
