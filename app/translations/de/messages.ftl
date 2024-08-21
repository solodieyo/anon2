choice-language-text = <b>Sprache wählen</b>

main-menu-text =
    🔗 <b>Beginne jetzt mit dem Empfang anonymer Nachrichten!</b>

    <i>Dein persönlicher Link:</i>
    👉 { $link }

    Teile diesen Link in deinem Profil <b>Telegram</b> ● <b>Instagram</b> ● <b>TikTok</b> oder anderen sozialen Netzwerken, um Nachrichten zu erhalten 💬

profile-menu-user-kek =
    ⭐️ <b>Benutzer —</b> <b>{ $link }</b>}
    📌 <b>Benutzername —</b> <code>{ $username }</code>
    🎗 <b>Rang —</b> <code>{ $role ->
                                    [member] <code>Benutzer</code>
                                    [admin] <code>Admin</code> 🅰️
                                    *[other] <code>Benutzer</code>
                                }</code> | <code>{ $top_place }</code>

    ➖➖➖➖➖➖➖➖➖➖➖➖

    📬 <b>Gesendete Nachrichten</b> — <code>{ $sent_messages_count }</code>
    └ <i>Heute</i> — <code>{ $message_sent_today }</code>
    💬 <b>Empfangene Nachrichten</b> — <code>{ $received_messages_count }</code>
    └ <i>Heute</i> — <code>{ $message_received_today }</code>

profile-settings =
    ⚙️<b>Einstellungen</b>

    <b>Sprache</b> - 🇩🇪<b>Deutsch</b>

profile-change-hello =
    👋 <b>Hier können Sie Ihre Begrüßung einstellen</b>

    Ihre aktuelle Begrüßung sieht so aus:

    { $hello_message ->
                    *[other] <b>{ $hello_message }</b>
                      [no]  <i>Keine Nachricht festgelegt</i>
    }


profile-create-username =
    📍 <b>Hier können Sie einen Benutzernamen für Ihren Link festlegen</b>

    Ihr aktueller Link zum Empfangen anonymer Nachrichten sieht so aus:

    <pre language="link">t.me/{ $bot_username }?start={ $user_id }</pre>

    Wenn Sie einen Benutzernamen festlegen, sieht Ihr Link so aus:

    <pre language="link">t.me/{ $bot_username }?start=IHR_BENUTZERNAME</pre>

    ❗️ <b>Beachten Sie, dass bei einer Änderung des Links der alte Link nicht mehr aktiv ist!</b>

input-anon-msg =
    ❓ Senden Sie eine anonyme Nachricht an einen Benutzer

    { $hello_message ->
                     *[other] <b>{ $hello_message }</b>
                      [no] <b>Schreiben Sie hier, was Sie wollen, und der Nutzer erhält die Nachricht sofort, weiß aber nicht, von wem sie stammt</b>
    }

   <i>❗️Ты können Sie Text, Foto, Video, Gif, Sprachnachricht, Videonachricht, Sticker oder Musik senden</i>

get-anon-msg =
    <b>Sie haben eine neue anonyme Nachricht</b>

success-send =
    • <b>Ihre Nachricht wurde gesendet! (Und sie ist bereits beim Empfänger angekommen)</b>

    <b>P.S. Sie können eine Antwort auf Ihre Nachricht erhalten</b>

ban-list-menu = ⛔️ <b>Sie haben keine blockierten Benutzer</b>
new-message-text =
    Du hast eine neue Nachricht erhalten:

    <b>{ $message_text }</b>


ratings-text =
    ⭐️ <b>Bewertung</b> — <b>{ $type ->
                            [getters] 💬 Empfänger
                            *[senders] 📬 Absender
                            }</b>

    { $username1 ->
        *[other] 🥇<b>#1</b> { $username1 } — <code>{ $username1_count }</code>
        [no] 🥇<b>#1</b> Verstecken — <code>0</code>
    }
    { $username2 ->
        *[other] 🥈<b>#2</b> { $username2 } — <code>{ $username2_count }</code>
        [no] 🥈<b>#2</b> Verstecken — <code>0</code>
    }
    { $username3 ->
        *[other] 🥉<b>#3</b> { $username3 } — <code>{ $username3_count }</code>
        [no] 🥉<b>#3</b> Verstecken — <code>0</code>
    }
    { $username4 ->
        *[other] 🏆<b>#4</b> { $username4 } — <code>{ $username4_count }</code>
        [no] 🏆<b>#4</b> Verstecken — <code>0</code>
    }
    { $username5 ->
        *[other] 🏆<b>#5</b> { $username5 } — <code>{ $username5_count }</code>
        [no] 🏆<b>#5</b> Verstecken — <code>0</code>
    }
    { $username6 ->
        *[other] 🏆<b>#6</b> { $username6 } — <code>{ $username6_count }</code>
        [no] 🏆<b>#6</b> Verstecken — <code>0</code>
    }
    { $username7 ->
        *[other] 🏆<b>#7</b> { $username7 } — <code>{ $username7_count }<code>
        [no] 🏆<b>#7</b> Verstecken — <code>0</code>
    }
    { $username8 ->
        *[other] 🏆<b>#8</b> { $username8 } — <code>{ $username8_count }</code>
        [no] 🏆<b>#8</b> Verstecken — <code>0</code>
    }
    { $username9 ->
        *[other] 🏆<b>#9</b> { $username9 } — <code>{ $username9_count }</code>
        [no] 🏆<b>#9</b> Verstecken — <code>0</code>
    }
    { $username10 ->
        *[other] 🏆<b>#10</b> { $username10 } — <code>{ $username10_count }</code>
        [no] 🏆<b>#10</b> Verstecken — <code>0</code>
    }

    👤 <b>Sie</b> — <b>#{ $from_user_place }</b> — <code>{ $from_user_count }</code>

profile-premium =
    ✍🏻 { $premium_active ->
                            [no] <b>Sie haben derzeit keinen Zugang</b>
                            [adm] <b>Zugang dauerhaft aktiviert</b>
                            *[other] <b>Zugang aktiviert bis { $premium_active }</b>
        }

    🛒 Durch den Kauf dieses Produkts erhalten Sie Zugriff auf die Ansicht von <b>Informationen</b> über den Nachrichtenabsender

    🔎 <b>Sie werden in der Lage sein zu erfahren:</b>

    • <i>Vorname | Nachname | ID</i>
    • <i>Benutzername (falls vorhanden)</i>
    • <i>Rang und Position in der Bewertung</i>
    • <i>Statistik von gesendeten und empfangenen Nachrichten</i>
    • <i>Registrierungsdatum</i>

    👑 <b>Wählen Sie die Gültigkeitsdauer von Premium:</b>

premium-choose-pay =
    💳 <b>Der Kaufpreis beträgt { $price }₽</b>

    🌐 <b>Wählen Sie eine Zahlungsmethode:</b>

premium-stars-pay-finish = ⭐️ Telegram-Sterne

premium-pay-finish =
    ✅ <b>Rechnung #{ $payment_id } zur Zahlung wurde erstellt!</b>
    💳 <b>Sie kaufen Zugang für</b> { $payment_type ->
                                                [premium_price_day] <b>1 Tag</b>
                                                [premium_price_week] <b>1 Woche</b>
                                                *[premium_price_month] <b>1 Monat</b>
                                } <b>für { $price }₽</b>

    Um zu bezahlen, folgen Sie dem Link unten oder klicken Sie auf die Schaltfläche
    <b>"💳 Bezahlen"</b>

    { $link }

    📞 Bei Problemen mit der Zahlung wenden Sie sich an den Support — @{ $support_username }

stars-invoice-title =
    💳 Bezahlen

success-payment = Zahlung erfolgreich

crypto-invoice-title = Bezahlen { $price }₽

message-text =
    <b>Nachrichtentext:</b>

    <b>{ $message_text }</b>

hidden-username = Verstecken

ban-list-menu-text = ⛔️ <b>Hier können Sie die Liste der Nachrichten anzeigen, für die Sie den Benutzer blockiert haben</b>

premium-text-faker =
    ⭐️ <b>Benutzer —</b> <b>{ $link }</b>
    🆔 <b>ID</b> — <code>{ $user_id }</code>
    📌 <b>Benutzername —</b> { $username ->
                                        [no] <b>Keiner</b>
                                        *[other] <b>{ $username }</b>
                            }
    🎗 <b>Rang —</b> <code>{ $role ->
                            [member] <code>Mitglied</code>
                            [admin] <code>Admin</code> 🅰️
                            *[other] <code>Mitglied</code>
                        }</code> | <code>{ $top_place }</code>

    ➖➖➖➖➖➖➖➖➖➖➖➖

    📬 <b>Gesendete Nachrichten</b> — <code>{ $message_sent }</code>
    └ <i>Heute</i> — <code>{ $message_sent_today }</code>
    💬 <b>Erhaltene Nachrichten</b> — <code>{ $message_got }</code>
    └ <i>Heute</i> — <code>{ $message_got_today }</code>

    ➖➖➖➖➖➖➖➖➖➖➖➖

    <b>📅 Registrierung -</b> <code>{ $created_at }</code>
    👤 <b>Empfohlen von</b> — { $referral_text ->
                                            [no] <b>No</b>
                                            *[other] { $referral_text }
                            }
    <b>🌐 Sprache -</b> { $locale ->
                                 [ru] <b>Russisch</b> 🇷🇺
                                 [en] <b>Englisch</b> 🇬🇧
                                 [de] <b>Deutsch</b> 🇩🇪
                                 [ua] <b>Ukrainisch</b> 🇺🇦
                                *[other] <b>Russisch</b> 🇷🇺
                        }

show-premium-username-callback-off =
    Jetzt wird der Name des Absenders nicht unter der anonymen Nachricht sichtbar sein. Er kann durch Klicken auf die Schaltfläche gesehen werden

show-premium-username-callback-on =
    Jetzt wird der Name des Absenders unter der anonymen Nachricht sichtbar sein. Auch durch Klicken können Sie detaillierte Informationen sehen

username-exist-already = <b>⚠️ Dieser Benutzername existiert bereits</b>

profile-wrong-input-username = <b>⚠️ Der Benutzername kann nur aus Buchstaben des englischen Alphabets, Ziffern und _ bestehen Der erste Buchstabe muss immer ein Buchstabe des englischen Alphabets sein</b>

wrong-hello-message = <b>⚠️ Die Länge der Begrüßung muss weniger als 1000 Zeichen betragen</b>
