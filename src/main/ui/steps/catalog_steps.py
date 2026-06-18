import allure
from playwright.sync_api import Page, expect

from src.main.ui.pages.catalog_page import CatalogPage


class CatalogSteps:
    def __init__(self, page: Page):
        self.page = page
        self.catalog = CatalogPage(page)

    @allure.step("Login user {username}")
    def login(self, username:str, password: str):
        self.catalog.login(username, password)
        return self

    @allure.step("Add item in basket: {product_name}")
    def add_to_cart(self, product_name: str):
        btn = self.catalog.add_to_cart(product_name)
        expect(btn).to_have_text("Remove")
        return self

    @allure.step("Delete item from basket {product_name}")
    def remove_from_cart(self, product_name: str):
        btn = self.catalog.remove_from_cart(product_name)
        expect(btn).to_have_text("Add to cart")
        return self

    @allure.step("Sorted items: {option}")
    def sort_items(self, option: str):
        self.catalog.sort_items(option)
        return self

    @allure.step("Get count items in catalog")
    def get_products_count(self) -> int:
        return self.catalog.get_products_count()

    @allure.step("Get list names items")
    def get_product_names(self) -> list[str]:
        return self.catalog.get_product_names()

    @allure.step("Get list prices items")
    def get_product_prices(self) -> list[float]:
        return self.catalog.get_product_prices()

    @allure.step("Get count items in basket")
    def get_cart_count(self) -> int:
        return self.catalog.get_cart_count()

    @allure.step("Open page details item: {product_name}")
    def open_product_details(self, product_name: str):
        return self.catalog.open_product_details(product_name)

    @allure.step("logout")
    def logout(self):
        self.catalog.logout()
        return self