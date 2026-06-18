from playwright.async_api import Page, expect


class CheckoutPage:
    URL = "https://www.saucedemo.com/checkout-complete.html"

    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")
        self.continue_btn = page.locator("#continue")
        self.finish_btn = page.locator('[data-test="finish"]')
        self.error_message = page.locator(".error-message-container")
        self.success_message = page.locator(".complete-header")
        self.item_total = page.locator(".summary_subtotal_label")

    def start_checkout(self, first_name: str, last_name: str, postal_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_btn.click()

    def finish_checkout(self):
        self.finish_btn.click()

    def get_error_text(self) -> str:
        return self.error_message.inner_text()

    def get_success_text(self) -> str:
        return self.success_message.inner_text()

    def get_item_total(self) -> float:
        total_text = self.item_total.inner_text()
        return float(total_text.replace("Item total: $", ""))

    def get_item_total_after_continue(self) -> float:
        expect(self.item_total).to_be_visible()
        total_text = self.item_total.inner_text()
        return float(total_text.replace("Item total: $", ""))