from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.inventory_item = (By.CLASS_NAME, "inventory_item")
        self.add_to_cart_button = (By.CLASS_NAME, "btn_inventory")
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")

    def get_inventory_items(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.inventory_item)
        )

    def add_first_item_to_cart(self):
        add_buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.add_to_cart_button)
        )
        add_buttons[0].click()  # Ensure we are treating this as a list of elements

    def cart_item_count(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.cart_badge)
        ).text
