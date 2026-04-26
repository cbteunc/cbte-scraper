from scraping.navegador import iniciar_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

logger = logging.getLogger('root')


def clickear_categoria(driver, nombre_categoria, wait):
    xpath = f"//div[contains(@class,'circulo')]//div[@class='titulo' and contains(text(),'{nombre_categoria}')]//following-sibling::div[@class='mas']/button"
    boton = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    driver.execute_script("arguments[0].click();", boton)
    logger.debug(f"Categoría '{nombre_categoria}' clickeada")

def cerrar_modal(driver, wait):
    """Clicks Aceptar to close the modal."""
    boton_aceptar = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class,'btn-azul-epec') and contains(.,'Aceptar')]"
    )))
    driver.execute_script("arguments[0].click();", boton_aceptar)
    logger.debug("Modal cerrado con Aceptar")
    # Wait for modal to disappear
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-content")))
    logger.debug("Modal cerrado correctamente")

def seleccionar_ng_option(driver, wait, select_id, texto_opcion):
    """Clicks an ng-select dropdown and selects an option by text."""
    logger.debug(f"Seleccionando '{texto_opcion}' en select '{select_id}'")
    select = wait.until(EC.element_to_be_clickable((By.ID, select_id)))
    driver.execute_script("arguments[0].click();", select)
    time.sleep(0.5)

    input_box = select.find_element(By.CSS_SELECTOR, "input[role='combobox']")
    input_box.send_keys(texto_opcion)
    time.sleep(0.5)

    opcion = wait.until(EC.element_to_be_clickable((
        By.XPATH, f"//ng-dropdown-panel//span[contains(text(),'{texto_opcion}')]"
    )))
    driver.execute_script("arguments[0].click();", opcion)
    logger.debug(f"Opción '{texto_opcion}' seleccionada")


def agregar_equipo(driver, wait, subcategoria, equipo, cantidad, uso_diario):
    seleccionar_ng_option(driver, wait, "subCcategoriaSeleccionada", subcategoria)
    time.sleep(1)
    seleccionar_ng_option(driver, wait, "equipoSeleccionado", equipo)

    input_cantidad = wait.until(EC.presence_of_element_located((By.ID, "cantidad")))
    input_cantidad.clear()
    input_cantidad.send_keys(str(cantidad))

    input_uso = driver.find_element(By.ID, "usoDiario")
    input_uso.clear()
    input_uso.send_keys(str(uso_diario))

    # More specific selector for Agregar button
    boton_agregar = driver.find_element(
        By.XPATH, "//button[contains(@class,'btn-azul-epec') and contains(.,'Agregar')]"
    )
    driver.execute_script("arguments[0].click();", boton_agregar)
    logger.debug("Botón Agregar clickeado")

    # Wait for Angular to render the row instead of fixed sleep
    wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".d-none.d-lg-block .tabla-equipos td"
    )))
    logger.debug("Fila de datos detectada en tabla")


def obtener_tabla_equipos(driver, wait):
    """Scrapes the desktop tabla-equipos after adding an equipment."""
    logger.debug("Obteniendo tabla de equipos")
    tabla = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".d-none.d-lg-block .tabla-equipos"
    )))
    filas = tabla.find_elements(By.CSS_SELECTOR, "tr")
    logger.debug(f"Filas encontradas en tabla: {len(filas)}")

    resultados = []
    for fila in filas[1:]:  # skip header row
        celdas = fila.find_elements(By.CSS_SELECTOR, "td")
        if celdas:
            fila_data = {
                "equipo":          celdas[0].text,
                "cantidad":        celdas[1].text,
                "uso_diario":      celdas[2].text,
                "consumo_diario":  celdas[3].text,
                "consumo_mensual": celdas[4].text,
            }
            logger.debug(f"Fila obtenida: {fila_data}")
            resultados.append(fila_data)

    return resultados


def obtener_datos_simulador():
    """
    Extrae datos del simulador de consumo de EPEC.
    Abre la categoría Tecnología, agrega un Cargador de celular genérico
    con cantidad 1 y uso diario 8hs, y retorna los resultados de la tabla.
    """
    driver = iniciar_driver()

    try:
        logger.debug("Abriendo página del simulador EPEC")
        driver.get("https://www.epec.com.ar/tramites/simulador-de-consumo")

        wait = WebDriverWait(driver, 10)

        # 1. Click the Tecnología category to open the modal
        clickear_categoria(driver, "Tecnología", wait)

        # 2. Wait for modal to appear
        logger.debug("Esperando que aparezca el modal")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content")))
        logger.debug("Modal visible")

        # 3. Fill form and click Agregar
        agregar_equipo(
            driver, wait,
            subcategoria="Informática",
            equipo="Cargador de celular genérico",
            cantidad=1,
            uso_diario=8
        )

        agregar_equipo(
            driver, wait,
            subcategoria="Informática",
            equipo="Notebook",
            cantidad=1,
            uso_diario=8
        )

        # 4. Scrape results from tabla-equipos
        resultados = obtener_tabla_equipos(driver, wait)
        logger.debug(f"Total de equipos en tabla: {len(resultados)}")

        cerrar

        return resultados

    except Exception as e:
        logger.error(f"Error EPEC: {e}", exc_info=True)
        return None

    finally:
        driver.quit()
