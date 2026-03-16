from scraping.simulador_epec import obtener_datos_simulador
# from utils.archivos import guardar_en_excel
from utils.rendimiento import medir_recursos
import logging
import logging.config

logging.config.fileConfig('logging_config/logging.conf')
logger = logging.getLogger('root')

def main():
    with medir_recursos():
        logger.info("===========INICIANDO SCRAPING DE ENERGIA ELECTRICA===========\n")

        try:
            logger.debug("Obteniendo datos del simulador de epec")
            datos_simulador = obtener_datos_simulador()
            logger.info(f"Datos simulador obtenidos: {datos_simulador}")
            # guardar_en_excel(datos_simulador)
            # logger.debug("Datos del simulador guardados en Excel")
        except Exception as e:
            logger.error(f"Error al obtener o guardar los datos del simulador: {e}") 

    logger.info("===========SCRAPING DE ENERGIA ELECTRICA FINALIZADO===========\n")


if __name__ == "__main__":
    main()    
