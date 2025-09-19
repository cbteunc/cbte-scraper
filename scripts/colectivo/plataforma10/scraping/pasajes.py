from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.limpieza import limpiar_precio, procesar_destino
import logging 
import logging.config 

logging.config.fileConfig('logging_config/logging.conf') 
logger = logging.getLogger('root')

def obtener_precios_pasajes_plataforma10(driver, url, lugar):
    productos_precios = []
    driver.get(url)
    
    try:
        # Esperar hasta que las tarjetas estén presentes
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".SearchResultCardV2_card-v2-container__QjROe"))
        )
        cards = driver.find_elements(By.CSS_SELECTOR, ".SearchResultCardV2_card-v2-container__QjROe")
    except Exception as e:
        logger.error(f"No se encontraron tarjetas: {e}")
        return []
    
    for card in cards:
        
        try:
            # Empresa (alt del logo dentro del contenedor de empresa)
            img = card.find_element(By.CSS_SELECTOR, "figure.SearchResultCardV2_trip-image-container__W3JsI img")
            company_name = img.get_attribute("alt").strip()
        except Exception as e:
            try:
                # Algunas empresas no tienen imagen, si no solo texto
                span = card.find_element(By.CSS_SELECTOR, "span.SearchResultCardV2_company-name-fallback__Kbcc2")
                company_name = span.text.strip()
            except Exception as e:
                logger.critical(f"Error en una empresa: {e}")
            
        try:
            price_element = card.find_element(By.CSS_SELECTOR, ".SearchResultCardV2_trip-price-value__iKYIv")
            price = price_element.text.strip()
        except Exception as e:
            logger.critical(f"Error en un precio: {e}")
            
        try:
            seat_type_element = card.find_element(By.CSS_SELECTOR, ".SearchResultCardV2_seat-type-text__I_hBZ")
            seat_type = seat_type_element.text.strip()
        except Exception as e:
            logger.warning(f"No se pudo obtener tipo de asiento: {e}")
            seat_type = None     

        if price and company_name:
            productos_precios.append({
                "Origen": "Cordoba",
                "Destino": procesar_destino(lugar),
                "Empresa": company_name,
                "Precio": limpiar_precio(price),
                "Tipo": seat_type
            })
        else:
            logger.critical("No hay precios para scrapear")

    return productos_precios 