from enum import auto, StrEnum


class PaymentsStatus(StrEnum):
    SUCCESS = auto()
    PENDING = auto()
    CANCEL = auto()
