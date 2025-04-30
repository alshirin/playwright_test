from playwright.sync_api import expect, Locator  # type: ignore

from .base_page import BasePage


class QuotePage(BasePage):
    URL = "https://qatest.datasub.com/quote.html"

    def __init__(self, page):
        super().__init__(page)
        self.name_input = page.locator("#q_name")
        self.email_input = page.locator("#q_email")
        self.service_select = page.locator("#q_service")
        self.message_input = page.locator("#q_message")
        self.request_quote_button = page.get_by_role("button", name="Request A Quote")
        self.request_status = page.locator("#quoteStatus")

    def load(self) -> None:
        self.visit(self.URL)

    def fill_form(self, name: str, email: str, service: str, message: str) -> None:
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.service_select.select_option(service)
        self.message_input.fill(message)

    def get_selected_service_option(self) -> Locator:
        return self.service_select.locator("option:checked")

    def get_request_status_div_height(self) -> str:
        return self.request_status.evaluate(
            "el => getComputedStyle(el).getPropertyValue('height')"
        )

    def request_quote_click(self) -> None:
        self.request_quote_button.click()

    def assert_default_form_state(self, submitted: bool = False) -> None:
        request_status_element_height = "auto" if submitted == False else "24px"

        def assert_text_input_ready(text_input: Locator) -> None:
            expect(text_input).to_be_visible()
            expect(text_input).to_be_enabled()
            expect(text_input).to_be_empty()

        def assert_combo_service_ready(
            combo_service: Locator, initial_text: str = "Select A Service"
        ) -> None:
            expect(combo_service).to_be_visible()
            expect(combo_service).to_be_enabled()
            expect(self.get_selected_service_option()).to_have_text(initial_text)

        def assert_request_quote_button_ready(
            request_quote_button: Locator, button_text: str = "Request A Quote"
        ) -> None:
            expect(request_quote_button).to_be_visible()
            expect(request_quote_button).to_be_enabled()
            expect(request_quote_button).to_have_text(button_text)

        assert_text_input_ready(self.name_input)
        assert_text_input_ready(self.email_input)
        assert_combo_service_ready(self.service_select)
        assert_text_input_ready(self.message_input)
        assert_request_quote_button_ready(self.request_quote_button)

        assert self.get_request_status_div_height() == request_status_element_height

    def assert_filled_form_state(
        self, name: str, email: str, service: str, message: str
    ) -> None:
        expect(self.name_input).to_have_value(name)
        expect(self.email_input).to_have_value(email)
        expect(self.get_selected_service_option()).to_have_text(service)
        expect(self.message_input).to_have_value(message)

    def assert_submitted_state(self, success_message: str) -> None:
        expect(self.request_status).to_contain_text(success_message)
        assert self.get_request_status_div_height() == "24px"
