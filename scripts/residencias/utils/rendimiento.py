import time
import psutil
from contextlib import contextmanager
import logging 
import logging.config 

logging.config.fileConfig('logging_config/logging.conf') 
logger = logging.getLogger('root')

@contextmanager
def medir_recursos():
    start_time = time.time()
    cpu_start = psutil.cpu_percent()
    mem_start = psutil.virtual_memory().used / (1024 ** 2)

    yield

    end_time = time.time()
    cpu_end = psutil.cpu_percent()
    mem_end = psutil.virtual_memory().used / (1024 ** 2)

    logger.info(f"Tiempo de ejecución: {(end_time - start_time) / 60:.2f} minutos")
    logger.info(f"Uso de CPU: {cpu_end - cpu_start:.2f}%")
