from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.bot.states.dialog_states import AdminSettingsStates
from app.src.infrastructure.database.models_dto.locales_dto import LocalesDTO
from app.src.infrastructure.database.repositories import GeneralRepository


@inject
async def on_select_price(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository]
):
    dialog_manager.dialog_data['selected_price'] = widget.widget_id
    await dialog_manager.switch_to(state=AdminSettingsStates.change_price)


@inject
async def on_input_start_picture(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository]
):
    await repository.settings.update_start_picture(message.photo[0].file_id)
    dialog_manager.dialog_data['start_picture'] = True


@inject
async def delete_start_picture(_, __, ___, repository: FromDishka[GeneralRepository]):
    await repository.settings.delete_start_picture()


@inject
async def on_input_new_price(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository]
):
    date_type = f"{dialog_manager.dialog_data['selected_price']}_{dialog_manager.dialog_data['pay_type']}"
    await repository.settings.update_price(date_type, int(message.text))
    await dialog_manager.switch_to(AdminSettingsStates.select_price)


@inject
async def manage_language(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    dialog_manager.dialog_data['language'] = widget.widget_id
    await dialog_manager.switch_to(state=AdminSettingsStates.confirm_language)


@inject
async def confirm_language(
        _,
        __,
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository]
):
    i18n: I18nContext = dialog_manager.middleware_data['i18n']
    selected_locale = dialog_manager.dialog_data['language']
    language_status = dialog_manager.dialog_data[f"{selected_locale}_status"]
    await repository.settings.update_language_status(
        locale=selected_locale,
        status=not language_status
    )
    if language_status is True:
        i18n.core.locales.pop(selected_locale[7:])
    else:
        await i18n.core.startup()
        languages: LocalesDTO = await repository.settings.get_language_status()
        for locale in languages.get_disabled():
            if locale:
                i18n.core.locales.pop(locale)


async def on_select_pay_type(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    dialog_manager.dialog_data['pay_type'] = widget.widget_id
    await dialog_manager.switch_to(AdminSettingsStates.select_price)
