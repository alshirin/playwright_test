from playwright.sync_api import Page, expect  # type: ignore


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def visit(self, url: str) -> None:
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()
