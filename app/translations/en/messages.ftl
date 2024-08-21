choice-language-text = <b>Choose language</b>

main-menu-text =
    🔗 <b>Start receiving anonymous messages right now!</b>

    <i>Your personal link:</i>
    👉 { $link }

    Share this link in your <b>Telegram</b> ● <b>Instagram</b> ● <b>TikTok</b> or other social media to start receiving messages 💬

profile-menu-user-kek =
    ⭐️ <b>User —</b> <b>{ $link }</b>
    📌 <b>Username —</b> <code>{ $username }</code>
    🎗 <b>Rank —</b> <code>{ $role ->
                                    [member] <code>User</code>
                                    [admin] <code>Admin</code> 🅰️
                                    *[other] <code>User</code>
                                }</code> | <code>{ $top_place }</code>

    ➖➖➖➖➖➖➖➖➖➖➖➖

    📬 <b>Messages sent</b> — <code>{ $sent_messages_count }</code>
    └ <i>Today</i> — <code>{ $message_sent_today }</code>
    💬 <b>Messages received</b> — <code>{ $received_messages_count }</code>
    └ <i>Today</i> — <code>{ $message_received_today }</code>

profile-settings =
    ⚙️<b>Settings</b>

    <b>Language</b> - 🇬🇧<b>English</b>

profile-change-hello =
    👋 <b>Here you can set your greeting</b>
    Currently, your greeting looks like this:

    { $hello_message ->
                    *[other] <b>{ $hello_message }</b>
                      [no]  <i>No message set</i>
    }

profile-create-username =
    📍 <b>Here you can set a username for your link</b>

    Your current link for receiving anonymous messages looks like this:

    <pre language="link">t.me/{ $bot_username }?start={ $user_id }</pre>

    And if you set a username, your link will look like this:

    <pre language="link">t.me/{ $bot_username }?start=YOUR_USERNAME</pre>

    ❗️ <b>Please note that when you change the link, the old link will no longer be active!</b>

input-anon-msg =
    ❓ Send an anonymous message to the user

     { $hello_message ->
                     *[other] <b>{ $hello_message }</b>
                      [no] <b>Write anything you want here and the user will receive the message immediately, but won't know who it's from</b>
    }

   <i>❗️Ты you can send a text, photo, video, gif, voice message, video message, sticker or music</i>

get-anon-msg =
    <b>You have a new anonymous message</b>

success-send =
    • <b>Your message has been sent! (And it has already reached the recipient)</b>

    <b>P.S. You may receive a reply to your message</b>

ban-list-menu = ️ ⛔️ <b>You have no blocked users</b>

new-message-text =
    You have received a new message:

    <b>{ $message_text }</b>

ratings-text =
    ⭐️ <b>Rating</b> — <b>{ $type ->
                            [getters] 💬 Receiver
                            *[senders] 📬 Senders
                            }</b>

    { $username1 ->
        *[other] 🥇<b>#1</b> { $username1 } — <code>{ $username1_count }</code>
        [no] 🥇<b>#1</b> xxx — <code>0</code>
    }
    { $username2 ->
        *[other] 🥈<b>#2</b> { $username2 } — <code>{ $username2_count }</code>
        [no] 🥈<b>#2</b> xxx — <code>0</code>
    }
    { $username3 ->
        *[other] 🥉<b>#3</b> { $username3 } — <code>{ $username3_count }</code>
        [no] 🥉<b>#3</b> xxx — <code>0</code>
    }
    { $username4 ->
        *[other] 🏆<b>#4</b> { $username4 } — <code>{ $username4_count }</code>
        [no] 🏆<b>#4</b> xxx — <code>0</code>
    }
    { $username5 ->
        *[other] 🏆<b>#5</b> { $username5 } — <code>{ $username5_count }</code>
        [no] 🏆<b>#5</b> xxx — <code>0</code>
    }
    { $username6 ->
        *[other] 🏆<b>#6</b> { $username6 } — <code>{ $username6_count }</code>
        [no] 🏆<b>#6</b> xxx — <code>0</code>
    }
    { $username7 ->
        *[other] 🏆<b>#7</b> { $username7 } — <code>{ $username7_count }</code>
        [no] 🏆<b>#7</b> xxx — <code>0</code>
    }
    { $username8 ->
        *[other] 🏆<b>#8</b> { $username8 } — <code>{ $username8_count }</code>
        [no] 🏆<b>#8</b> xxx — <code>0</code>
    }
    { $username9 ->
        *[other] 🏆<b>#9</b> { $username9 } — <code>{ $username9_count }</code>
        [no] 🏆<b>#9</b> xxx — <code>0</code>
    }
    { $username10 ->
        *[other] 🏆<b>#10</b> { $username10 } — <code>{ $username10_count }</code>
        [no] 🏆<b>#10</b> xxx — <code>0</code>
    }

    👤 <b>You</b> — <b>#{ $from_user_place }</b> — { $from_user_count }

profile-premium =
    ✍🏻 { $premium_active ->
                            [no] <b>You currently do not have access</b>
                            [adm] <b>Access activated forever</b>
                            *[other] <b>Access activated until { $premium_active }</b>
        }

    🛒 By purchasing this product, you gain access to view <b>information</b> about the message sender

    🔎 <b>You will be able to find out:</b>

    • <i>First Name | Last Name | ID</i>
    • <i>Username (if available)</i>
    • <i>Rank and position in the rating</i>
    • <i>Statistics of sent and received messages</i>
    • <i>Registration date</i>

    👑 <b>Choose the Premium validity period:</b>

premium-choose-pay =
    💳 <b>The purchase price will be { $price }₽</b>

    🌐 <b>Choose a payment method:</b>


premium-stars-pay-finish = ⭐️ Telegram stars

premium-pay-finish =
    ✅ <b>Invoice #{ $payment_id } for payment has been generated!</b>
    💳 <b>You are purchasing access for</b> { $payment_type ->
                                                [premium_price_day] <b>1 day</b>
                                                [premium_price_week] <b>1 week</b>
                                                *[premium_price_month] <b>1 month</b>
                                } <b>for { $price }₽</b>

    To pay, follow the link below or click the button
    <b>"💳 Pay"</b>

    { $link }

    📞 If you encounter any issues with payment, contact support — @{ $support_username }

stars-invoice-title =
    💳 Pay

success-payment = Payment successful

crypto-invoice-title = Pay { $price }₽

message-text =
    <b>Message text:</b>

    <b>{ $message_text }</b>

hidden-username = Hide

ban-list-menu-text = ⛔️ <b>Here you can view the list of messages for which you have blocked the user</b>

premium-text-faker =
    ⭐️ <b>User —</b> <b>{ $link }</b>
    🆔 <b>ID</b> — <code>{ $user_id }</code>
    📌 <b>Username —</b> { $username ->
                                        [no] <b>None</b>
                                        *[other] <b>{ $username }</b>
                            }
    🎗 <b>Rank —</b> <code>{ $role ->
                            [member] <code>Member</code>
                            [admin] <code>Admin</code> 🅰️
                            *[other] <code>Member</code>
                        }</code> | <code>{ $top_place }</code>

    ➖➖➖➖➖➖➖➖➖➖➖➖

    📬 <b>Messages Sent</b> — <code>{ $message_sent }</code>
    └ <i>Today</i> — <code>{ $message_sent_today }</code>
    💬 <b>Messages Received</b> — <code>{ $message_got }</code>
    └ <i>Today</i> — <code>{ $message_got_today }</code>

    ➖➖➖➖➖➖➖➖➖➖➖➖

    <b>📅 Registration -</b> <code>{ $created_at }</code>
    👤 <b>Referred by</b> — { $referral_text ->
                                            [no] <b>No</b>
                                            *[other] { $referral_text }
                            }
    <b>🌐 Language -</b> { $locale ->
                                 [ru] <b>Russian</b> 🇷🇺
                                 [en] <b>English</b> 🇬🇧
                                 [de] <b>German</b> 🇩🇪
                                 [ua] <b>Ukrainian</b> 🇺🇦
                                *[other] <b>Russian</b> 🇷🇺
                        }

show-premium-username-callback-off =
    Now the sender's name will not be visible under the anonymous message. It can be seen by clicking the button

show-premium-username-callback-on =
    Now the sender's name will be visible under the anonymous message. Also, by clicking, you can see detailed information

username-exist-already = <b>⚠️ This username already exists</b>

profile-wrong-input-username = <b>⚠️ The username can only consist of letters from the English alphabet, digits, and _ The first character must always be a letter from the English alphabet</b>

wrong-hello-message = <b>⚠️ The length of the greeting must be less than 1000 characters</b>
