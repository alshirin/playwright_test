from enum import Enum, auto


class BrowserType(Enum):
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    SAFARI = "webkit"


class AccountPurpose(Enum):
    BUSINESS = "Business"
    PERSONAL = "Personal"


class WithdrawOption(Enum):
    CASH = "Cash"
    CARD = "Card"
    CRYPTO = "Cryptocurrency"
