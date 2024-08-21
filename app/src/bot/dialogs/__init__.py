from aiogram import Router
from dishka import AsyncContainer

from .admin_dialog.dialog import admin_dialog
from .admin_settings_dialog.dialog import admin_dialog_settings
from .admin_users_dialog.dialog import admin_user_dialog
from .main_menu.dialog import main_menu_dialog
from .profile_dialog.dialog import profile_dialog
from .send_message_dialog.dialog import anon_msg_dialog
from .statistic_dialog.dialog import statistic_dialog
from .admin_broadcast.dialog import mailing_dialog
from ..midllewares.admin_midlleware import AdminMiddleware
from ..midllewares.clear_state import ClearState


def dialog_setups(dishka: AsyncContainer) -> Router:

	for router in (admin_dialog, admin_dialog_settings, admin_user_dialog, mailing_dialog, statistic_dialog):
		router.message.middleware(AdminMiddleware(dishka=dishka))
		router.callback_query.middleware(AdminMiddleware(dishka=dishka))

	router = Router()

	router.include_routers(
		mailing_dialog,
		admin_dialog,
		admin_dialog_settings,
		admin_user_dialog,
		main_menu_dialog,
		profile_dialog,
		anon_msg_dialog,
		statistic_dialog,
	)

	router.message.outer_middleware(ClearState())
	router.callback_query.outer_middleware(ClearState())

	return router
