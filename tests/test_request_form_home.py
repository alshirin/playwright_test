import pytest

import enums as e
from pages.home_page import HomePage

SLEEP_TIMER = 5


@pytest.mark.negative_home
@pytest.mark.parametrize(
    "inv_name, inv_email, inv_service, purpose, withdrawals, inv_message",
    [
        ("J", "john@@example.com", "Select A Service", None, None, "A"),
        ("J", "jane@domain..com", "Select A Service", None, None, "B"),
        ("F", "foo@!bar.com", "Select A Service", None, None, "C"),
    ],
)
def test_negative_invalid_required_fields(
    page,
    sleep_short,
    inv_name,
    inv_email,
    inv_service,
    purpose,
    withdrawals,
    inv_message,
):
    valid_values = (
        "Jane Smith",
        "jane@domain.com",
        "Select C Service",
        e.AccountPurpose.BUSINESS,
        [e.WithdrawOption.CARD],
        "Message B",
    )
    # Load page
    home_page = HomePage(page)
    home_page.load()

    # Check pre-conditions
    home_page.assert_default_form_state(submitted=False)

    # Fill form with invalid values
    home_page.fill_form(
        inv_name, inv_email, inv_service, purpose, withdrawals, inv_message
    )
    home_page.assert_filled_form_state(
        inv_name, inv_email, inv_service, purpose, withdrawals, inv_message
    )

    # Try to click Request button
    home_page.request_quote_click()

    # Check Negative scenario
    home_page.assert_request_status(submitted=False)

    assert home_page.is_invalid_name()
    assert home_page.is_invalid_email()
    assert home_page.is_invalid_service()
    assert home_page.is_invalid_message()

    # Fill form with valid values
    home_page.fill_form(*valid_values)
    home_page.assert_filled_form_state(*valid_values)

    assert not home_page.is_invalid_name()
    assert not home_page.is_invalid_email()
    assert not home_page.is_invalid_service()
    assert not home_page.is_invalid_message()


@pytest.mark.positive
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
    # Load Page
    home_page = HomePage(page)
    home_page.load()

    # Check pre-conditions
    home_page.assert_default_form_state(submitted=False)

    # Fill form with valid values
    home_page.fill_form(name, email, service, purpose, withdrawals, message)
    home_page.assert_filled_form_state(
        name, email, service, purpose, withdrawals, message
    )

    # Try to click Request button
    home_page.request_quote_click()

    sleep_short(1)

    # Check form being submitted
    home_page.assert_default_form_state(submitted=True)
