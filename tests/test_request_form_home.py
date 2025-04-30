import pytest

import enums as e
from pages.home_page import HomePage

SLEEP_TIMER = 5


@pytest.mark.negative
def test_submit_unfilled_form(page, sleep_short):
    main_page = HomePage(page)
    main_page.load()
    main_page.assert_default_form_state()

    main_page.request_quote_click()
    sleep_short(SLEEP_TIMER)

    assert None  # TODO: add negative checks


# @pytest.mark.positive
@pytest.mark.happy_path_home
@pytest.mark.parametrize(
    "name, email, service, purpose, withdrawals, message",
    [
        (
            "John Doe",
            "john@example.com",
            "Select B Service",
            e.AccountPurpose.BUSINESS,
            None,
            "Message A",
        ),
        (
            "Jane Smith",
            "jane@domain.com",
            "Select C Service",
            e.AccountPurpose.BUSINESS,
            [e.WithdrawOption.CARD],
            "Message B",
        ),
        (
            "Foo Bar",
            "foo@bar.com",
            "Select D Service",
            None,
            [e.WithdrawOption.CASH, e.WithdrawOption.CARD, e.WithdrawOption.CRYPTO],
            "Message C",
        ),
    ],
)
def test_happy_path(
    page, sleep_short, name, email, service, purpose, withdrawals, message
):
    home_page = HomePage(page)
    home_page.load()

    home_page.assert_default_form_state(submitted=False)

    home_page.fill_form(name, email, service, purpose, withdrawals, message)
    home_page.assert_filled_form_state(name, email, service, purpose, withdrawals, message)

    home_page.request_quote_click()

    sleep_short(1)

    home_page.assert_submitted_state(success_message="Форма отправлена.")
    home_page.assert_default_form_state(submitted=True)
