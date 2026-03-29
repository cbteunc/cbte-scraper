import os
import datetime
import pandas as pd
from utils.limpieza import procesar_destino
import logging 
import logging.config 

logging.config.fileConfig('logging_config/logging.conf') 
logger = logging.getLogger('root')

def agregar_fecha(nombre_base):
    """Agrega la fecha actual al nombre del archivo, respetando la extensión."""
    fecha_hoy = datetime.datetime.today().strftime("%d-%m-%Y")
    
    # Separar la extensión
    nombre, extension = os.path.splitext(nombre_base)
    
    return f"{nombre}_{fecha_hoy}{extension}"

def guardar_en_excel(pasajes, lugar):
    """Guarda los productos en un archivo Excel con el nombre de la subcategoría."""
    if not pasajes:
        logger.info("No hay pasajes para guardar.")
        return

    # Ruta relativa para ir a la carpeta superior y luego a "data"
    directorio = os.path.abspath(os.path.join(".", "data/colectivos/plataforma10"))

    os.makedirs(directorio, exist_ok=True) 

    nombre_archivo = os.path.join(directorio, agregar_fecha(f"{procesar_destino(lugar).replace(" ", "_")}.xlsx"))

    df = pd.DataFrame(pasajes)
    df.to_excel(nombre_archivo, index=False)

    logger.info(f"Datos guardados correctamente en '{nombre_archivo}'")