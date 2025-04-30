from enum import Enum, auto


class BrowserType(Enum):
    CHROMIUM = auto()
    FIREFOX = auto()
    SAFARI = auto()
    EDGE = auto()


class AccountPurpose(Enum):
    BUSINESS = auto()
    PERSONAL = auto()


class WithdrawOption(Enum):
    CASH = auto()
    CARD = auto()
    CRYPTO = auto()
