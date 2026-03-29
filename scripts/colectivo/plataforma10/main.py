
from scraping.navegador import crear_driver
from config import destinos, datos, pagina
from scraping.pasajes.scrapper import obtener_precios_pasajes_plataforma10
from utils.archivos import guardar_en_excel
from utils.excepciones import get_traceback
import logging 
import logging.config 


logging.config.fileConfig('logging_config/logging.conf') 
logger = logging.getLogger('root')

N_REINTENTOS = 3

def main():

    logger.info("===========INICIANDO SCRAPING DE PLATAFORMA10 ===========\n")
    driver = crear_driver()

    for lugar in destinos: 
        link_destino = pagina + lugar + datos
        logger.info(f"Scrapeando {link_destino}...\n")
        excepciones_encontradas = []
        
        for i in range(3):
            logger.info(f"Intento {i+1}/{N_REINTENTOS}:")
            try:
                pasajes = obtener_precios_pasajes_plataforma10(driver, link_destino, lugar)
                guardar_en_excel(pasajes, lugar)
                break
            except Exception as e:
                logger.error(f"No se pudo extraer correctamente la información {link_destino}")
                excepciones_encontradas.append(e)
        
        if len(excepciones_encontradas) == N_REINTENTOS:
            info_excepciones = [get_traceback(e) for e in excepciones_encontradas]
            logger.critical(f"No se pudo scrapear {link_destino} correctamente")
            
            logger.debug("================================================")
            
            for e in info_excepciones:
                logger.debug(e)
                
            logger.debug("================================================")

    driver.quit()
    logger.info("===========SCRAPING DE PLATAFORMA10 FINALIZADO===========")


if __name__ == "__main__":
    main()
