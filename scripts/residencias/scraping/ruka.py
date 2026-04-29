import time
import re
import logging
import logging.config

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.limpieza import limpiar_precio

logging.config.fileConfig('logging_config/logging.conf')
logger = logging.getLogger('root')

URL = "https://www.rukaresidencia.com.ar"
_SLEEP_CARGA = 5

def extraer_cantidad_desde_tipo(texto):
    texto = texto.lower()

    if "cuádruple" in texto or "cuadruple" in texto:
        return 4
    elif "triple" in texto:
        return 3
    elif "doble" in texto:
        return 2
    elif "individual" in texto:
        return 1
    return None


def extraer_precios_limpios(lista_textos):
    """
    Wix rompe precios en spans:
    "$330." + "000" → reconstruir
    """
    precios = []
    for texto in lista_textos:
        encontrados = re.findall(r'\$\s?[\d\.]+', texto)
        precios.extend(encontrados)
    return precios


def scrapear_bloque(driver, id_tipos, id_precios, titulo):
    resultados = []

    try:
        tipos_el = driver.find_element(By.ID, id_tipos)
        precios_el = driver.find_element(By.ID, id_precios)
    except Exception:
        logger.warning(f"[RuKa] No se encontró bloque: {titulo}")
        return resultados

    tipos = [
        t.text.strip()
        for t in tipos_el.find_elements(By.TAG_NAME, "p")
        if t.text.strip()
    ]

    precios_raw = [
        p.text.strip()
        for p in precios_el.find_elements(By.TAG_NAME, "p")
        if p.text.strip()
    ]

    precios = extraer_precios_limpios(precios_raw)

    for i in range(min(len(tipos), len(precios))):
        tipo = tipos[i]
        precio = limpiar_precio(precios[i])
        cantidad_compañeros = extraer_cantidad_desde_tipo(tipo)

        if not precio or precio < 10000:
            continue

        resultados.append({
            "Titulo": titulo,
            "Tipo": tipo,
            "Cantidad_Compañeros": cantidad_compañeros,
            "Precio": precio
        })

    return resultados

def scrapear_ruka(driver):
    logger.info(f"[RuKa] Cargando {URL}")
    driver.get(URL)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    time.sleep(_SLEEP_CARGA)

    resultados = []

    # Plaza España
    resultados += scrapear_bloque(
        driver,
        "comp-k8hwzbcl",
        "comp-k8hxp7ia",
        "RUKA PLAZA ESPAÑA"
    )

    # Vélez Sarsfield
    resultados += scrapear_bloque(
        driver,
        "comp-k8hy9zci",
        "comp-k8hy9zen",
        "RUKA VÉLEZ SARSFIELD"
    )

    # Pisos compartidos
    resultados += scrapear_bloque(
        driver,
        "comp-k8hzcrx5",
        "comp-k8hzcry0",
        "PISOS COMPARTIDOS"
    )

    logger.info(f"[RuKa] {len(resultados)} precio(s) encontrado(s)")
    return resultados
