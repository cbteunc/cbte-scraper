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

def guardar_en_excel(datos):
    """Guarda los datos de consumo eléctrico en un archivo xlsx dentro de 'data'."""
    if datos:
        filas = aplanar_datos(datos)  # Aplanar estructura anidada

        carpeta = "data/electricidad"
        os.makedirs(carpeta, exist_ok=True)

        archivo = os.path.join(carpeta, agregar_fecha("consumo_electrico.xlsx"))

        df_nuevo = pd.DataFrame(filas, dtype=str)

        if os.path.exists(archivo):
            df_existente = pd.read_excel(archivo, dtype=str)
            df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
        else:
            df_final = df_nuevo

        df_final.to_excel(archivo, index=False)
        logger.info(f"Datos guardados en {archivo}")
    else:
        logger.critical("No se guardaron datos, ocurrió un error.")
