import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.page_objects.login_page import LoginPage
from utils.page_objects.inventory_page import InventoryPage
from utils.logger import test_logger
from config import BROWSER

@pytest.fixture(scope="module")
def driver():
    if BROWSER == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif BROWSER == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    yield driver
    driver.quit()

def test_login(driver):
    test_logger.info("Starting test_login")
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login("standard_user", "secret_sauce")
    assert "inventory.html" in driver.current_url
    test_logger.info("Finished test_login")

def test_add_item_to_cart(driver):
    test_logger.info("Starting test_add_item_to_cart")
    test_login(driver)  # Ensure user is logged in
    inventory_page = InventoryPage(driver)
    inventory_page.add_first_item_to_cart()
    assert inventory_page.cart_item_count() == '1'
    test_logger.info("Finished test_add_item_to_cart")
