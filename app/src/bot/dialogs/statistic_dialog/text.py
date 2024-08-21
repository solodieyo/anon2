from aiogram_i18n import I18nContext


def get_statistic_text(i18n: I18nContext, statistic, statistic_type: str) -> str:
    texts = {
        'common_statistic': lambda: i18n.get(
            'statistics-common-text',
            'ru',
            selected_date=statistic.selected_date,
            date_type=statistic.date_type,
            new_users=statistic.new_users,
            users_count=statistic.users_count,
            payments_count=statistic.payments_count,
            payments_sum=statistic.payments_sum,
            blocked_users=statistic.blocked_users,
            blocked_users_count=statistic.blocked_users_count
        ),
        'languages_statistic': lambda: i18n.get(
            'statistics-languages-text',
            'ru',
            date_type=statistic.date_type,
            selected_date=statistic.selected_date,
            payments_count=statistic.payments_count,
            new_ru_payments_percent=statistic.new_ru_payments_percent,
            new_en_payments_percent=statistic.new_en_payments_percent,
            new_de_payments_percent=statistic.new_de_payments_percent,
            new_uk_payments_percent=statistic.new_uk_payments_percent,
            ru_payments_sum=statistic.ru_payments_sum,
            ru_payments_count=statistic.ru_payments_count,
            en_payments_sum=statistic.en_payments_sum,
            en_payments_count=statistic.en_payments_count,
            de_payments_sum=statistic.de_payments_sum,
            de_payments_count=statistic.de_payments_count,
            uk_payments_sum=statistic.uk_payments_sum,
            uk_payments_count=statistic.uk_payments_count,
            new_users=statistic.new_users,
            new_ru_users_percent=statistic.new_ru_users_percent,
            new_ru_users_count=statistic.new_ru_users_count,
            new_en_users_percent=statistic.new_en_users_percent,
            new_en_users_count=statistic.new_en_users_count,
            new_uk_users_percent=statistic.new_uk_users_percent,
            new_uk_users_count=statistic.new_uk_users_count,
            new_de_users_percent=statistic.new_de_users_percent,
            new_de_users_count=statistic.new_de_users_count,
            sent_message_count=statistic.sent_message_count,
            ru_sent_message_percent=statistic.ru_sent_message_percent,
            ru_sent_message_count=statistic.ru_sent_message_count,
            en_sent_message_percent=statistic.en_sent_message_percent,
            en_sent_message_count=statistic.en_sent_message_count,
            uk_sent_message_percent=statistic.uk_sent_message_percent,
            uk_sent_message_count=statistic.uk_sent_message_count,
            de_sent_message_percent=statistic.de_sent_message_percent,
            de_sent_message_count=statistic.de_sent_message_count,
            received_message_count=statistic.received_message_count,
            ru_received_message_percent=statistic.ru_received_message_percent,
            ru_received_message_count=statistic.ru_received_message_count,
            en_received_message_percent=statistic.en_received_message_percent,
            en_received_message_count=statistic.en_received_message_count,
            uk_received_message_percent=statistic.uk_received_message_percent,
            uk_received_message_count=statistic.uk_received_message_count,
            de_received_message_percent=statistic.de_received_message_percent,
            de_received_message_count=statistic.de_received_message_count

        ),
        'payments_statistic': lambda: i18n.get(
            'statistic-payments-text',
            'ru',
            date_type=statistic.date_type,
            selected_date=statistic.selected_date,
            payments_sum=statistic.payments_sum,
            payments_count=statistic.payments_count,
            payments_pending_sum=statistic.payments_not_success_sum,
            payments_pending_count=statistic.payments_not_success_count,
            payments_time=statistic.payments_time,
            stars_sum=statistic.stars_sum,
            stars_count=statistic.stars_count,
            crypto_bot_sum=statistic.crypto_bot_sum,
            crypto_bot_count=statistic.crypto_bot_count
        )
    }

    text = texts[statistic_type]()
    return text
