
import pytest
import allure
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@allure.epic("SauceDemo UI Automation")
@allure.feature("Shopping Cart")
@allure.story("Cart Persistence")
@allure.title("TC_CART_001 | Verify Cart After Removing Product")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_cart_updates_after_removing_item(logged_in_page):

    page = logged_in_page
    inventory = InventoryPage(page)
    cart = CartPage(page)

    product_name = "Sauce Labs Backpack"

    with allure.step("Add product to shopping cart"):
        inventory.add_product_to_cart(product_name)
        expect(inventory.cart_badge).to_have_text("1")

    with allure.step("Open shopping cart"):
        inventory.open_cart()

    with allure.step("Remove product from cart"):
        cart.remove_product(product_name)

    with allure.step("Verify cart badge disappears"):
        expect(
            page.get_by_test_id("shopping-cart-badge")
        ).to_have_count(0)

    with allure.step("Continue shopping"):
        cart.continue_shopping()

    with allure.step("Verify Add to cart button is displayed"):
        inventory.verify_add_button(product_name)

    with allure.step("Verify cart badge remains empty"):
        expect(inventory.cart_badge).to_have_count(0)
