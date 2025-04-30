from playwright.sync_api import expect, Locator  # type: ignore
from typing import List, Dict, Optional

import enums as e
from .base_page import BasePage


class HomePage(BasePage):
    URL = "https://qatest.datasub.com"

    def __init__(self, page):
        super().__init__(page)
        self.form = page.locator("#subscriptionForm")

        self.name_input = page.locator("#name")

        self.email_input = page.locator("#email")

        self.service_select = page.locator("#service")

        self.purpose_label = page.get_by_label(text="Account Purpose:")
        self.purpose_business = page.locator("#purposeBusiness")
        self.purpose_personal = page.locator("#purposePersonal")

        self.withdrawal_label = page.get_by_label(text="Withdrawal Options:")

        self.wo_cash = page.locator("#withdrawCash")
        self.wo_card = page.locator("#withdrawCard")
        self.wo_crypto = page.locator("#withdrawCrypto")
        self._withdrawal_locators: Dict[e.WithdrawOption, Locator] = {
            e.WithdrawOption.CASH: self.wo_cash,
            e.WithdrawOption.CARD: self.wo_card,
            e.WithdrawOption.CRYPTO: self.wo_crypto,
        }

        self.message_input = page.locator("#message")
        self.request_quote_button = page.get_by_role("button", name="Request A Quote")

        self.request_status = page.locator("#formStatus")

    def load(self) -> None:
        self.visit(self.URL)

    def fill_form(
        self,
        name: str,
        email: str,
        service: str,
        purpose: Optional[e.AccountPurpose],
        withdrawals: Optional[List[e.WithdrawOption]],
        message: str,
    ) -> None:
        self.form.scroll_into_view_if_needed()
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.service_select.select_option(service)
        if purpose:
            (
                self.purpose_business.check()
                if purpose == e.AccountPurpose.BUSINESS
                else self.purpose_personal.check()
            )

        if withdrawals:
            for option in withdrawals:
                if option in self._withdrawal_locators:
                    self._withdrawal_locators[option].check()

        self.message_input.fill(message)

    def get_selected_service_option(self) -> Locator:
        self.form.scroll_into_view_if_needed()
        return self.service_select.locator("option:checked")

    def get_element_height(self, element: Locator) -> str:
        self.form.scroll_into_view_if_needed()
        return element.evaluate("el => getComputedStyle(el).getPropertyValue('height')")

    def request_quote_click(self) -> None:
        self.form.scroll_into_view_if_needed()
        self.request_quote_button.click()

    def assert_default_form_state(self, submitted: bool = False) -> None:
        self.form.scroll_into_view_if_needed()

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

        def assert_checkbox_ready(checkbox: Locator) -> None:
            expect(checkbox).to_be_visible()
            expect(checkbox).to_be_enabled()
            expect(checkbox).not_to_be_checked()

        def assert_radio_ready(radio: Locator) -> None:
            expect(radio).to_be_visible()
            expect(radio).to_be_enabled()
            expect(radio).not_to_be_checked()

        def assert_request_quote_button_ready(
            request_quote_button: Locator, button_text: str = "Request A Quote"
        ) -> None:
            expect(request_quote_button).to_be_visible()
            expect(request_quote_button).to_be_enabled()
            expect(request_quote_button).to_have_text(button_text)

        assert_text_input_ready(self.name_input)
        assert_text_input_ready(self.email_input)

        assert_combo_service_ready(self.service_select)

        for option in self._withdrawal_locators.values():
            assert_checkbox_ready(option)

        assert_radio_ready(self.purpose_business)
        assert_radio_ready(self.purpose_personal)

        assert_text_input_ready(self.message_input)

        assert_request_quote_button_ready(self.request_quote_button)

        self.assert_request_status(submitted=submitted)

    def assert_filled_form_state(
        self,
        name: str,
        email: str,
        service: str,
        purpose: Optional[e.AccountPurpose],
        withdrawals: Optional[List[e.WithdrawOption]],
        message: str,
    ) -> None:
        self.form.scroll_into_view_if_needed()

        expect(self.name_input).to_have_value(name)
        expect(self.email_input).to_have_value(email)
        expect(self.get_selected_service_option()).to_have_text(service)
        (
            expect(self.purpose_business)
            if purpose == e.AccountPurpose.BUSINESS
            else expect(self.purpose_personal)
        )
        if withdrawals:
            for option, locator in self._withdrawal_locators.items():
                if option in withdrawals:
                    expect(locator).to_be_checked()
                else:
                    expect(locator).not_to_be_checked()
        else:
            for locator in self._withdrawal_locators.values():
                expect(locator).not_to_be_checked()
        expect(self.message_input).to_have_value(message)

    def assert_request_status(self, submitted: bool) -> None:
        self.form.scroll_into_view_if_needed()
        height = self.get_element_height(self.request_status)
        if submitted:
            assert height == "24px"
        else:
            assert height == "auto"

    def is_invalid_name(self):
        return "is-invalid" in self.name_input.get_attribute("class")

    def is_invalid_email(self):
        validation_message = self.email_input.evaluate("el => el.validationMessage")
        return validation_message != ""

    def is_invalid_service(self):
        return "is-invalid" in self.service_select.get_attribute("class")

    def is_invalid_message(self):
        return "is-invalid" in self.message_input.get_attribute("class")
