from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Texto general de la página ---
def wait_for_visible_text(driver, timeout=5):
    # Esperar a que el contenido informativo esté presente
    WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".SearchResultClient_results-data-content__k6rav"))
    )


# --- Cards ---
def wait_for_card_container(driver, timeout=40):
    # Esperar hasta que las tarjetas estén presentes
    WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".SearchResultClient_service-group-services__2TIq7"))
    )

def find_card_container(driver):
    return driver.find_element(By.CSS_SELECTOR, ".SearchResultClient_service-group-services__2TIq7")

def find_card_list(cards_container):
    return cards_container.find_elements(By.CSS_SELECTOR, ".GroupedSearchResultCard_card__r7pxV")

def find_imagen_empresa(card):
    return card.find_element(By.CSS_SELECTOR, "div.GroupedSearchResultCard_header__7H134 img")

def find_span_nombre_empresa(card):
    return card.find_element(By.CSS_SELECTOR, ".GroupedSearchResultCard_companyNameFallback__lUPli")

# --- Asientos ---
def find_seat_type_container(card):
    return card.find_element(By.CSS_SELECTOR, ".GroupedSearchResultCard_qualities__QoudX")

def find_seat_type_list(card):
    seat_types_container = find_seat_type_container(card)
  
    # Obtener la lista de botones (hijos inmediatos del contenedor)
    return seat_types_container.find_elements(By.XPATH, "./*")

def find_seat_type_element(seat_type_button):
    return seat_type_button.find_element(By.CSS_SELECTOR, ".GroupedSearchResultCard_qualityName__a1ZT5")

# --- Precios ---
def find_price_element(seat_type_button):
    return seat_type_button.find_element(By.CSS_SELECTOR, ".GroupedSearchResultCard_qualityAmount__bBHMb")
