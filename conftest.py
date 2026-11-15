
import os
import pytest
from pathlib import Path
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def pytest_addoption(parser):
    parser.addoption(
        "--app-url",
        action="store",
        default=os.getenv("BASE_URL", "https://www.saucedemo.com")
    )
    parser.addoption(
        "--user-name",
        action="store",
        default=os.getenv("SAUCE_USERNAME", "standard_user")
    )
    parser.addoption(
        "--password",
        action="store",
        default=os.getenv("SAUCE_PASSWORD", "secret_sauce")
    )


# Configure SauceDemo's data-test attributes
@pytest.fixture(scope="session", autouse=True)
def configure_test_ids(playwright):
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def app_url(request):
    return request.config.getoption("--app-url").rstrip("/")


@pytest.fixture(scope="session")
def user_name(request):
    return request.config.getoption("--user-name")


@pytest.fixture(scope="session")
def password(request):
    return request.config.getoption("--password")


@pytest.fixture
def login_page(page, app_url):
    page.goto(app_url)
    return LoginPage(page)


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)


@pytest.fixture(scope="session")
def auth_state(browser, playwright, app_url, user_name, password):

    # Configure before creating authenticated context
    playwright.selectors.set_test_id_attribute("data-test")

    auth_dir = Path("playwright/.auth")
    auth_dir.mkdir(parents=True, exist_ok=True)

    auth_file = auth_dir / "user.json"

    context = browser.new_context()

    try:
        page = context.new_page()
        page.goto(app_url)

        login = LoginPage(page)
        login.login(user_name, password)

        expect(page).to_have_url(f"{app_url}/inventory.html")

        context.storage_state(path=str(auth_file))

    finally:
        context.close()

    return str(auth_file)


@pytest.fixture
def logged_in_page(browser, auth_state, app_url):

    context = browser.new_context(
        storage_state=auth_state,
        record_video_dir="test-results/videos",
        record_video_size={
            "width": 1280,
            "height": 720
        },
    )

    page = context.new_page()

    try:
        page.goto(f"{app_url}/inventory.html")

        expect(page).to_have_url(
            f"{app_url}/inventory.html"
        )

        yield page

    finally:
        context.close()
