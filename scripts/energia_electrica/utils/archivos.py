import pandas as pd
from utils.limpieza import limpiar_oferta, limpiar_precio
import datetime 
import os
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

def guardar_en_excel(datos):
    """Guarda los datos en un archivo xlsx dentro de la carpeta 'data'."""
    if datos:
        datos["oferta (MB)"] = limpiar_oferta(datos["oferta (MB)"])  # Unificar MB
        datos["precio"] = limpiar_precio(datos["precio"])  # Unificar precios
        
        # Crear la carpeta si no existe
        carpeta = "data/internet"
        os.makedirs(carpeta, exist_ok=True)

        # Generar el nombre del archivo con la fecha
        archivo = os.path.join(carpeta, agregar_fecha("servicios_internet.xlsx"))

        # Guardar los datos en Excel
        df_nuevo = pd.DataFrame([datos], dtype=str)

        if os.path.exists(archivo):
            df_existente = pd.read_excel(archivo, dtype=str)
            df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
        else:
            df_final = df_nuevo

        df_final.to_excel(archivo, index=False)
        logger.info(f"Datos guardados en {archivo}")
    else:
        logger.crititcal("No se guardaron datos, ocurrió un error.")