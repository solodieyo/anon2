from enum import auto, StrEnum


class MailingStatus(StrEnum):
    FINISH = auto()
    PENDING = auto()
    FAILED = auto()


class MailingType(StrEnum):
    DEFAULT = auto()
    PREMIUM = auto()
    ALL = auto()
