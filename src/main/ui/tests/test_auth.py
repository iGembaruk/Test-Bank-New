from playwright.sync_api import expect

from src.main.ui.pages import login_page, catalog_page
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.login_steps import LoginSteps


def test_auth(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")

    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0

def test_auth_locked_user(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("locked_out_user", "secret_sauce")

    error_text = steps.login_page.get_error_text()
    assert "locked out" in error_text, "expect message locking user"

def test_logout_standart_user(page):
    login = LoginSteps(page)
    catalog = CatalogPage(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    assert catalog.get_products_count() > 0

    catalog.logout()
    assert page.url == LoginPage.URL, "expected return on page login"

def test_logout_visual_user(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login("visual_user", "secret_sauce")
    assert catalog.get_products_count() > 0

    catalog.logout()
    assert page.url == LoginPage.URL