from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.limpieza import limpiar_precio
import time
import logging 
import logging.config 

# TODO: Revisar Stock y Ofertas

logging.config.fileConfig('logging_config/logging.conf') 
logger = logging.getLogger('root')

def obtener_productos_y_precios(driver, max_reintentos=5, espera_entre_intentos=3): 
    """Extrae productos, precios, stock y ofertas desde la web de Grafitti Librería."""

    for intento in range(max_reintentos):
        logger.info(f"Intento {intento + 1} de {max_reintentos}")

        # Scroll para cargar productos
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)

        try:
            # Esperamos a que cargue la grilla
            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".js-product-table")
                )
            )

            # Buscamos los productos dentro de la grilla
            productos = driver.find_elements(
                By.CSS_SELECTOR,
                ".js-product-table .js-product-item-private"
            )

            logger.info(f"{len(productos)} productos visibles")


            productos_precios = []

            for container in productos:
                # --- DATA VARIANTS
                try:
                    label_container = container.find_element(By.CLASS_NAME, "labels")
                    stock_label = label_container.find_element(By.CLASS_NAME, "js-stock-label")

                    # Analizamos el texto y estilo
                    texto_label = stock_label.text.strip()
                    style = stock_label.get_attribute("style")

                    if "SIN STOCK" in texto_label and ("display:none" not in style if style else True):
                        stock = "No"
                    else:
                        stock = "Si"
                except Exception as e:
                    stock ="Si"

                                    
                    # --- DESCRIPCIÓN
                    try:
                        desc = container.find_element(
                            By.CSS_SELECTOR,
                            ".product-item-information"
                        )

                        nombre = desc.find_element(
                            By.CSS_SELECTOR,
                            ".js-item-name"
                        ).text.strip()

                    except:
                        nombre = "Nombre no disponible"


                    # --- PRECIO
                    try:
                        contenedor_precio = container.find_element(
                            By.CSS_SELECTOR,
                            ".product-item-price-container"
                        )

                        precio_final = contenedor_precio.find_element(
                            By.CSS_SELECTOR,
                            ".js-price-display"
                        ).text.strip()

                    except:
                        precio_final = "Precio no disponible"                

                    try:
                        precio_original_elem = contenedor_precio.find_element(By.CLASS_NAME, "price-compare")
                        precio_original = precio_original_elem.text.strip()
                        if not precio_original or "$0" in precio_original:
                            precio_original = precio_final
                            tiene_oferta = "No"
                        else:
                            tiene_oferta = "Sí"
                    except:
                        precio_original = precio_final
                        tiene_oferta = "No"

                except:
                    precio_final = "No disponible"
                    precio_original = "No disponible"
                    tiene_oferta = "No"

                precio_final_limpio = limpiar_precio(precio_final)
                precio_original_limpio = limpiar_precio(precio_original)
                
                productos_precios.append({
                    "Nombre del producto": nombre,
                    "Precio final": precio_final_limpio,
                    "Precio original": precio_original_limpio,
                    "Tiene oferta": tiene_oferta,
                    "Stock": stock
                })

            if productos_precios:
                logger.info(f"* {len(productos_precios)} productos.")
                return productos_precios
            else:
                logger.critical("No se encontraron productos. Reintentando...")
                time.sleep(espera_entre_intentos)

        except Exception as e:
            logger.error(f"Error en intento {intento + 1}: {e}")
            time.sleep(espera_entre_intentos)

    logger.info("No se encontraron productos luego de varios intentos.\n")
    return []




