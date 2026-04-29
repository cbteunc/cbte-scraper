import pandas as pd
from utils.limpieza import aplanar_datos
import datetime
import os
import logging
import logging.config

logging.config.fileConfig('logging_config/logging.conf')
logger = logging.getLogger('root')

def agregar_fecha(nombre_base):
    """Agrega la fecha actual al nombre del archivo, respetando la extensión."""
    fecha_hoy = datetime.datetime.today().strftime("%d-%m-%Y")
    nombre, extension = os.path.splitext(nombre_base)
    return f"{nombre}_{fecha_hoy}{extension}"

def guardar_en_excel_residencias(datos, nombre_fuente):
    """
    Guarda listings de residencias en data/residencias/<nombre_fuente>_<fecha>.xlsx
    Columnas: Tipo, Cantidad_personas / Cantidad_compañeros, Precio, Fuente
    """
    if not datos:
        logger.critical(f"No se guardaron datos de {nombre_fuente}, lista vacía.")
        return

    carpeta = "data/residencias"
    os.makedirs(carpeta, exist_ok=True)

    archivo = os.path.join(carpeta, agregar_fecha(f"{nombre_fuente}.xlsx"))

    df = pd.DataFrame(datos)
    df.to_excel(archivo, index=False)
    logger.info(f"Datos de {nombre_fuente} guardados en {archivo}")
