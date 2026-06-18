from playwright.sync_api import expect

from src.main.ui.pages.basket_page import BasketPage
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.checkout_page import CheckoutPage
from src.main.ui.steps.basket_steps import BasketSteps
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps


def test_add_item_and_check_in_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Backpack")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Backpack")


def test_add_items_and_check_in_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")


def test_remove_item_from_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.remove_item("Sauce Labs Fleece Jacket")
    basket.expect_item_not_in_cart("Sauce Labs Fleece Jacket")


def test_remove_items_from_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Test.allTheThings() T-Shirt (Red)")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Test.allTheThings() T-Shirt (Red)")

    basket.remove_item("Sauce Labs Fleece Jacket")
    basket.remove_item("Test.allTheThings() T-Shirt (Red)")

    basket.expect_item_not_in_cart("Sauce Labs Backpack")
    basket.expect_item_not_in_cart("Test.allTheThings() T-Shirt (Red)")

def test_e2e_add_buy(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-shirt")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-shirt")
    basket_total = basket.get_items_total_price

    basket.checkout()
    checkout.start_checkout("Test", "User", "12345")
    checkout_total = checkout.get_item_total_after_continue()
    assert checkout_total == basket_total, "sum items in Checkout no equals with basket"


def test_negative_no_field_in_checkout(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    catalog.login("standard_user", "secret_sauce")
    basket.open_cart()
    items = basket.get_item_names()
    assert len(items) == 0, "basket no empty"

    basket.checkout()
    checkout.start_checkout(
        first_name="NewUser",
        last_name="Nrk",
        postal_code=""
    )

    error_text = checkout.get_error_text()
    assert error_text != "", "Expected error for payment empty basket"