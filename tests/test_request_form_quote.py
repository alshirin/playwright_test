import pytest

from pages.quote_page import QuotePage

SLEEP_TIMER = 5


@pytest.mark.positive
@pytest.mark.happy_path_quote
@pytest.mark.parametrize(
    "name, email, service, message",
    [
        ("John Doe", "john@example.com", "Service 1", "Message A"),
        ("Jane Smith", "jane@domain.com", "Service 2", "Message B"),
        ("Foo Bar", "foo@bar.com", "Service 3", "Message C"),
    ],
)
def test_happy_path(page, sleep_short, name, email, service, message):
    quote_page = QuotePage(page)
    quote_page.load()
    quote_page.assert_default_form_state(submitted=False)

    quote_page.fill_form(name, email, service, message)
    quote_page.assert_filled_form_state(name, email, service, message)

    quote_page.request_quote_click()

    sleep_short(1)

    quote_page.assert_submitted_state(success_message="Форма отправлена успешно!")
    quote_page.assert_default_form_state(submitted=True)
