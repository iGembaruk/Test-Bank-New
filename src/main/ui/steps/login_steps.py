import allure
from playwright.sync_api import Page

from src.main.ui.pages.login_page import LoginPage


class LoginSteps:
    LOGIN_URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)

    @allure.step("Open page login")
    def open_login_page(self):
        self.login_page.open()
        return self

    @allure.step("Login user {username}")
    def login(self, username:str, password: str):
        self.login_page.login(username, password)
        return self

    @allure.step("Catching text error for login")
    def get_error_text(self) -> str:
        return self.login_page.get_error_text()


