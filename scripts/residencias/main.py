from scraping.navegador import crear_driver
from scraping.ruka import scrapear_ruka
from scraping.roomgo import scrapear_roomgo
from utils.rendimiento import medir_recursos
from utils.archivos import guardar_en_excel_residencias
import pandas as pd
import logging
import logging.config

logging.config.fileConfig('logging_config/logging.conf')
logger = logging.getLogger('root')

def main():

    residencias_fallidas = []

    logger.info("===========INICIANDO SCRAPING DE RESIDENCIAS===========\n")

    with medir_recursos():

        # ── RuKa ──────────────────────────────────────────────────────────
        logger.info("Scrapeando RuKa Residencias...")
        try:
            driver = crear_driver()
            opciones = scrapear_ruka(driver)
            driver.quit()
            guardar_en_excel_residencias(opciones, "ruka")
        except Exception as e:
            logger.critical(f"Error al procesar RuKa: {e}")
            residencias_fallidas.append("rukaresidencia.com.ar")
        finally:
            driver.quit()

        # ── Roomgo ────────────────────────────────────────────────────────
        logger.info("Scrapeando Roomgo Córdoba...")
        try:
            driver = crear_driver()
            publicaciones = scrapear_roomgo(driver)
            driver.quit()
            guardar_en_excel_residencias(publicaciones, "roomgo")
        except Exception as e:
            logger.critical(f"Error al procesar Roomgo: {e}")
            residencias_fallidas.append("roomgo.com.ar")
        finally:
            driver.quit()

    if residencias_fallidas:
        logger.info("Residencias que fallaron:")
        for r in residencias_fallidas:
            print(f"- {r}")
    else:
        logger.info("¡Todas las residencias se escrapearon correctamente!")

    logger.info("===========SCRAPING DE RESIDENCIAS FINALIZADO===========")

if __name__ == "__main__":
    main()
