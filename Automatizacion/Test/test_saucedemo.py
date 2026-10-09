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

def iniciar_sesion(driver: WebDriver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element("id", "user-name").send_keys("standard_user")
    driver.find_element("id", "password").send_keys("secret_sauce")
    driver.find_element("id", "login-button").click()

def test_01_login(driver: WebDriver):
    
    iniciar_sesion(driver)
    assert "inventory" in driver.current_url

def test_02_verificar_inventario(driver: WebDriver):
    
    iniciar_sesion(driver)
    page_title = driver.title
    section_title = driver.find_element("class name", "title").text
    assert page_title == "Swag Labs" , f"ERROR: El titulo de ventana esperado es 'Swag Labs' pero se obtuvo '{page_title}' "
    assert section_title == "Products" , f"ERROR: El titulo de sección esperado es 'Products' pero se obtuvo '{section_title}' "

def test_03_productos_visibles(driver: WebDriver):
    iniciar_sesion(driver)
    inventory_items = driver.find_elements("class name", "inventory_item")
    assert len(inventory_items) > 0 , f"ERROR: No se encontraron productos visibles"  

def test_04_verificar_nombres_y_precios(driver: WebDriver):
    iniciar_sesion(driver)

    nombres = driver.find_elements("class name", "inventory_item_name")
    precios = driver.find_elements("class name", "inventory_item_price")

    assert len(nombres) == len(precios), (
        f"ERROR: Hay {len(nombres)} nombres y {len(precios)} precios"
    )

    productos_obtenidos = {
        nombre.text: precio.text
        for nombre, precio in zip(nombres, precios)
    }

    productos_esperados = {
        "Sauce Labs Backpack": "$29.99",
        "Sauce Labs Bike Light": "$9.99",
        "Sauce Labs Bolt T-Shirt": "$15.99",
        "Sauce Labs Fleece Jacket": "$49.99",
        "Sauce Labs Onesie": "$7.99",
        "Test.allTheThings() T-Shirt (Red)": "$15.99",
    }

    assert productos_obtenidos == productos_esperados, (
        f"ERROR: Los productos o precios no coinciden.\n"
        f"Esperados: {productos_esperados}\n"
        f"Obtenidos: {productos_obtenidos}"
    )  

def test_05_validar_interfaz(driver: WebDriver):   
    iniciar_sesion(driver)
    menu_button = driver.find_element("id", "react-burger-menu-btn")
    filtro = driver.find_element("class name", "product_sort_container")
    assert menu_button.is_displayed(), "ERROR: El botón de menú no es visible" 
    assert filtro.is_displayed(), "ERROR: El filtro de productos no es visible"


    