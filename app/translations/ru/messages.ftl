choice-language-text = <b>Выберите язык</b>

main-menu-text =
    🔗 <b>Начни получать анонимные сообщения прямо сейчас!</b>

    <i>Твоя личная ссылка:</i>
    👉 { $link }

    Размести эту ссылку в своём профиле <b>Telegram</b> ● <b>Instagram</b> ● <b>TikTok</b> или других соц. сетях, чтобы начать получать сообщения 💬

profile-menu-user-kek =
    ⭐️ <b>Пользователь —</b> <b>{ $link }</b>
    📌 <b>Юзернейм —</b> <code>{ $username }</code>
    🎗 <b>Ранг —</b> <code>{ $role ->
                                [member] <code>Пользователь</code>
                                [admin] <code>Админ</code> 🅰️
                                *[other] <code>Пользователь</code>
                            }</code> | <code>{ $top_place }</code>

    ➖➖➖➖➖➖➖➖➖➖➖➖

    📬 <b>Отправлено сообщений</b> — <code>{ $sent_messages_count }</code>
    └ <i>Сегодня</i> — <code>{ $message_sent_today }</code>
    💬 <b>Получено сообщений</b> — <code>{ $received_messages_count }</code>
    └ <i>Сегодня</i> — <code>{ $message_received_today }</code>


profile-settings =
    ⚙️<b>Настройки</b>

    <b>Язык</b> - 🇷🇺<b>Русский</b>

profile-change-hello =
    👋 <b>Здесь вы можете установить приветствие</b>

    Сейчас ваше приветствие выглядит так:

    { $hello_message ->
                    *[other] <b>{ $hello_message }</b>
                      [no]  <i>Сообщение не установлено</i>
    }

profile-create-username =
    📍 <b>Здесь вы можете установить никнейм для вашей ссылки</b>

    Сейчас ваша ссылка для получения анонимных сообщений выглядит так:

    <pre language="link">t.me/{ $bot_username }?start={ $user_id }</pre>

    А если вы установите никнейм, то ваша ссылка будет выглядеть так:

    <pre language="link">t.me/{ $bot_username }?start=ВАШ_НИКНЕЙМ</pre>

    ❗️ <b>Обратите внимание, что при смене ссылки, старая ссылка перестанет быть активной!</b>

input-anon-msg =
    ❓ Отправь анонимное сообщение для пользователя

    { $hello_message ->
                     *[other] <b>{ $hello_message }</b>
                      [no] <b>Напиши сюда всё, что хочешь, а пользователь сразу получит это сообщение, но не будет знать от кого оно</b>
    }

    ❗️<i>Ты можешь отправить текст, фото, видео, гифку, голосовое сообщение, видеосообщение, стикер или музыку</i>

get-anon-msg =
    <b>У тебя новое анонимное сообщение</b>


success-send =
    • <b>Твое сообщение было отправлено! (И оно уже пришло получателю)</b>

    <b>P.S. Тебе может прийти ответ на сообщение</b>

ban-list-menu = ⛔️ <b>У вас нету заблокированных пользователей</b>

new-message-text =
    Тебе пришло новое сообщение:

    <b>{ $message_text }</b>


ratings-text =
    ⭐️ <b>Рейтинг</b> — <b>{ $type ->
                            [getters] 💬 Получатели
                            *[senders] 📬 Отправители
                            }</b>

    { $username1 ->
        *[other] 🥇<b>#1 </b>{ $username1 } — <code>{ $username1_count }</code>
        [no] 🥇<b>#1 </b>Cкрыт — <code>0</code>
    }
    { $username2 ->
        *[other] 🥈<b>#2 </b>{ $username2 } — <code>{ $username2_count }</code>
        [no] 🥈<b>#2 </b>Cкрыт — <code>0</code>
    }
    { $username3 ->
        *[other] 🥉<b>#3 </b>{ $username3 } — <code>{ $username3_count }</code>
        [no] 🥉<b>#3 </b>Cкрыт — <code>0</code>
    }
    { $username4 ->
        *[other] 🏆<b>#4 </b>{ $username4 } — <code>{ $username4_count }</code>
        [no] 🏆<b>#4 </b>Cкрыт — <code>0</code>
    }
    { $username5 ->
        *[other] 🏆<b>#5 </b>{ $username5 } — <code>{ $username5_count }</code>
        [no] 🏆<b>#5 </b>Cкрыт — <code>0</code>
    }
    { $username6 ->
        *[other] 🏆<b>#6 </b>{ $username6 } — <code>{ $username6_count }</code>
        [no] 🏆<b>#6 </b>Cкрыт — <code>0</code>
    }
    { $username7 ->
        *[other] 🏆<b>#7 </b>{ $username7 } — <code>{ $username7_count }</code>
        [no] 🏆<b>#7 </b>Cкрыт — <code>0</code>
    }
    { $username8 ->
        *[other] 🏆<b>#8 </b>{ $username8 } — <code>{ $username8_count }</code>
        [no] 🏆<b>#8 </b>Cкрыт — <code>0</code>
    }
    { $username9 ->
        *[other] 🏆<b>#9 </b>{ $username9 } — <code>{ $username9_count }</code>
        [no] 🏆<b>#9 </b>Cкрыт — <code>0</code>
    }
    { $username10 ->
        *[other] 🏆<b>#10</b> { $username10 } — <code>{ $username10_count }</code>
        [no] 🏆<b>#10</b> Cкрыт — <code>0</code>
    }

    👤 <b>Вы</b> — <b>#{ $from_user_place }</b> — <code>{ $from_user_count }</code>

# kek

profile-premium =
    ✍🏻 { $premium_active ->
                            [no] <b>Сейчас у вас нет доступа</b>
                            [adm] <b>Доступ активирован навсегда</b>
                            *[other] <b>Доступ активирован до { $premium_active }</b>
        }

    🛒 Покупая данный товар, вы получаете доступ к просмотру <b>информации</b> об отправителе сообщений

    🔎 <b>Вы сможете узнать:</b>

    • <i>Имя | Фамилия | ID</i>
    • <i>Юзернейм (если присутствует)</i>
    • <i>Ранг и место в рейтинге</i>
    • <i>Статистику отправлений и получений сообщений</i>
    • <i>Дату регистрации</i>

    👑 <b>Выберите срок действия Premium:</b>

premium-choose-pay =
    💳 <b>Стоимость покупки составит { $price }₽</b>

    🌐 <b>Выберите способ оплаты:</b>

premium-stars-pay-finish = ⭐️ Telegram stars

premium-pay-finish =
    ✅ <b>Счёт #{ $payment_id } на оплату сформирован!</b>
    💳 <b>Вы покупаете доступ на</b> { $payment_type ->
                                                [premium_price_day] <b>1 день</b>
                                                [premium_price_week] <b>1 неделю</b>
                                                *[premium_price_month] <b>1 месяц</b>
                                } <b>за { $price }₽</b>

    Для оплаты перейдите по ссылке ниже или нажмите на кнопку
    <b>"💳 Оплатить"</b>

    { $link }

    📞 В случае возникновения проблем с оплатой обратитесь к поддержке — @{ $support_username }

stars-invoice-title =
    💳 Оплатить

success-payment = Оплата прошла успешно

crypto-invoice-title = Оплатить { $price }₽

message-text =
    <b>Текст сообщения:</b>

    <b>{ $message_text }</b>

hidden-username = Cкрыт

ban-list-menu-text = ⛔️ <b>Здесь вы можете посмотреть список сообщений, за которые вы заблокировали пользователя</b>

premium-text-faker =
    ⭐️ <b>Пользователь —</b> <b>{ $link }</b>
    🆔 <b>ID</b> — <code>{ $user_id }</code>
    📌 <b>Юзернейм —</b> { $username ->
                                        [no] <b>Нету</b>
                                        *[other] <b>{ $username }</b>
                            }
    🎗 <b>Ранг —</b> <code>{ $role ->
                            [member] <code>Пользователь</code>
                            [admin] <code>Админ</code> 🅰️
                            *[other] <code>Пользователь</code>
                        }</code> | <code>{ $top_place }</code>

    ➖➖➖➖➖➖➖➖➖➖➖➖

    📬 <b>Отправлено сообщений</b> — <code>{ $message_sent }</code>
    └ <i>Сегодня</i> — <code>{ $message_sent_today }</code>
    💬 <b>Получено сообщений</b> — <code>{ $message_got }</code>
    └ <i>Сегодня</i> — <code>{ $message_got_today }</code>

    ➖➖➖➖➖➖➖➖➖➖➖➖

    <b>📅 Регистрация -</b> <code>{ $created_at }</code>
    👤 <b>Пригласил</b> — { $referral_text ->
                                            [no] <b>Нет</b>
                                            *[other] { $referral_text }
                            }
    <b>🌐 Язык -</b> { $locale ->
                                 [ru] <b>Русский</b> 🇷🇺
                                 [en] <b>Английский</b> 🇬🇧
                                 [de] <b>Немецкий</b> 🇩🇪
                                 [ua] <b>Украинский</b> 🇺🇦
                                *[other] <b>Русский</b> 🇷🇺
                        }

show-premium-username-callback-off =
    Теперь имя отправителя не будет видно под анонимным сообщением. Его можно будет увидеть нажав на кнопку

show-premium-username-callback-on =
    Теперь имя отправителя будет видно под анонимным сообщением. Также при нажатии можно будет увидеть подробную информацию

username-exist-already = ⚠️ <b>Такой никнейм уже существует</b>

profile-wrong-input-username = <b>⚠️ Никнейм может состоять только из букв английского алфавита, цифр а также _ Первым символом всегда идет буква английского алфавита</b>

wrong-hello-message = <b>⚠️ Длина приветствия должна быть меньше 1000 символов</b>