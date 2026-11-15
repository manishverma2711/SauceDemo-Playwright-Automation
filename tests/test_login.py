
import pytest
import allure
from playwright.sync_api import expect


@allure.epic("SauceDemo UI Automation")
@allure.feature("Login")
@allure.story("Valid Login")
@allure.title("TC_LOGIN_001 | Valid User Login")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_valid_user_login(login_page, app_url, user_name, password):

    with allure.step("Login with valid credentials"):
        login_page.login(user_name, password)

    with allure.step("Verify user navigates to inventory page"):
        expect(login_page.page).to_have_url(
            f"{app_url}/inventory.html"
        )


@allure.epic("SauceDemo UI Automation")
@allure.feature("Login")
@allure.story("Locked Out User")
@allure.title("TC_LOGIN_002 | Locked Out User Login")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_locked_out_user(login_page):

    with allure.step("Login with locked out user credentials"):
        login_page.login("locked_out_user", "secret_sauce")

    with allure.step("Verify locked out error message"):
        assert login_page.get_error() == (
            "Epic sadface: Sorry, this user has been locked out."
        )


@allure.epic("SauceDemo UI Automation")
@allure.feature("Login")
@allure.story("Username Validation")
@allure.title("TC_LOGIN_003 | Empty Username Validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_empty_username(login_page):

    with allure.step("Login with empty username"):
        login_page.login("", "secret_sauce")

    with allure.step("Verify username required error message"):
        assert login_page.get_error() == (
            "Epic sadface: Username is required"
        )


@allure.epic("SauceDemo UI Automation")
@allure.feature("Login")
@allure.story("Password Validation")
@allure.title("TC_LOGIN_004 | Empty Password Validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_empty_password(login_page):

    with allure.step("Login with empty password"):
        login_page.login("standard_user", "")

    with allure.step("Verify password required error message"):
        assert login_page.get_error() == (
            "Epic sadface: Password is required"
        )
