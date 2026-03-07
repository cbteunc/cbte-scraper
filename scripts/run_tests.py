import subprocess
import sys

SCRIPTS_PATH = "scripts"

# Lista de directorios que contienen tests que se quieren ejecutar
TEST_DIRS = [
    "Supermercados/supermercados_vea/tests",
]

def main():
    # Agregar el prefijo con la dirección de los scripts
    PATHS = [f"{SCRIPTS_PATH}/{dir}" for dir in TEST_DIRS]
    
    # Comando para ejecutar los tests
    cmd = ["pytest", "--import-mode=importlib"] + PATHS

    result = subprocess.run(cmd)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()