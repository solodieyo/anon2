from dataclasses import dataclass


@dataclass
class LocalesDTO:
	locale_en: bool
	locale_de: bool
	locale_uk: bool

	def get_disabled(self):
		en = 'en' if self.locale_en is False else None
		de = 'de' if self.locale_de is False else None
		uk = 'uk' if self.locale_uk is False else None
		return en, de, uk