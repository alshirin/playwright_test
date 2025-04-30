import pytest

from pages.quote_page import QuotePage

SLEEP_TIMER = 5


# @pytest.mark.positive
# def test_quote_form_initial_state(page, sleep_short):
#     quote_page = QuotePage(page)
#     quote_page.load()
#     # sleep_short(SLEEP_TIMER)
#     quote_page.assert_initial_state()
#     # sleep_short(SLEEP_TIMER)
#
#
# @pytest.mark.positive
# def test_form_filling(page, sleep_short):
#     quote_page = QuotePage(page)
#     quote_page.load()
#     # sleep_short(SLEEP_TIMER)
#     quote_page.fill_form("Test Name", "test@mail.com", "Service 1", "Test Message")
#
#     assert quote_page.name_input.input_value() == "Test Name"
#     assert quote_page.email_input.input_value() == "test@mail.com"
#     assert quote_page.get_selected_service_option().inner_text() == "Service 1"
#     assert quote_page.message_input.input_value() == "Test Message"
#
#     # sleep_short(SLEEP_TIMER)
#
#
# @pytest.mark.positive
# def test_form_submitting(page, sleep_short):
#     quote_page = QuotePage(page)
#     quote_page.load()
#     # sleep_short(SLEEP_TIMER)
#     quote_page.fill_form("Test Name", "test@mail.com", "Service 1", "Test Message")
#
#     assert quote_page.name_input.input_value() == "Test Name"
#     assert quote_page.email_input.input_value() == "test@mail.com"
#     assert quote_page.get_selected_service_option().inner_text() == "Service 1"
#     assert quote_page.message_input.input_value() == "Test Message"
#
#     # quote_page.request_quote_click()
#
#     # sleep_short(SLEEP_TIMER)


@pytest.mark.negative
def test_submit_unfilled_form(page, sleep_short):
    quote_page = QuotePage(page)
    quote_page.load()
    quote_page.assert_default_form_state()

    quote_page.request_quote_click()
    sleep_short(SLEEP_TIMER)

    assert None  # TODO: add negative checks


# @pytest.mark.positive
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
