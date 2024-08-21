from dataclasses import dataclass


@dataclass
class PricesDTO:
	price_day: int
	price_week: int
	price_month: int
	price_forever: int