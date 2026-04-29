import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.limpieza import limpiar_precio
from utils.limpieza import extraer_cantidad_compañeros
import logging
import logging.config

logging.config.fileConfig('logging_config/logging.conf')
logger = logging.getLogger('root')

BASE_URL = "https://www.roomgo.com.ar/cordoba/en-alquiler-cordoba-capital"


def obtener_total_paginas_roomgo(driver):
    """Obtiene el número total de páginas de Roomgo."""
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.listing_pagination_page a"))
        )
        paginas = driver.find_elements(By.CSS_SELECTOR, "div.listing_pagination_page a")
        numeros = []
        for p in paginas:
            try:
                numeros.append(int(p.text.strip()))
            except ValueError:
                continue
        total = max(numeros) if numeros else 1
        logger.info(f"[Roomgo] Total de páginas detectadas: {total}")
        return total
    except Exception as e:
        logger.error(f"[Roomgo] Error obteniendo páginas: {e}")
        return 1


def obtener_listings_pagina(driver):
    """Extrae listings de la página actual."""
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.listing_item_price"))
        )
    except Exception:
        logger.info("[Roomgo] No se encontraron listings en esta página.")
        return []

    time.sleep(2)

    precios = driver.find_elements(By.CSS_SELECTOR, "div.listing_item_price")
    flatmates = driver.find_elements(By.CSS_SELECTOR, "span.listing_item_nb_flatmates")
    titulos = driver.find_elements(By.CSS_SELECTOR, "div.grey.heading--small")

    resultados = []
    for i, precio_el in enumerate(precios):
        precio_raw = precio_el.text.strip()
        precio_limpio = limpiar_precio(precio_raw)

        tipo = flatmates[i].text.strip() if i < len(flatmates) else "No disponible"
        cantidad_compañeros = extraer_cantidad_compañeros(tipo)

        titulo_raw = titulos[i].text.strip() if i < len(titulos) else "No disponible"
        if "habitaciones" in titulo_raw.lower():
            titulo = "Habitaciones"
        elif "habitación" in titulo_raw.lower() or "habitacion" in titulo_raw.lower():
            titulo = "Habitación"
        else:
            titulo = titulo_raw

        if precio_limpio is not None and precio_limpio >= 1000 and cantidad_compañeros is not None:
            resultados.append({
                "Titulo": titulo,
                "Tipo": tipo,
                "Cantidad_Compañeros": cantidad_compañeros,
                "Precio": precio_limpio 
            })
    
    logger.info(f"[Roomgo] {len(resultados)} listing(s) en esta página.")
    return resultados


def scrapear_roomgo(driver):
    """Recorre todas las páginas de Roomgo y extrae los listings."""
    driver.get(BASE_URL)
    time.sleep(3)

    total_paginas = obtener_total_paginas_roomgo(driver)
    todos = []

    for pagina in range(1, total_paginas + 1):
        url_pagina = BASE_URL if pagina == 1 else f"{BASE_URL}?page={pagina}"
        driver.get(url_pagina)
        logger.info(f"[Roomgo] Scrapeando página {pagina} de {total_paginas}...")
        time.sleep(3)
        todos.extend(obtener_listings_pagina(driver))

    return todos
