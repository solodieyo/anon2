import time
from datetime import datetime
from itertools import zip_longest
from typing import Optional

from aiocryptopay import AioCryptoPay
from aiogram import html, Bot
from aiogram.types import LabeledPrice
from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from redis.asyncio import Redis

from app.src.config import AppConfig
from app.src.enums import PaymentType
from app.src.infrastructure.database.models import User, Blocked
from app.src.infrastructure.database.models_dto.ban_list_dto import BanListDTO
from app.src.infrastructure.database.models_dto.prices_dto import PricesDTO
from app.src.infrastructure.database.models_dto.rating_dto import RatingDTO
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


@inject
async def getter_profile_menu_text(
    dialog_manager: DialogManager,
    repository: FromDishka[GeneralRepository],
    user: User,
    **_
):

    message_received_today = await repository.messages.get_received_messages_count_today(user_id=user.id)
    message_sent_today = await repository.messages.get_sent_messages_count_today(user_id=user.id)
    top_place = await repository.statistic.get_top_place(user_pk=user.id)
    link = f"<a href='t.me/{user.username}'>{user.full_name}</a>"
    return {
        "from_user_id": user.user_id,
        "full_name": html.quote(user.full_name),
        "username": user.custom_username or user.username or html.quote(user.full_name),
        "role": user.rank,
        "message_received_today": message_received_today,
        "message_sent_today": message_sent_today,
        "top_place": f"{PLACES.get(top_place, '')}#{top_place}",
        "link": link if user.username else f"<a href='tg://user?id={user.user_id}'>{user.full_name}</a>"
    }


@inject
async def getter_profile_settings_text(dialog_manager: DialogManager, repository: FromDishka[GeneralRepository], **_):
    locale = await repository.user.get_user_locale(user_id=dialog_manager.event.from_user.id)
    return {
        "locale": locale
    }


@inject
async def getter_hello_menu(dialog_manager: DialogManager, repository: FromDishka[GeneralRepository], **_):
    hello_message: Optional[str] = await repository.user.get_user_hello_message(
        user_id=dialog_manager.event.from_user.id
    )

    dialog_manager.dialog_data["hello_message"] = hello_message

    return {
        "hello_message": hello_message if hello_message else 'no',
        'wrong_hello': dialog_manager.dialog_data.get('wrong_hello', False)
    }


@inject
async def getter_ban_list(
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository],
        user: User,
        i18n: I18nContext,
        **_
):
    ban_list = await repository.blocked.get_user_ban_list(user_id=user.id, i18n=i18n)
    return {
        "ban_list": ban_list
    }


def get_ban_list_id(item: BanListDTO):
    return item.message_id


@inject
async def getter_top_type(
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository],
        i18n: I18nContext,
        **_
):
    types_top = {
        "senders": repository.statistic.get_senders_top,
        "getters": repository.statistic.get_getters_top
    }
    type_top = dialog_manager.dialog_data.get("type_top", "senders")
    top_info: RatingDTO = await types_top[type_top](
        user_id=dialog_manager.middleware_data['user'].id
    )
    data = {
        "type": type_top,
        "from_user_place": top_info.from_user_place if top_info.from_user_count > 0 else "xxx",
        "from_user_count": top_info.from_user_count
    }
    for i, user_data in zip_longest(range(1, 11), top_info.users, fillvalue='no'):
        user_data = user_data[0]
        if isinstance(user_data, str):
            username = "no"
        elif user_data.show_in_tops:
            username = html.quote(user_data.full_name)
        else:
            username = i18n.get('hidden-username')

        data[f"username{i}"] = username
        data[f"username{i}_count"] = user_data.count_send_message\
            if type_top == "senders" else user_data.count_received_message

    return data


async def getter_user_id(
        dialog_manager: DialogManager,
        user: User,
        **_
):
    return {
        "user_id": user.custom_username or f'{dialog_manager.event.from_user.id}'.strip(),
        'exist_username': dialog_manager.dialog_data.get('exist_username', False)
    }


@inject
async def getter_invoice_stars_text(
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository],
        redis: FromDishka[Redis],
        config: FromDishka[AppConfig],
        bot: Bot,
        user: User,
        **_
):
    start_time_payment = int(time.time())
    payment_type = await redis.get(f'payment:payment_type:{user.user_id}')
    price = await repository.settings.get_price_by_type_stars(payment_type)

    payment_id = await repository.payments.add_payment(
        user=user,
        payment_type=PaymentType.STARS,
        amount=(price * 1.15) * 100
    )
    await redis.set(
        name=f"payment:start_time:{user.user_id}",
        value=start_time_payment

    )
    await redis.set(
        name=f"payment:payment_id:{user.user_id}",
        value=payment_id
    )
    invoice_link = await bot.create_invoice_link(
        title='Premium',
        description='premium subscription',
        prices=[LabeledPrice(label="XTR", amount=price)],
        provider_token="",
        payload=f"{price}_stars",
        currency="XTR"
    )

    return {
        "payment_id": payment_id,
        "link": invoice_link,
        'price': price,
        'payment_type': payment_type,
        'support_username': config.tg.support_username
    }


@inject
async def getter_invoice_crypto_text(
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository],
        crypto: FromDishka[AioCryptoPay],
        redis: FromDishka[Redis],
        config: FromDishka[AppConfig],
        user: User,
        **_
):
    start_time_payment = int(time.time())

    await redis.set(
        name=f"payment:start_time:{user.user_id}",
        value=start_time_payment
    )

    payment_type = await redis.get(f"payment:payment_type:{user.user_id}")
    price = await repository.settings.get_price_by_type_crypto(payment_type)
    payment_id = await repository.payments.add_payment(
        user=user,
        payment_type=PaymentType.CRYPTO_BOT,
        amount=price * 100
    )
    await redis.set(
        name=f"payment:payment_id:{user.user_id}",
        value=payment_id
    )
    invoice = await crypto.create_invoice(
        currency_type='fiat',
        fiat='RUB',
        accepted_assets=['BTC', 'USDT', 'TRX'],
        amount=price,
        payload=str(user.user_id),
    )

    dialog_manager.dialog_data['invoice_id'] = invoice.invoice_id
    return {
        "link": invoice.bot_invoice_url,
        "price": price,
        "payment_type": payment_type,
        "payment_id": payment_id,
        'support_username': config.tg.support_username
    }


@inject
async def getter_premium_sub(
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository],
        user: User,
        config: FromDishka[AppConfig],
        **_
):
    prices: PricesDTO = await repository.settings.get_prices_stars()
    if user.premium_date:
        premium_active = user.premium_date.strftime('%d.%m.%Y')
    elif user.premium and not user.premium_date:
        premium_active = 'adm'
    else:
        premium_active = 'no'

    show_username = False
    if user.premium and user.show_premium_username is True or user.premium and user.show_premium_username is None:
        show_username = True
    elif user.premium and user.show_premium_username is False:
        show_username = False
    return {
        "premium_active": premium_active,
        "day_price": prices.price_day,
        "week_price": prices.price_week,
        "month_price": prices.price_month,
        "forever_price": prices.price_forever,
        "price_forever": prices.price_forever,
        "show_username": show_username,
        'command': dialog_manager.start_data["command"] if dialog_manager.start_data else False,
        'day': config.tg.premium_day,
        'week': config.tg.premium_week,
        'month': config.tg.premium_month,
        'forever': config.tg.premium_forever
    }


@inject
async def get_price(
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository],
        redis: FromDishka[Redis],
        user: User,
        **_
):
    payment_type = await redis.get(f"payment:payment_type:{user.user_id}")
    price = await repository.settings.get_price_by_type_crypto(payment_type)

    return {
        "price": price
    }


async def getter_bot_username(
    dialog_manager: DialogManager,
    bot: Bot,
    **_
):
    bot_data = await bot.get_me()
    return {
        'bot_username': bot_data.username
    }