import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utils.limpieza import limpiar_nombre, filtrar_productos, limpiar_precio
from scraping.paginacion import obtener_total_paginas
import logging 
import logging.config 

logging.config.fileConfig('logging_config/logging.conf') 
logger = logging.getLogger('root')

# TODO: precisar la llamada a nombre (class_="vtex-product-summary-2-x-productBrand"
# " vtex-product-summary-2-x-brandName t-body"))

def obtener_productos_y_precios(driver, max_reintentos=5, espera_entre_intentos=3):
    """Extrae productos y precios, reintentando hasta encontrar al menos uno filtrado."""
    
    for intento in range(max_reintentos):
        logger.info(f"Intento {intento + 1} de {max_reintentos}")
        # Scroll para cargar productos
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 5000);")
            time.sleep(1)

        try:
            WebDriverWait(driver, 5000).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "section[aria-label]"))
            )

            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

            # productos = driver.find_elements(By.CSS_SELECTOR, "section[aria-label]")
            productos = driver.find_elements(
                By.CSS_SELECTOR,
                "div[class*='valtech-carrefourar-product-summary-status-0-x-container']"
                )
            logger.info(f"{len(productos)} productos visibles")

            productos_precios = []

            for producto in productos:
                nombre_elemento = producto.find_element(By.CSS_SELECTOR,
                    ".vtex-product-summary-2-x-productBrand, .vtex-product-summary-2-x-brandName.t-body")
                nombre = nombre_elemento.text.strip()
                nuevo_nombre = limpiar_nombre(nombre)

                botones_inhabilitados = producto.find_elements(By.CSS_SELECTOR, "button:disabled")
                if botones_inhabilitados:
                    # Es decir, el boton de compra esta deshabilitado porque no hay stock
                    logger.info("Ignorando producto sin stock...")
                    continue

                try:
                    precio_elemento = producto.find_element(By.CSS_SELECTOR, "span.valtech-carrefourar-product-price-0-x-sellingPriceValue")
                    selling_price_raw = precio_elemento.text.replace("\n", "").strip()
                except:
                    selling_price_raw = "No disponible"

                try: # Ofertas 
                    list_price_elemento = producto.find_element(By.CSS_SELECTOR, "span.valtech-carrefourar-product-price-0-x-listPrice")
                    list_price_raw = list_price_elemento.text.replace("\n", "").strip()
                except:
                    list_price_raw = selling_price_raw
                    
                # Limpiar precios una sola vez
                selling_price_limpio = limpiar_precio(selling_price_raw) if selling_price_raw else None
                list_price_limpio = limpiar_precio(list_price_raw) if list_price_raw else selling_price_limpio


                # === PRECIO POR KG/LT ===
                try:
                    contenedor_peso = producto.find_element(
                        By.CSS_SELECTOR,
                        "span[class*='dynamic-weight-price'][class$='currencyContainer']"
                    )
                    partes = [sp.text.strip() for sp in contenedor_peso.find_elements(By.TAG_NAME, "span")]
                    precio_kglt = "".join(partes)
                except:
                    precio_kglt = "No disponible"

                try:
                    mi_crf_elemento = producto.find_element(By.CSS_SELECTOR, "div[data-highlight-name*='Mi CRF']")
                    beneficio_mi_crf = "Si"
                except:
                    beneficio_mi_crf = "No"

                if precio_kglt != "No disponible": 
                    precio_kglt_limpio = limpiar_precio(precio_kglt)
                else:
                    precio_kglt_limpio = precio_kglt
                
                productos_precios.append({
                    "Producto": nuevo_nombre,
                    "Precio": selling_price_limpio,
                    "Precio original": list_price_limpio,
                    "Tiene oferta": "Si" if list_price_limpio != selling_price_limpio else "No",
                    "Beneficio Mi CRF": beneficio_mi_crf,
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

    logger.info("No se encontraron productos luego de varios intentos.\n")
    
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

        productos_pagina = obtener_productos_y_precios(driver)
        todos_los_productos.extend(productos_pagina)

    return todos_los_productos



