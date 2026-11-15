
from playwright.sync_api import expect


class InventoryPage:

    def __init__(self, page):
        self.page = page
        self.sort_dropdown = page.locator(
            "[data-test='product-sort-container']"
        )
        self.product_names = page.locator(".inventory_item_name")
        self.product_prices = page.locator(".inventory_item_price")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.cart_icon = page.get_by_test_id("shopping-cart-link")

    def sort_products(self, value):
        self.sort_dropdown.select_option(value)

    def add_product_to_cart(self, product_name):
        product_id = product_name.lower().replace(" ", "-")
        self.page.get_by_test_id(
            f"add-to-cart-{product_id}"
        ).click()

    # Compatibility with your existing cart test
    def add_product(self, product_name):
        self.add_product_to_cart(product_name)

    def get_cart_count(self):
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def open_cart(self):
        self.cart_icon.click()

    def verify_add_button(self, product_name):
        product_id = product_name.lower().replace(" ", "-")
        expect(
            self.page.get_by_test_id(f"add-to-cart-{product_id}")
        ).to_be_visible()
