import time
import logging 
import logging.config
from .extractores import wait_for_visible_text, wait_for_card_container, find_card_container
from .procesadores import *

logging.config.fileConfig('logging_config/logging.conf') 
logger = logging.getLogger('root')

def obtener_precios_pasajes_plataforma10(driver, url, lugar):
    productos_precios = []
    driver.get(url)
    
    try:
        wait_for_visible_text(driver, timeout=2)
        visible_text = driver.execute_script("return document.body.innerText;")
        
        if colectivos_no_disponibles(visible_text):
            logger.error(f"No hay colectivos hacia esa zona")
            return []
        
        if fecha_no_disponible(visible_text):
            logger.error(f"No hay colectivos para esa fecha")
            return []
        
        # Esperar hasta que las tarjetas estén presentes
        wait_for_card_container(driver, timeout=40)
        
        # Esperar a que se estabilice la ui
        time.sleep(2)
        
        cards_container = find_card_container(driver)
        cards = get_card_list(cards_container)
    except Exception as e:
        raise Exception(f"Error inesperado: {e}")
    
    for card in cards:
        try:
            company_name = get_nombre_empresa(card)
        except Exception as e:
            raise Exception(f"Error en una empresa: {e}")
            
        seat_types_list = get_seat_type_list(card)

        for seat_type_button in seat_types_list:
            seat_type = get_seat_type(seat_type_button)
            price = get_price(seat_type_button)

            productos_precios.append({
                "Origen": "Cordoba",
                "Destino": get_destino(lugar),
                "Empresa": company_name,
                "Precio": price,
                "Tipo": seat_type
            })

    return productos_precios 