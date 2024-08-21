from enum import auto, StrEnum


class Locale(StrEnum):
    RU = auto()
    EN = auto()
    DE = auto()
    UK = auto()

    DEFAULT_LOCALE = RU
