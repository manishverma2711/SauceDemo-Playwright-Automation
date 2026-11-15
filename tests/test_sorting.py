
import pytest
from pages.inventory_page import InventoryPage


@pytest.mark.regression
def test_sort_price_low_to_high(logged_in_page):
    inventory = InventoryPage(logged_in_page)

    inventory.sort_products("lohi")

    actual_prices = inventory.product_prices.all_text_contents()

    expected_prices = [
        "$7.99",
        "$9.99",
        "$15.99",
        "$15.99",
        "$29.99",
        "$49.99"
    ]

    assert actual_prices == expected_prices


@pytest.mark.regression
def test_sort_name_z_to_a(logged_in_page):
    inventory = InventoryPage(logged_in_page)

    inventory.sort_products("za")

    actual_names = inventory.product_names.all_text_contents()

    expected_names = [
        "Test.allTheThings() T-Shirt (Red)",
        "Sauce Labs Onesie",
        "Sauce Labs Fleece Jacket",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Bike Light",
        "Sauce Labs Backpack"
    ]

    print("Actual product order:", actual_names)
    print("Expected product order:", expected_names)

    assert actual_names == expected_names