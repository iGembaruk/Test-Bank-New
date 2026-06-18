import allure
from src.main.ui.pages.basket_page import BasketPage
from playwright.sync_api import Page, expect


class BasketSteps:
    def __init__(self, page: Page):
        self.page = page
        self.basket = BasketPage(page
                                 )
    @allure.step("Open basket")
    def open_cart(self):
        self.basket.open_cart()
        return self

    @allure.step("Checked item {product_name} has be in basket")
    def expect_item_in_cart(self, product_name: str):
        self.basket.expect_item_in_cart(product_name)
        return self

    @allure.step("Checked item {product_name} not has be in basket")
    def expect_item_not_in_cart(self, product_name: str):
        self.basket.expect_item_not_in_cart(product_name)
        return self

    @allure.step("Remove item in basket: {product_name}")
    def remove_item(self, product_name: str):
        self.basket.remove_item(product_name)
        return self

    @allure.step("Move checkout")
    def checkout(self):
        self.basket.checkout()
        return self

    @allure.step("Get names from basket")
    def get_item_names(self) -> list[str]:
        return self.basket.get_item_names()

    @allure.step("Get total sum from basket")
    def get_items_total_price(self) -> float:
        return self.basket.get_items_total_price()