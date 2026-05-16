# ============================================
# FILE: utils/config.py
# ============================================

BASE_URL = "https://www.saucedemo.com/"

WAIT_TIME = 10

USERNAME = "standard_user"

PASSWORD = "secret_sauce"

EXPECTED_PRODUCT = "Sauce Labs Backpack"


# ============================================
# FILE: utils/logger.py
# ============================================

import logging


def setup_logger():

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s - "
            "%(levelname)s - "
            "%(message)s"
        )
    )

    return logging.getLogger()


# ============================================
# FILE: utils/driver_factory.py
# ============================================

from selenium import webdriver

from selenium.webdriver.chrome.options import (
    Options
)

from selenium.webdriver.chrome.service import (
    Service
)

from webdriver_manager.chrome import (
    ChromeDriverManager
)


def initialize_browser():

    chrome_options = Options()

    chrome_options.add_argument(
        "--start-maximized"
    )

    service = Service(
        ChromeDriverManager().install()
    )

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    return driver


# ============================================
# FILE: pages/login_page.py
# ============================================

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import (
    WebDriverWait
)

from selenium.webdriver.support import (
    expected_conditions as ec
)

from utils.config import (
    BASE_URL,
    WAIT_TIME
)


class LoginPage:

    USERNAME_INPUT = (
        By.ID,
        "user-name"
    )

    PASSWORD_INPUT = (
        By.ID,
        "password"
    )

    LOGIN_BUTTON = (
        By.ID,
        "login-button"
    )

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            WAIT_TIME
        )

    def open_application(self):

        self.driver.get(BASE_URL)

    def login(
        self,
        username,
        password
    ):

        username_field = self.wait.until(
            ec.presence_of_element_located(
                self.USERNAME_INPUT
            )
        )

        password_field = self.wait.until(
            ec.presence_of_element_located(
                self.PASSWORD_INPUT
            )
        )

        login_button = self.wait.until(
            ec.element_to_be_clickable(
                self.LOGIN_BUTTON
            )
        )

        username_field.send_keys(
            username
        )

        password_field.send_keys(
            password
        )

        login_button.click()


# ============================================
# FILE: pages/inventory_page.py
# ============================================

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import (
    WebDriverWait
)

from selenium.webdriver.support import (
    expected_conditions as ec
)

from utils.config import WAIT_TIME


class InventoryPage:

    ADD_TO_CART_BUTTON = (
        By.ID,
        "add-to-cart-sauce-labs-backpack"
    )

    CART_ICON = (
        By.CLASS_NAME,
        "shopping_cart_link"
    )

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            WAIT_TIME
        )

    def add_product_to_cart(self):

        add_to_cart_button = self.wait.until(
            ec.element_to_be_clickable(
                self.ADD_TO_CART_BUTTON
            )
        )

        add_to_cart_button.click()

    def open_cart(self):

        cart_icon = self.wait.until(
            ec.element_to_be_clickable(
                self.CART_ICON
            )
        )

        cart_icon.click()


# ============================================
# FILE: pages/cart_page.py
# ============================================

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import (
    WebDriverWait
)

from selenium.webdriver.support import (
    expected_conditions as ec
)

from utils.config import WAIT_TIME


class CartPage:

    CART_ITEM_NAME = (
        By.CLASS_NAME,
        "inventory_item_name"
    )

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            WAIT_TIME
        )

    def get_cart_product_name(self):

        cart_item = self.wait.until(
            ec.presence_of_element_located(
                self.CART_ITEM_NAME
            )
        )

        return cart_item.text


# ============================================
# FILE: tests/test_add_to_cart.py
# ============================================

import pytest

from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException
)

from pages.login_page import LoginPage

from pages.inventory_page import (
    InventoryPage
)

from pages.cart_page import CartPage

from utils.driver_factory import (
    initialize_browser
)

from utils.config import (
    USERNAME,
    PASSWORD,
    EXPECTED_PRODUCT
)

from utils.logger import setup_logger


logger = setup_logger()


@pytest.fixture
def driver():

    driver_instance = initialize_browser()

    yield driver_instance

    driver_instance.quit()


@pytest.mark.parametrize(
    "username,password",
    [
        (
            USERNAME,
            PASSWORD
        )
    ]
)
def test_add_product_to_cart(
    driver,
    username,
    password
):

    try:

        login_page = LoginPage(driver)

        inventory_page = InventoryPage(
            driver
        )

        cart_page = CartPage(driver)

        login_page.open_application()

        login_page.login(
            username,
            password
        )

        logger.info(
            "Login successful."
        )

        inventory_page.add_product_to_cart()

        logger.info(
            "Product added to cart."
        )

        inventory_page.open_cart()

        logger.info(
            "Cart opened successfully."
        )

        cart_product = (
            cart_page.get_cart_product_name()
        )

        assert (
            EXPECTED_PRODUCT == cart_product
        )

        logger.info(
            "TEST PASSED: Product found "
            "inside cart."
        )

    except TimeoutException as error:

        logger.error(
            "Timeout occurred: %s",
            error
        )

        pytest.fail(
            "TimeoutException occurred."
        )

    except WebDriverException as error:

        logger.error(
            "WebDriver issue occurred: %s",
            error
        )

        pytest.fail(
            "WebDriverException occurred."
        )

    except Exception as error:

        logger.error(
            "Unexpected error occurred: %s",
            error
        )

        pytest.fail(
            "Unexpected exception occurred."
        )
