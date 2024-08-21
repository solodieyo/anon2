
statistics-common-text =
    🏛 <b>{ $date_type }</b> <code>{ $selected_date }</code>

    👥 Пользователей в боте — <code>{ $users_count }</code> — <code>+{ $new_users }</code>
    💣 Заблокировавших бота — <code>{ $blocked_users }</code> — <code>+{ $blocked_users_count }</code>
    💳 Пополнения — <code>{ $payments_sum }₽</code> — <code>{ $payments_count } шт.</code>

statistics-languages-text =
    🏛 <b>{ $date_type }</b> <code>{ $selected_date }</code>

    💳 <b>Пополнения</b> <code>({ $payments_count })</code>
    🇷🇺 <b>{ $new_ru_payments_percent }%</b> - <code>{ $ru_payments_sum }₽ { $ru_payments_count}</code>
    🇬🇧 <b>{ $new_en_payments_percent }%</b> - <code>{ $en_payments_sum }₽ { $en_payments_count}</code>
    🇺🇦 <b>{ $new_uk_payments_percent }%</b> - <code>{ $uk_payments_sum }₽ { $uk_payments_count}</code>
    🇩🇪 <b>{ $new_de_payments_percent }%</b> - <code>{ $de_payments_sum }₽ { $de_payments_count}</code>

    👥 <b>Новые пользователи</b> <code>({ $new_users })</code>
    🇷🇺 <b>{ $new_ru_users_percent }%</b> — <code>{ $new_ru_users_count }</code>
    🇬🇧 <b>{ $new_en_users_percent }%</b> — <code>{ $new_en_users_count }</code>
    🇺🇦 <b>{ $new_uk_users_percent }%</b> - <code>{ $new_uk_users_count }</code>
    🇩🇪 <b>{ $new_de_users_percent }%</b> - <code>{ $new_de_users_count }</code>

    📧 Отправлено сообщений <code>({ $sent_message_count })</code>
    🇷🇺 <b>{ $ru_sent_message_percent }%</b> — <code>{ $ru_sent_message_count }</code>
    🇬🇧 <b>{ $en_sent_message_percent }%</b> — <code>{ $en_sent_message_count }</code>
    🇺🇦 <b>{ $uk_sent_message_percent }%</b> - <code>{ $uk_sent_message_count }</code>
    🇩🇪 <b>{ $de_sent_message_percent }%</b> - <code>{ $de_sent_message_count }</code>

    📩 Получено сообщений <code>({ $received_message_count })</code>
    🇷🇺 <b>{ $ru_received_message_percent }%</b> — <code>{ $ru_received_message_count }</code>
    🇬🇧 <b>{ $en_received_message_percent }%</b> — <code>{ $en_received_message_count }</code>
    🇺🇦 <b>{ $uk_received_message_percent }%</b> - <code>{ $uk_received_message_count }</code>
    🇩🇪 <b>{ $de_received_message_percent }%</b> - <code>{ $de_received_message_count }</code>


statistic-payments-text =

    🏛 <b>{ $date_type }</b> <code>{ $selected_date }</code>

    💳 <b>Пополнения</b> - <code>{ $payments_sum }₽</code> - <code>({ $payments_count })</code>
    ❌ <b>Не оплаченные</b> — <code>{ $payments_pending_sum }₽</code> — <code>{ $payments_pending_count } шт.</code>
    ⏳ В среднем на оплату — <code>{ $payments_time }.</code>

    ⚡️ CryptoBot — <code>{ $crypto_bot_sum }₽</code> — <code>{ $crypto_bot_count }шт.</code>
    ⭐️ Звездочки — <code>{ $stars_sum }₽</code> —  <code>{ $stars_count } шт.</code>


message-admin-text =
    <b>Вопрос { $message_id }</b>

    <b>От кого -</b><a href="tg://user?id={ $from_user_id }">{ $from_user }</a>
    <b>Кому -</b><a href="tg://user?id={ $to_user_id }">{ $to_user }</a>

    <b>Дата - { $message_date } (МСК)</b>

    <b>Текст:</b>

    { $message_text }

admin-start-text =
    🔸 <u>Вход прошел успешно</u>

    👥 <b>Кол-во пользователей —</b> { $users_count }
    └ <i>Сегодня</i> — +{ $join_today }
    📬 <b>Кол-во сообщений</b> — { $messages_count }
    └ <i>Сегодня</i> — +{ $message_today }

admin-users-main-text =
    👤<b>Всего пользователей: { $users_count }</b>

    🌎<b>Статистика используемых языков</b>
    ➖🇷🇺 { $ru_total_users } » { $ru_percent }%
    ➖🇺🇦 { $ua_total_users } » { $ua_percent }%
    ➖🇬🇧 { $en_total_users } » { $en_percent }%
    ➖🇩🇪 { $de_total_users } » { $de_percent }%

    ✳️<b>Введите ID/username или перешлите сообщение пользователя, чтобы посмотреть информацию</b>


admin-user-info-text =
    ⭐️ <b>Пользователь —</b> <b>{ $link }</b>
    🆔<b>ID</b> <code>{ $user_id }</code>
    📌 <b>Никнейм —</b> <code>{ $username }</code>
    🎗 <b>Ранг —</b> <code>{ $role ->
                                 [member] Пользователь
                                 [admin] Админ 🅰️
                                *[other] Пользователь
                                            }</code> | <code>{ $top_place }</code>
    ➖➖➖➖➖➖➖➖➖➖➖➖

    📬 <b>Отправлено сообщений</b> — <code>{ $message_sent }</code>
    └ <i>Сегодня</i> — <code>{ $message_sent_today }</code>
    💬 <b>Получено сообщений</b> — <code>{ $message_got }</code>
    └ <i>Сегодня</i> — <code>{ $message_got_today }</code>

    ➖➖➖➖➖➖➖➖➖➖➖➖

    <b>📅 Регистрация -</b> <code>{ $created_at }</code>
    <b>🌐 Язык -</b> { $locale ->
                                 [ru] 🇷🇺
                                 [en] 🇬🇧
                                 [de] 🇩🇪
                                 [ua] 🇺🇦
                                *[other] 🇷🇺
                        }

last-activity =
    ⏳ <b>Последняя активность</b> — <b>{ $last_activity }</b>

broadcast-text =
    ✉️ <b>Рассылка #{ $mailing_id }</b>

    👥 <b>Всего пользователей — { $count_users }</b>
    ╭ <b>Статус отправки:</b> { $status ->
                                [finish] ✅ <b>Завершено</b>
                                [canceled] ❌ <b>Отменена</b>
                                *[pending] 📶 <b>Отправляется</b>
                        }
    ├  <b>Отправлено: 👥 { $success_sent }</b>
    ╰ <b>Забанено: 🗑 { $failed_sent }</b>

    { $status ->
                [pending] ◾️◾️◾️◽️◽️◽️◽️◽️◽️◽️
                [finish] ◾️◾️◾️◾️◾️◾️◾️◾️◾️ ✔️
                *[canceled] ◽️◽️◽️◽️◽️◽️◽️◽️◽️◽️❌
    }

    ╭ <b>Дата начала: { $mailing_date } (МСК)</b>
    ╰ <b>Дата завершения: { $finish_date ->
                                        *[other] { $finish_date }
                                         [no] ...
                        } </b><b>(МСК)</b>

mailing-text = <b>Поделиться информацией о рассылке</b> - { $link }


all-messages-text =

    📅 <b>Все сообщения</b>

    ✉️ <b>Всего сообщений: { $message_count }</b>
