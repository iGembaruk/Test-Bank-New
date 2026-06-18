from playwright.sync_api import expect

from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps


def test_count_catalog(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")
    assert steps.catalog.get_products_count() == 6


def test_sorted_by_name_a_to_z(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")
    steps.sort_items("az")
    assert steps.get_product_names() == sorted(steps.get_product_names())

    steps.sort_items("za")
    assert steps.get_product_names() == sorted(steps.get_product_names(), reverse=True)


def test_sort_by_price(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.sort_items("lohi")
    assert steps.get_product_prices() == sorted(steps.get_product_prices())

    steps.sort_items("hilo")
    assert steps.get_product_prices() == sorted(steps.get_product_prices(), reverse=True)


def test_add_to_cart(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Bike Light")
    assert steps.get_cart_count() == 1


def test_add_card_remove(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Onesie")
    assert steps.get_cart_count() == 1
    steps.remove_from_cart("Sauce Labs Onesie")
    assert steps.get_cart_count() == 0


def test_product_details_onesie(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")

    name, price, detail_name, detail_price = catalog.open_product_details("Sauce Labs Onesie")
    assert name == detail_name
    assert price == detail_price


def test_product_details_fleece_jacket(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")
    name, price, detail_name, detail_price = steps.open_product_details("Sauce Labs Fleece Jacket")

    assert name == detail_name
    assert price == detail_price


def test_remove_item_from_catalog(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")
    steps.remove_from_cart("Test.allTheThings() T-Shirt (Red)")