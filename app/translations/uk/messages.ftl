choice-language-text = <b>Оберіть мову</b>

main-menu-text =
    🔗 <b>Почніть отримувати анонімні повідомлення прямо зараз!</b>

    <i>Ваше особисте посилання:</i>
    👉 { $link }

    Розмістіть це посилання у своєму профілі <b>Telegram</b> ● <b>Instagram</b> ● <b>TikTok</b> або інших соц. мережах, щоб почати отримувати повідомлення 💬

profile-menu-user-kek =
    ⭐️ <b>Користувач —</b> <b>{ $link }</b>
    📌 <b>Ім'я користувача —</b> <code>{ $username }</code>
    🎗 <b>Ранг —</b> <code>{ $role ->
                                        [member] <code>Користувач</code>
                                        [admin] <code>Адмін</code> 🅰️
                                        *[other] <code>Користувач</code>
                                    }</code> | <code>{ $top_place }</code>

    ➖➖➖➖➖➖➖➖➖➖➖➖

    📬 <b>Відправлено повідомлень</b> — <code>{ $sent_messages_count }</code>
    └ <i>Сьогодні</i> — <code>{ $message_sent_today }</code>
    💬 <b>Отримано повідомлень</b> — <code>{ $received_messages_count }</code>
    └ <i>Сьогодні</i> — <code>{ $message_received_today }</code>

profile-settings =
    ⚙️<b>Налаштування</b>

    <b>Мова</b> - 🇺🇦<b>Українська</b>

profile-change-hello =
    👋 <b>Тут ви можете встановити привітання</b>

    Зараз ваше привітання виглядає так:

    { $hello_message ->
                    *[other] <b>{ $hello_message }</b>
                      [no]  <i>Повідомлення не встановлено</i>
    }

profile-create-username =
    📍 <b>?Тут ви можете встановити нікнейм для вашого посилання</b>

    Зараз ваше посилання для отримання анонімних повідомлень виглядає так:

    <pre language="link">t.me/{ $bot_username }?start={ $user_id }</pre>

    А якщо ви встановите нікнейм, то ваше посилання буде виглядати так:

    <pre language="link">t.me/{ $bot_username }?start=ВАШ_НІКНЕЙМ</pre>

    ❗️ <b>Зверніть увагу, що при зміні посилання, старе посилання перестане бути активним!</b>

input-anon-msg =
    ❓ Надішли анонімне повідомлення для користувача

    { $hello_message ->
                     *[other] <b>{ $hello_message }</b>
                      [no] <b>Напиши сюди все, що хочеш, а користувач одразу отримає це повідомлення, але не знатиме від кого воно</b>
    }

    <i>❗️Ты можеш відправити текст, фото, відео, гіфку, голосове повідомлення, відеоповідомлення, стікер або музику</i>

get-anon-msg =
    <b>У вас нове анонімне повідомлення</b>

success-send =
    • <b>Ваше повідомлення було відправлено! (І воно вже дісталося одержувачу)</b>

    <b>P.S. Вам може прийти відповідь на повідомлення</b>

ban-list-menu = ⛔️ <b>У вас немає заблокованих користувачів</b>

new-message-text =
    Ви отримали нове повідомлення:

    <b>{ $message_text }</b>

ratings-text =
    ⭐️ <b>Рейтинг</b> — <b>{ $type ->
                            [getters] 💬 Отримувачі
                            *[senders] 📬 Відправники
                            }</b>

    { $username1 ->
        *[other] 🥇<b>#1 </b>{ $username1 } — <code>{ $username1_count }</code>
        [no] 🥇<b>#1 </b>прихований — <code>0</code>
    }
    { $username2 ->
        *[other] 🥈<b>#2 </b>{ $username2 } — <code>{ $username2_count }</code>
        [no] 🥈<b>#2 </b>прихований — <code>0</code>
    }
    { $username3 ->
        *[other] 🥉<b>#3 </b>{ $username3 } — <code>{ $username3_count }</code>
        [no] 🥉<b>#3 </b>прихований — <code>0</code>
    }
    { $username4 ->
        *[other] 🏆<b>#4 </b>{ $username4 } — <code>{ $username4_count }</code>
        [no] 🏆<b>#4 </b>прихований — <code>0</code>
    }
    { $username5 ->
        *[other] 🏆<b>#5 </b>{ $username5 } — <code>{ $username5_count }</code>
        [no] 🏆<b>#5 </b>прихований — <code>0</code>
    }
    { $username6 ->
        *[other] 🏆<b>#6 </b>{ $username6 } — <code>{ $username6_count }</code>
        [no] 🏆<b>#6 </b>прихований — <code>0</code>
    }
    { $username7 ->
        *[other] 🏆<b>#7 </b>{ $username7 } — <code>{ $username7_count }</code>
        [no] 🏆<b>#7 </b>прихований — <code>0</code>
    }
    { $username8 ->
        *[other] 🏆<b>#8 </b>{ $username8 } — <code>{ $username8_count }</code>
        [no] 🏆<b>#8 </b>прихований — <code>0</code>
    }
    { $username9 ->
        *[other] 🏆<b>#9 </b>{ $username9 } — <code>{ $username9_count }</code>
        [no] 🏆<b>#9 </b>прихований — <code>0</code>
    }
    { $username10 ->
        *[other] 🏆<b>#10</b> { $username10 } — <code>{ $username10_count }</code>
        [no] 🏆<b>#10</b> прихований — <code>0</code>
    }

    👤 <b>Ви</b> — <b>#{ $from_user_place }</b> — <code>{ $from_user_count }</code>

profile-premium =
    ✍🏻 { $premium_active ->
                            [no] <b>Зараз у вас немає доступу</b>
                            [adm] <b>Доступ активовано назавжди</b>
                            *[other] <b>Доступ активовано до { $premium_active }</b>
        }

    🛒 Купуючи цей товар, ви отримуєте доступ до перегляду <b>інформації</b> про відправника повідомлень

    🔎 <b>Ви зможете дізнатися:</b>

    • <i>Ім'я | Прізвище | ID</i>
    • <i>Юзернейм (якщо присутній)</i>
    • <i>Ранг і місце в рейтингу</i>
    • <i>Статистику відправлень і отримань повідомлень</i>
    • <i>Дату реєстрації</i>

    👑 <b>Виберіть термін дії Premium:</b>

premium-choose-pay =
    💳 <b>Вартість покупки складе { $price }₽</b>

    🌐 <b>Виберіть спосіб оплати:</b>

premium-stars-pay-finish = ⭐️ Telegram stars

premium-pay-finish =
    ✅ <b>Рахунок #{ $payment_id } на оплату сформовано!</b>
    💳 <b>Ви купуєте доступ на</b> { $payment_type ->
                                                [premium_price_day] <b>1 день</b>
                                                [premium_price_week] <b>1 тиждень</b>
                                                *[premium_price_month] <b>1 місяць</b>
                                } <b>за { $price }₽</b>

    Для оплати перейдіть за посиланням нижче або натисніть на кнопку
    <b>"💳 Оплатити"</b>

    { $link }

    📞 У разі виникнення проблем з оплатою зверніться до підтримки — @{ $support_username }

stars-invoice-title =
    💳 Сплатити

success-payment = Оплата пройшла успішно

crypto-invoice-title = Оплатити { $price }₽

message-text =
    <b>Текст повідомлення:</b>

    <b>{ $message_text }</b>

hidden-username = прихований

ban-list-menu-text = ⛔️ <b>Тут ви можете переглянути список повідомлень, за які ви заблокували користувача</b>

premium-text-faker =
    ⭐️ <b>Користувач —</b> <b>{ $link }</b>
    🆔 <b>ID</b> — <code>{ $user_id }</code>
    📌 <b>Юзернейм —</b> { $username ->
                                        [no] <b>Немає</b>
                                        *[other] <b>{ $username }</b>
                            }
    🎗 <b>Ранг —</b> <code>{ $role ->
                            [member] <code>Користувач</code>
                            [admin] <code>Адмін</code> 🅰️
                            *[other] <code>Користувач</code>
                        }</code> | <code>{ $top_place }</code>

    ➖➖➖➖➖➖➖➖➖➖➖➖

    📬 <b>Відправлено повідомлень</b> — <code>{ $message_sent }</code>
    └ <i>Сьогодні</i> — <code>{ $message_sent_today }</code>
    💬 <b>Отримано повідомлень</b> — <code>{ $message_got }</code>
    └ <i>Сьогодні</i> — <code>{ $message_got_today }</code>

    ➖➖➖➖➖➖➖➖➖➖➖➖

    <b>📅 Реєстрація -</b> <code>{ $created_at }</code>
    👤 <b>Запросив</b> — { $referral_text ->
                                            [no] <b>Нет</b>
                                            *[other] { $referral_text }
                            }
    <b>🌐 Мова -</b> { $locale ->
                                 [ru] <b>Російська</b> 🇷🇺
                                 [en] <b>Англійська</b> 🇬🇧
                                 [de] <b>Німецька</b> 🇩🇪
                                 [ua] <b>Українська</b> 🇺🇦
                                *[other] <b>Російська</b> 🇷🇺
                        }

show-premium-username-callback-off =
    Тепер ім'я відправника не буде видно під анонімним повідомленням. Його можна буде побачити, натиснувши на кнопку

show-premium-username-callback-on =
    Тепер ім'я відправника буде видно під анонімним повідомленням. Також при натисканні можна буде побачити детальну інформацію

username-exist-already = <b>⚠️ Такий нікнейм вже існує</b>

profile-wrong-input-username = <b>⚠️ Нікнейм може складатися тільки з літер англійського алфавіту, цифр та _ Першим символом завжди має бути літера англійського алфавіту</b>

wrong-hello-message = <b>⚠️ Довжина привітання має бути менше 1000 символів</b>
