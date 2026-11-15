
import pytest

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.regression
@pytest.mark.parametrize(
    "first_name,last_name,postal_code,expected_error",
    [
        ("", "Verma", "421301", "Error: First Name is required"),
        ("Manish", "", "421301", "Error: Last Name is required"),
        ("Manish", "Verma", "", "Error: Postal Code is required"),
    ],
)
def test_checkout_required_fields(
    logged_in_page,
    first_name,
    last_name,
    postal_code,
    expected_error
):
    inventory = InventoryPage(logged_in_page)
    inventory.add_product_to_cart("Sauce Labs Backpack")

    logged_in_page.locator("[data-test='shopping-cart-link']").click()

    cart = CartPage(logged_in_page)
    cart.checkout()

    checkout = CheckoutPage(logged_in_page)
    checkout.enter_information(first_name, last_name, postal_code)

    assert checkout.get_error() == expected_error
