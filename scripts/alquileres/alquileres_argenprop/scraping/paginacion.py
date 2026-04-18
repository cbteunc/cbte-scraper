from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
import logging.config

logging.config.fileConfig('logging_config/logging.conf')
logger = logging.getLogger('root')

def obtener_total_paginas(driver):
    """Devuelve la cantidad total de páginas basada en los botones de paginación."""
    try:
        # Esperar explícitamente a que aparezcan los botones de paginación
        WebDriverWait(driver, 3000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.pagination.pagination--links"))
        )

        ul_paginacion = driver.find_element(By.CSS_SELECTOR, "ul.pagination.pagination--links")
        paginas = ul_paginacion.find_elements(By.CSS_SELECTOR, "li.pagination__page")

        numeros = []
        for pagina in paginas:
            if pagina.find_elements(By.CSS_SELECTOR, "span"):
                enlace = pagina.find_element(By.CSS_SELECTOR, "span")
                texto = enlace.text.strip()

                # Filtrar botones "‹" y "›"
                if texto not in ["‹", "›"]:
                    try:
                        numero = int(texto)
                        numeros.append(numero)
                    except ValueError:
                        continue  # Ignorar si no es número

        if numeros:
            total_paginas = max(numeros)
        else:
            logger.warning("No se pudo extraer correctamente el número de páginas. Asumiendo una sola página por defecto...")
            total_paginas = 1
        logger.info(f"Total de páginas detectadas: {total_paginas}")
        return total_paginas

    except Exception as e:
        logger.info(f"Error al obtener total de páginas: {e}")
        return 1


