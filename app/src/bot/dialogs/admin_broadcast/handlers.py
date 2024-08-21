import asyncio

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, Chat
from aiogram_album import AlbumMessage
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from redis.asyncio import Redis

from app.src.bot.dialogs.common.trash import get_file_id
from app.src.bot.dialogs.common.widgets import DELETE_KEYBOARD
from app.src.bot.senders import send_message, NewMessage
from app.src.bot.senders.mailing.new_mailing import create_new_mailing
from app.src.bot.senders.mailing.start_mailing import INPUT_MEDIA_TYPES
from app.src.bot.states.dialog_states import BroadcastStates
from app.src.enums import MailingType
from app.src.infrastructure.database.models import Mailing
from app.src.infrastructure.database.repositories import GeneralRepository


async def choice_mailing_group(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    group = {
        'default': MailingType.DEFAULT,
        'premium': MailingType.PREMIUM,
        'all': MailingType.ALL,
    }

    dialog_manager.dialog_data['mail_group'] = group[widget.widget_id]
    await dialog_manager.switch_to(state=BroadcastStates.confirm_start)


@inject
async def on_input_album(
        message: AlbumMessage,
        widget: MessageInput,
        dialog_manager: DialogManager,
):
    dialog_manager.dialog_data['text'] = message.text or message.caption or '**альбом без текста**'
    dialog_manager.dialog_data['file_id'] = [(None, None)]
    dialog_manager.dialog_data['content_type_media'] = [m.content_type.value for m in message]
    await dialog_manager.switch_to(state=BroadcastStates.confirm_start)


@inject
async def on_input_message(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
):
    dialog_manager.dialog_data['default_mailing'] = True
    dialog_manager.dialog_data['text'] = message.text or message.caption
    dialog_manager.dialog_data['file_id'] = [get_file_id(message)]
    dialog_manager.dialog_data['content_type_media'] = [message.content_type.value]
    await dialog_manager.switch_to(state=BroadcastStates.confirm_start)


async def on_faker_click(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
):
    faker = dialog_manager.dialog_data.get('faker', False)
    dialog_manager.dialog_data['faker'] = not faker


@inject
async def start_broadcast(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
):
    bot: Bot = dialog_manager.middleware_data['bot']
    dishka = dialog_manager.middleware_data['dishka_container']
    i18n: I18nContext = dialog_manager.middleware_data['i18n']

    await create_new_mailing(
        text=dialog_manager.dialog_data['text'],
        dishka=dishka,
        mailing_type=dialog_manager.dialog_data.get('mail_group', MailingType.ALL),
        file_ids=dialog_manager.dialog_data['file_id'],
        content_type_media=dialog_manager.dialog_data['content_type_media'],
        bot=bot,
        faker=dialog_manager.dialog_data.get('faker', False),
        i18n=i18n
    )

    await dialog_manager.start(state=BroadcastStates.main_menu)


@inject
async def cancel_mailing(
        _,
        __,
        dialog_manager: DialogManager,
        redis: FromDishka[Redis]
):
    await redis.set(name='mailing:cancel', value='y')
    await asyncio.sleep(0.3)
    dialog_manager.dialog_data['active_mailing'] = False
    await dialog_manager.switch_to(state=BroadcastStates.main_menu)


@inject
async def show_mailing_content(
        _,
        __,
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository],
        bot: FromDishka[Bot],
):
    i18n: I18nContext = dialog_manager.middleware_data['i18n']
    mailing_content: Mailing = await repository.mailing.get_active_mailing()
    await _show_mailing_content(
        _,
        __,
        dialog_manager=dialog_manager,
        bot=bot,
        mailing_content=mailing_content,
        i18n=i18n
    )


@inject
async def show_previous_mailing(
        callback: CallbackQuery,
        __,
        dialog_manager: DialogManager,
        selected_item: str,
        repository: FromDishka[GeneralRepository],
        bot: FromDishka[Bot]
):
    dialog_manager.dialog_data['mailing_id'] = int(selected_item)
    await dialog_manager.switch_to(BroadcastStates.show_previus_mailing_content)


async def _show_mailing_content(
        callback: CallbackQuery,
        dialog_manager: DialogManager,
        bot: Bot,
        mailing_content: Mailing,
        i18n: I18nContext
):
    if len(mailing_content.media) > 1 and mailing_content.media[0] is not None:
        medias = [INPUT_MEDIA_TYPES[content_type](media=file_id) for file_id, content_type in
                  zip(mailing_content.media, mailing_content.content_type_media)]
        medias[0].caption = mailing_content.text
        await bot.send_media_group(
            chat_id=dialog_manager.event.from_user.id,
            media=medias,
        )
    else:
        media = mailing_content.media[0][0]
        chat: Chat = await bot.get_chat(dialog_manager.event.from_user.id)
        await send_message(
            bot=bot,
            new_message=NewMessage(
                text=mailing_content.text,
                media=media,
                media_content_type=mailing_content.content_type_media[0] if mailing_content.media else None,
                chat=chat,
                reply_markup=DELETE_KEYBOARD
            )
        )


@inject
async def show_previous_mailing_content(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository],
        bot: FromDishka[Bot]
):
    i18n: I18nContext = dialog_manager.middleware_data['i18n']
    mailing_id = dialog_manager.dialog_data['mailing_id']
    mailing_content: Mailing = await repository.mailing.get_mailing_by_id(mailing_id=mailing_id)
    await _show_mailing_content(
        callback=callback,
        dialog_manager=dialog_manager,
        bot=bot,
        mailing_content=mailing_content,
        i18n=i18n
    )

