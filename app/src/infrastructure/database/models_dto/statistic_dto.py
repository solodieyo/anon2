from dataclasses import dataclass


@dataclass
class CommonStatisticDTO:
	date_type: str
	selected_date: str
	new_users: int
	users_count: int
	blocked_users: int
	blocked_users_count: int
	payments_sum: float
	payments_count: int


@dataclass
class LanguageStatisticDTO:
	date_type: str
	selected_date: str
	new_users: int
	payments_count: int
	ru_payments_count: int
	en_payments_count: int
	uk_payments_count: int
	de_payments_count: int
	ru_payments_sum: float
	en_payments_sum: float
	uk_payments_sum: float
	de_payments_sum: float
	new_ru_users_count: int
	new_en_users_count: int
	new_uk_users_count: int
	new_de_users_count: int
	sent_message_count: int
	ru_sent_message_count: int
	en_sent_message_count: int
	uk_sent_message_count: int
	de_sent_message_count: int
	received_message_count: int
	ru_received_message_count: int
	en_received_message_count: int
	uk_received_message_count: int
	de_received_message_count: int

	def __post_init__(self):
		self.new_ru_payments_percent = self._calculate_percent(self.ru_payments_count, self.payments_count)
		self.new_en_payments_percent = self._calculate_percent(self.en_payments_count, self.payments_count)
		self.new_uk_payments_percent = self._calculate_percent(self.uk_payments_count, self.payments_count)
		self.new_de_payments_percent = self._calculate_percent(self.de_payments_count, self.payments_count)
		self.new_ru_users_percent = self._calculate_percent(self.new_ru_users_count, self.new_users)
		self.new_en_users_percent = self._calculate_percent(self.new_en_users_count, self.new_users)
		self.new_uk_users_percent = self._calculate_percent(self.new_uk_users_count, self.new_users)
		self.new_de_users_percent = self._calculate_percent(self.new_de_users_count, self.new_users)
		self.ru_sent_message_percent = self._calculate_percent(self.ru_sent_message_count, self.sent_message_count)
		self.en_sent_message_percent = self._calculate_percent(self.en_sent_message_count, self.sent_message_count)
		self.uk_sent_message_percent = self._calculate_percent(self.uk_sent_message_count, self.sent_message_count)
		self.de_sent_message_percent = self._calculate_percent(self.de_sent_message_count, self.sent_message_count)
		self.ru_received_message_percent = self._calculate_percent(self.ru_received_message_count,
																   self.received_message_count)
		self.en_received_message_percent = self._calculate_percent(self.en_received_message_count,
																   self.received_message_count)
		self.uk_received_message_percent = self._calculate_percent(self.uk_received_message_count,
																   self.received_message_count)
		self.de_received_message_percent = self._calculate_percent(self.de_received_message_count,
																   self.received_message_count)

	@staticmethod
	def _calculate_percent(numerator, denominator):
		if denominator == 0:
			return 0.0
		return round((numerator / denominator) * 100, 2)


@dataclass
class PreviewStatistic:
	count_users: int
	count_messages: int
	users_today: int
	message_today: int


@dataclass
class UsersStatisticDTO:
	users_count: int = 0
	ru_count: int = 0
	ua_count: int = 0
	en_count: int = 0
	de_count: int = 0
	ru_percent: float = 0
	ua_percent: float = 0
	en_percent: float = 0
	de_percent: float = 0

	def __post_init__(self):
		self.ru_percent = round((self.ru_count / self.users_count) * 100, 2)
		self.ua_percent = round((self.ua_count / self.users_count) * 100, 2)
		self.en_percent = round((self.en_count / self.users_count) * 100, 2)
		self.de_percent = round((self.de_count / self.users_count) * 100, 2)


@dataclass
class UserMessageStatisticDTO:
	message_sent_count: int = 0
	message_sent_today: int = 0
	message_got_count: int = 0
	message_got_today: int = 0


@dataclass
class PaymentsDTO:
	date_type: str
	selected_date: str
	payments_sum: float
	payments_count: int
	payments_not_success_sum: float
	payments_not_success_count: int
	payments_time: str
	crypto_bot_sum: float
	crypto_bot_count: int
	stars_sum: float
	stars_count: int