
from playwright.sync_api import expect


class CheckoutPage:
    def __init__(self, page):
        self.page = page
        self.first_name = page.locator("[data-test='firstName']")
        self.last_name = page.locator("[data-test='lastName']")
        self.postal_code = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")
        self.error_message = page.locator("[data-test='error']")

    def enter_information(self, first_name, last_name, postal_code):
        if first_name:
            self.first_name.fill(first_name)
        if last_name:
            self.last_name.fill(last_name)
        if postal_code:
            self.postal_code.fill(postal_code)
        self.continue_button.click()

    def get_error(self):
        expect(self.error_message).to_be_visible()
        return self.error_message.inner_text()

    def get_summary_amounts(self):
        item_total = self.page.locator("[data-test='subtotal-label']").inner_text()
        tax = self.page.locator("[data-test='tax-label']").inner_text()
        total = self.page.locator("[data-test='total-label']").inner_text()

        return (
            float(item_total.split("$")[1]),
            float(tax.split("$")[1]),
            float(total.split("$")[1]),
        )

    def finish_order(self):
        self.finish_button.click()
