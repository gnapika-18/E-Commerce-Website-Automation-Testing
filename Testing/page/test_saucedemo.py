from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest



def login(driver):
    driver.get("https://www.saucedemo.com/")

    driver.find_element(
        By.ID,
        "user-name"
    ).send_keys("standard_user")

    driver.find_element(
        By.ID,
        "password"
    ).send_keys("secret_sauce")

    driver.find_element(
        By.ID,
        "login-button"
    ).click()


def test_valid_login():

    driver = webdriver.Chrome()

    login(driver)

    assert "inventory" in driver.current_url

    driver.quit()


def test_invalid_login():

    driver = webdriver.Chrome()

    driver.get("https://www.saucedemo.com/")

    driver.find_element(
        By.ID,
        "user-name"
    ).send_keys("wrong_user")

    driver.find_element(
        By.ID,
        "password"
    ).send_keys("wrong_password")

    driver.find_element(
        By.ID,
        "login-button"
    ).click()

    error = driver.find_element(
        By.TAG_NAME,
        "h3"
    ).text

    assert "do not match" in error

    driver.quit()


def test_add_to_cart():

    driver = webdriver.Chrome()

    login(driver)

    driver.find_element(
        By.ID,
        "add-to-cart-sauce-labs-backpack"
    ).click()

    badge = driver.find_element(
        By.CLASS_NAME,
        "shopping_cart_badge"
    ).text

    assert badge == "1"

    driver.quit()

def test_remove_from_cart():

    driver = webdriver.Chrome()

    login(driver)

    driver.find_element(
        By.ID,
        "add-to-cart-sauce-labs-backpack"
    ).click()

    driver.find_element(
        By.ID,
        "remove-sauce-labs-backpack"
    ).click()

    cart = driver.find_elements(
        By.CLASS_NAME,
        "shopping_cart_badge"
    )

    assert len(cart) == 0

    driver.quit()


def test_product_displayed():

    driver = webdriver.Chrome()

    login(driver)

    products = driver.find_elements(
        By.CLASS_NAME,
        "inventory_item"
    )

    assert len(products) > 0

    driver.quit()


def test_logout():

    driver = webdriver.Chrome()

    login(driver)

    driver.find_element(
        By.ID,
        "react-burger-menu-btn"
    ).click()

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.ID, "logout_sidebar_link")
        )
    )

    driver.find_element(
        By.ID,
        "logout_sidebar_link"
    ).click()

    assert "saucedemo" in driver.current_url

    driver.quit()