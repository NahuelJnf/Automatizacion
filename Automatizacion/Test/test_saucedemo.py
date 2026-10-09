import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def driver():
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    yield browser
    browser.quit()

def test_01_login(driver: WebDriver):
    driver.get("https://www.saucedemo.com/")

    driver.find_element("id", "user-name").send_keys("standard_user")
    driver.find_element("id", "password").send_keys("secret_sauce")
    driver.find_element("id", "login-button").click()

    assert "inventory" in driver.current_url

def test_02_verificar_inventario(driver):
    driver.get("https://www.saucedemo.com/")

    driver.find_element("id", "user-name").send_keys("standard_user")
    driver.find_element("id", "password").send_keys("secret_sauce")
    driver.find_element("id", "login-button").click()

    page_title = driver.title
    section_title = driver.find_element("class name", "title").text

    assert page_title == "Swag Labs" , f"ERROR: El titulo de ventana esperado es 'Swag Labs' pero se obtuvo '{page_title}' "
   
    assert section_title == "Products" , f"ERROR: El titulo de sección esperado es 'Products' pero se obtuvo '{section_title}' "

def test_03_productos_visibles(driver):
    inventory_items = driver.find_elements("class name", "inventory_item")
    assert len(inventory_items) > 0 , f"ERROR: No se encontraron productos visibles"  