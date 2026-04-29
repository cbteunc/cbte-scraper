import subprocess
import os
import logging 
import logging.config 
import time

logging.config.fileConfig('logging_config/logging.conf') 
logger = logging.getLogger('root')

# Lista de paths a cada main.py
scripts = [
    "internet/main.py",
    "telefonia/main.py",
    "alquileres/alquileres_argenprop/main.py",
    "alquileres/alquileres_lavoz/main.py",
    "libreria/libreria_ferniplast/main.py",
    "libreria/libreria_grafitti/main.py",
    "libreria/libreria_pencilbag/main.py",
    "supermercados/supermercados_disco/main.py",
    "supermercados/supermercados_vea/main.py",
    "supermercados/supermercados_carrefour/main.py",
    "energia_electrica/main.py",
    "residencias/main.py",
    "upload_to_drive.py", # Comentar línea si no lo querés subir a drive
    "erase_data.py", # Comentar esta línea si no lo vas a subir a drive 
    "erase_log.py" # Comentar esta línea si no lo vas a subir a drive
]

def run_all():
    # --- Ejecutar secuencialmente ---
    for script in scripts:
        path = os.path.join(os.path.dirname(__file__), script)
        logger.info(f"Ejecutando script: {script}")

        try:
            result = subprocess.run(["python", path], check=True, capture_output=True, text=True)

            logger.info(f"{script} finalizado correctamente.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error al ejecutar {script}. Código de salida: {e.returncode}")
            logger.error(f"Stderr:\n{e.stderr}")

    logger.info("Todos los scripts fueron procesados.")

if __name__ == "__main__":
    run_all()
