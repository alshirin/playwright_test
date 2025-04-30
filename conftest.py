import sys, shutil, os, time
from typing import Callable, Iterator

import pytest
from playwright.sync_api import sync_playwright, BrowserContext, Page  # type: ignore

import enums as e

HEADLESS = False


@pytest.fixture
def page(browser_context: BrowserContext) -> Iterator[Page]:
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture
def sleep_short() -> Callable:
    def sleeper(seconds=0):
        time.sleep(seconds)

    return sleeper


def get_edge_path() -> str:
    if sys.platform == "darwin":
        path = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
        if os.path.exists(path):
            return path
    elif sys.platform == "win32":
        return "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    elif sys.platform.startswith("linux"):
        path = shutil.which("microsoft-edge") or shutil.which("edge")
        if path:
            return path
    raise RuntimeError("Microsoft Edge not found on this system.")


def get_browser(playwright: sync_playwright, browser_type: e.BrowserType):
    if browser_type == e.BrowserType.CHROMIUM:
        return playwright.chromium.launch(headless=HEADLESS)
    elif browser_type == e.BrowserType.FIREFOX:
        return playwright.firefox.launch(headless=HEADLESS)
    elif browser_type == e.BrowserType.SAFARI:
        return playwright.webkit.launch(headless=HEADLESS)
    elif browser_type == e.BrowserType.EDGE:
        return playwright.chromium.launch(
            headless=HEADLESS, executable_path=get_edge_path()
        )
    raise ValueError(f"Unsupported browser type: {browser_type}")


@pytest.fixture(
    params=[
        e.BrowserType.CHROMIUM,
        e.BrowserType.FIREFOX,
        e.BrowserType.SAFARI,
        e.BrowserType.EDGE,
    ],
    scope="session",
)
def browser_context(request: pytest.FixtureRequest) -> Iterator[BrowserContext]:
    browser_type = request.param
    with sync_playwright() as playwright:
        browser = get_browser(playwright, browser_type)
        context = browser.new_context(
            # viewport={"width": 1280, "height": 1350},
            # locale="en-US"
        )
        yield context
        context.close()
        browser.close()
