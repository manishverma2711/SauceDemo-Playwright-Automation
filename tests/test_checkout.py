
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.smoke
def test_complete_checkout(logged_in_page):

    inventory = InventoryPage(logged_in_page)

    inventory.add_product_to_cart("Sauce Labs Backpack")
    inventory.add_product_to_cart("Sauce Labs Bike Light")

    assert inventory.get_cart_count() == 2

    logged_in_page.locator("[data-test='shopping-cart-link']").click()

    cart = CartPage(logged_in_page)

    expected_items = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light"
    ]

    assert cart.get_items() == expected_items

    cart.checkout()

    checkout = CheckoutPage(logged_in_page)

    checkout.enter_information("Manish", "Verma", "421301")

    item_total, tax, total = checkout.get_summary_amounts()

    assert round(item_total + tax, 2) == total

    checkout.finish_order()

    expect(logged_in_page.locator("[data-test='complete-header']")).to_have_text(
        "Thank you for your order!"
    )
