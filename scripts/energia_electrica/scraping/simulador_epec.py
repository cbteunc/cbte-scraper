from scraping.navegador import iniciar_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logger = logging.getLogger('root')

def clickear_categoria(driver, wait, nombre_categoria):
    boton = wait.until(EC.element_to_be_clickable((By.XPATH,
        f"//div[contains(@class,'circulo')]//div[@class='titulo' and contains(text(),'{nombre_categoria}')]//following-sibling::div[@class='mas']/button"
    )))
    boton.click()
    time.sleep(1)

def seleccionar_ng_option(driver, wait, select_id, texto_opcion):
    input_el = driver.find_element(By.CSS_SELECTOR, f"#{select_id} input[role='combobox']")
    driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));", input_el)
    time.sleep(1)

    opcion = wait.until(EC.element_to_be_clickable((
        By.XPATH, f"//ng-dropdown-panel//div[contains(@class,'ng-option') and .//span[normalize-space()='{texto_opcion}']]"
    )))
    opcion.click()
    # logger.debug(f"Opción '{texto_opcion}' seleccionada")

def agregar(subcategoria, equipo, cant, usoDiario, driver, wait):
    seleccionar_ng_option(driver, wait, "subCcategoriaSeleccionada", subcategoria)

    seleccionar_ng_option(driver, wait, "equipoSeleccionado", equipo)

    input_cantidad = wait.until(EC.presence_of_element_located((By.ID, "cantidad")))
    input_cantidad.clear()
    input_cantidad.send_keys(cant)

    input_uso = driver.find_element(By.ID, "usoDiario")
    input_uso.clear()
    input_uso.send_keys(usoDiario)
        
    boton_agregar = driver.find_element(By.XPATH, "//button[contains(@class,'btn-azul-epec') and contains(.,'Agregar')]")
    boton_agregar.click()

def aceptar_modal(wait):
    boton_aceptar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'btn-azul-epec') and contains(.,'Aceptar')]")))
    boton_aceptar.click()

def obtener_resumen_pagina(driver, wait):
    # logger.debug("Obteniendo resumen de la página")

    # Wait for at least one accordion header to appear
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".accordion-header")))

    categorias = []
    accordion_headers = driver.find_elements(By.CSS_SELECTOR, ".accordion-header")

    for header in accordion_headers:
        titulo = header.find_element(By.CSS_SELECTOR, ".categoria-titulo").text
        kwh = header.find_element(By.CSS_SELECTOR, ".categoria-kwh").text
        porcentaje = header.find_element(By.CSS_SELECTOR, ".categoria-porcentaje").text

        # Get collapse id from the href e.g. "#collapseTwo" → "collapseTwo"
        collapse_id = header.find_element(By.CSS_SELECTOR, "a").get_attribute("href").split("#")[-1]

        equipos = []
        equipos_elements = driver.find_elements(By.CSS_SELECTOR, f"#{collapse_id} .equipo-subtitulos")
        for eq in equipos_elements:
            equipos.append({
                "nombre": eq.find_element(By.CSS_SELECTOR, ".equipo-titulo").text,
                "kwh":    eq.find_element(By.CSS_SELECTOR, ".equipo-kwh").text,
            })

        categorias.append({
            "categoria":  titulo,
            "porcentaje": porcentaje,
            "kwh":        kwh,
            "equipos":    equipos,
        })
        # logger.debug(f"Categoría: {titulo} | {kwh} | {porcentaje} | equipos: {equipos}")
    consumo_estimado = driver.find_element(By.XPATH,
        "//div[contains(@class,'mini-card')]//p[contains(text(),'Consumo estimado')]"
        "/following-sibling::div[@class='valor']//span[@class='numero']"
    ).text

    importe_estimado = driver.find_element(By.XPATH,
        "//div[contains(@class,'mini-card')]//p[contains(text(),'Importe estimado')]"
        "/following-sibling::div[@class='valor']//span[@class='numero']"
    ).text

    # logger.debug(f"Consumo estimado: {consumo_estimado} | Importe estimado: {importe_estimado}")

    return {"Consumo": consumo_estimado, "Importe": importe_estimado, "categorias": categorias}

def obtener_datos_simulador():

    driver = iniciar_driver()
    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://www.epec.com.ar/tramites/simulador-de-consumo")
        # logger.debug("Página cargada")
        time.sleep(2) 

        # HOGAR Y ELECTRODOMESTICOS
        clickear_categoria(driver, wait, "Hogar y electrodomésticos") 

        # Wait for modal
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content")))

        agregar("Iluminación", "Lámpara de bajo consumo de 11W", 3, 8, driver, wait)

        agregar("Iluminación", "Tubo fuorescente de 18W", 2, 5, driver, wait)
 
        agregar("Hogar", "Ventiladores de pie", 1, 1, driver, wait) 

        aceptar_modal(wait)

        time.sleep(2)

        # Tecnologia
        clickear_categoria(driver, wait, "Tecnología")

        # Wait for modal
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content")))

        agregar("Informática", "Cargador de celular genérico", 1, 8, driver, wait)
        agregar("Informática", "Notebook", 1, 8, driver, wait)

        aceptar_modal(wait)

        time.sleep(2)

        #Lavado y cocina
        clickear_categoria(driver, wait, "Lavado y Cocina")

        # Wait for modal
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content")))

        agregar("Heladera Y Frezeer", "Heladera con freezer", 1, 24, driver, wait)
        agregar("Lavado", "Lavarropas Semi-automático de 5kg.", 1, 1, driver, wait)

        aceptar_modal(wait)

        time.sleep(2)

        # Open all collapse panels at once before scraping
        driver.execute_script("""
            document.querySelectorAll('.collapseContent').forEach(el => {
                el.classList.add('show');
            });
        """)
        time.sleep(2)
        
        resultado = obtener_resumen_pagina(driver, wait)

        time.sleep(2)

        return resultado

    except Exception as e:
        logger.error(f"Error EPEC: {e}", exc_info=True)
        return None

    finally:
        driver.quit()
