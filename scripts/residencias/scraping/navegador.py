from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def crear_driver():
    """Configura y devuelve un WebDriver en modo headless."""
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    return webdriver.Firefox(options=options)
