
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.mark.regression
def test_cart_persistence(logged_in_page):

    inventory = InventoryPage(logged_in_page)

    inventory.add_product_to_cart("Sauce Labs Backpack")

    assert inventory.get_cart_count() == 1

    logged_in_page.locator("[data-test='shopping-cart-link']").click()

    cart = CartPage(logged_in_page)

    cart.remove_product("Sauce Labs Backpack")

    cart.continue_shopping()

    expect(
        logged_in_page.locator("[data-test='add-to-cart-sauce-labs-backpack']")
    ).to_be_visible()

    expect(inventory.cart_badge).to_have_count(0)
