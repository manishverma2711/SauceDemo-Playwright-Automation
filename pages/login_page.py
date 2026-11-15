
from playwright.sync_api import expect


class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    def login(self, user_name, password):
        self.username.fill(user_name)
        self.password.fill(password)
        self.login_button.click()

    def get_error(self):
        expect(self.error_message).to_be_visible()
        return self.error_message.inner_text()
