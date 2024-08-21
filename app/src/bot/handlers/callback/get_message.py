from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.src.bot.dialogs.common.widgets import DELETE_KEYBOARD
from app.src.bot.states.default_states import SendMessageStates
from app.src.bot.dialogs.factory.callback import ReceivedCallbackData, BlockedCallbackData, UnblockCallbackData
from app.src.infrastructure.database.models import User
from app.src.infrastructure.database.repositories import GeneralRepository

router = Router()


@router.callback_query(ReceivedCallbackData.filter())
@inject
async def on_click_answer(
        callback: CallbackQuery,
        callback_data: ReceivedCallbackData,
        state: FSMContext,
        i18n: I18nContext,
        repository: FromDishka[GeneralRepository]
):
    message = await repository.user.get_hello_message(user_id=callback_data.from_user_id)
    text = i18n.get(
        'input-anon-msg',
        hello_message=f"{message}" if message else "no"
    )
    await state.update_data(
        to_user_id=callback_data.from_user_id,
        from_user_id=callback_data.to_user_id,

    )
    await state.set_state(SendMessageStates.input_anon_message)
    await callback.answer()
    await callback.message.reply(
        text=text,
        reply_markup=DELETE_KEYBOARD
    )


@router.callback_query(BlockedCallbackData.filter())
@inject
async def on_click_answer_blocked(
        callback: CallbackQuery,
        dialog_manager: DialogManager,
        repository: FromDishka[GeneralRepository],
        callback_data: BlockedCallbackData,
        user: User,
        i18n: I18nContext
):
    from_user = await repository.user.get_user_by_id(user_pk=callback_data.from_user_id)

    await repository.blocked.block_user(
        user_id=user.id,
        blocked_user_id=callback_data.from_user_id,
        message_id=callback_data.message_id
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(
            text=i18n.get('unblock-user-button'),
            callback_data=UnblockCallbackData(
                user_id=user.id,
                blocked_user_id=from_user.id,
                message_id=callback_data.message_id
            ).pack()
        )],
        [InlineKeyboardButton(
            text=i18n.get('answer-message-button'),
            callback_data=ReceivedCallbackData(
                message_id=callback_data.message_id,
                from_user_id=from_user.id,
                to_user_id=user.id
            ).pack()
        )],
    ]
    )

    if user.premium:
        if from_user.custom_username:
            username = from_user.custom_username
        elif from_user.username:
            username = f"@{from_user.username}"
        else:
            username = from_user.full_name

        if not user.show_premium_username:
            keyboard.inline_keyboard.insert(
                0, [InlineKeyboardButton(
                    text=i18n.get("checker-sender-not-premium"),
                    callback_data=f'user_faker_{from_user.user_id}'
                )], )
        else:
            keyboard.inline_keyboard.insert(
                0, [InlineKeyboardButton(
                    text=i18n.get("checker-sender-premium", username=username),
                    callback_data=f'user_faker_{from_user.user_id}'
                )], )
    else:
        keyboard.inline_keyboard.insert(
            0, [InlineKeyboardButton(
                text=i18n.get("checker-sender-not-premium"),
                callback_data=f'user_faker_{from_user.user_id}'
            )], )

    await callback.message.edit_reply_markup(
        reply_markup=keyboard
    )
