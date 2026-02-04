import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utils.limpieza import filtrar_productos, limpiar_precio, limpiar_precio_kg_lt
from scraping.paginacion import obtener_total_paginas
import logging 
import logging.config 

logging.config.fileConfig('logging_config/logging.conf') 
logger = logging.getLogger('root')
# NOTA: scrapea también lo que está en los sliders al fondo... 
# TODO: ver si se arregla scrolleando hasta cierta parte de la pantalla

def obtener_productos_y_precios_disco(driver, max_reintentos=5, espera_entre_intentos=3):
    """Extrae productos, precios y promociones desde la página de Disco."""

    clases_promociones = [
        "discoargentina-store-theme-3Hc7_vKK9au6dX_Su4b0Ae",  # -25%, -30%
        "discoargentina-store-theme-MnHW0PCgcT3ih2-RUT-t_",   # 2do al 70%
        "discoargentina-store-theme-Aq2AAEuiQuapu8IqwN0Aj"   # 3x2
    ]

    for intento in range(max_reintentos):
        logger.info(f"Intento {intento + 1} de {max_reintentos}")

        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(50)

        try:
            WebDriverWait(driver, 150).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "div[class*='discoargentina-cmedia-integration-cencosud-1-x-galleryItem']"
                ))
            )

            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(500)

            productos = driver.find_elements(
                By.CSS_SELECTOR,
                "div[class*='discoargentina-cmedia-integration-cencosud-1-x-galleryItem']"
            )
            productos_precios = []

            for producto in productos:
                try:
                    nombre = producto.find_element(
                        By.CSS_SELECTOR, "div.vtex-product-summary-2-x-nameContainer h2"
                    ).text.strip()
                except:
                    nombre = "No disponible"

                try:
                    precio_elemento = producto.find_element(By.CSS_SELECTOR, "div#priceContainer")
                    precio = precio_elemento.text.strip()
                except:
                    precio = "No disponible"

                try:
                    precio_kg_lt_elemento = producto.find_element(
                        By.CSS_SELECTOR, "span.vtex-custom-unit-price"
                    )
                    precio_kg_lt = precio_kg_lt_elemento.text.strip()
                except:
                    precio_kg_lt = "No disponible"

                promociones = []
                for clase in clases_promociones:
                    spans = producto.find_elements(By.CSS_SELECTOR, f"span.{clase}")
                    for span in spans:
                        promo_text = span.text.strip()
                        if promo_text:
                            promociones.append(promo_text) # Guardo las ofertas

                promo_final = "Si" if promociones else "No"

                # Limpieza de precios
                precio_limpio = limpiar_precio(precio)
                precio_kglt_limpio = limpiar_precio_kg_lt(precio_kg_lt)

                productos_precios.append({
                    "Producto": nombre,
                    "Precio": precio_limpio,
                    "Tiene oferta": promo_final, 
                    "Precio x kg/lt": precio_kglt_limpio
                })

            productos_filtrados = filtrar_productos(productos_precios)

            if productos_filtrados:
                logger.info(f"* {len(productos_filtrados)} productos.")
                return productos_filtrados
            else:
                logger.critical("No se encontraron productos. Reintentando...")
                time.sleep(espera_entre_intentos)

        except Exception as e:
            logger.error(f"Error en intento {intento + 1}: {e}")
            time.sleep(espera_entre_intentos)

    logger.info("No se encontraron productos luego de varios intentos.")
    return []

def scrapear_categoria(driver, url_categoria):
    """Recorre todas las páginas de una categoría y extrae los productos."""
    driver.get(url_categoria)
    time.sleep(3)

    total_paginas = obtener_total_paginas(driver)

    todos_los_productos = []

    for pagina in range(1, total_paginas + 1):
        url_pagina = f"{url_categoria}?page={pagina}"
        driver.get(url_pagina)
        logger.info(f"Scrapeando página {pagina} de {total_paginas}...")
        time.sleep(3)

        productos_pagina = obtener_productos_y_precios_disco(driver)
        todos_los_productos.extend(productos_pagina)

    return todos_los_productos



