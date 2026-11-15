
from playwright.sync_api import expect


class CartPage:

    def __init__(self, page):
        self.page = page
        self.checkout_button = page.get_by_test_id("checkout")
        self.continue_shopping_button = page.get_by_test_id(
            "continue-shopping"
        )

    def get_items(self):
        return self.page.get_by_test_id(
            "inventory-item-name"
        ).all_inner_texts()

    def remove_product(self, product_name):
        product_id = product_name.lower().replace(" ", "-")

        remove_button = self.page.get_by_test_id(
            f"remove-{product_id}"
        )

        expect(remove_button).to_be_visible(timeout=10000)
        remove_button.click(timeout=10000)

    def checkout(self):
        expect(self.checkout_button).to_be_visible(timeout=10000)
        self.checkout_button.click(timeout=10000)

    def continue_shopping(self):
        expect(
            self.continue_shopping_button
        ).to_be_visible(timeout=10000)

        self.continue_shopping_button.click(timeout=10000)
