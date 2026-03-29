import pytest
import pandas as pd
from pathlib import Path
import re
import pytest_check as check
from ..config import destinos
from ..utils.limpieza import procesar_destino

# Datos y funciones auxiliares
ZONAS_SIN_COLECTIVO = [
    "Bell-Ville/19/302",    # No tiene colectivos que lleven ahí desde Córdoba de forma directa (28/03/2026)
    "La-Carlota/19/387",    # No tiene colectivos que lleven ahí desde Córdoba (28/03/2026)
    "Marcos-Juarez/19/303", # No tiene colectivos que lleven ahí desde Córdoba (28/03/2026)
    "Rio-Segundo/19/297",   # No tiene colectivos que lleven ahí desde Córdoba de forma directa (28/03/2026)
    "Ushuaia/19/1515",      # No tiene colectivos que lleven ahí desde Córdoba (28/03/2026)
    "Viedma/19/713"         # No tiene colectivos que lleven ahí desde Córdoba (28/03/2026)
]

CANTIDAD_CATEGORIAS_ESPERADAS = 47 - len(ZONAS_SIN_COLECTIVO)
PATH_DATOS = "data/colectivos/plataforma10"

excel_files = sorted(Path(PATH_DATOS).glob("*.xlsx"))

def hay_fila_vacia(df, nombre_columna):
    vacias = df[nombre_columna].isna() | df[nombre_columna].astype(str).str.strip().eq("")

    return vacias.any()

# Tests
@pytest.mark.parametrize("file", excel_files)
def test_columnas_no_vacias(file):
    df = pd.read_excel(file)

    for col in ["Origen", "Destino", "Empresa", "Precio", "Tipo"]:
        check.is_false(
            hay_fila_vacia(df, col),
            f"La columna '{col}' del archivo '{file}' tiene celdas vacías.",
        )

@pytest.mark.parametrize("file", excel_files)
def test_precio_es_numero(file):
    df = pd.read_excel(file)
    col = "Precio"

    converted = pd.to_numeric(df[col], errors="coerce")
    errores = df[converted.isna()]

    assert (
        errores.empty
    ), f"Hay valores de '{col}' no convertibles a float en el archivo {file}."


def test_cantidad_destinos_esperados():
    assert (
        len(destinos)-len(ZONAS_SIN_COLECTIVO) == CANTIDAD_CATEGORIAS_ESPERADAS
    ), f"Se esperaba tener que scrapear {CANTIDAD_CATEGORIAS_ESPERADAS} categorías, pero está configurado para que se scrapeen solo {len(destinos)}."


def test_cantidad_destinos():
    assert len(excel_files) == len(destinos) - len(ZONAS_SIN_COLECTIVO), "Hay una cantidad distinta de archivos guardados a la cantidad de categorías deseadas."

@pytest.mark.parametrize("destino", sorted(destinos))
def test_todas_destinos_scrapeados(destino):
    # Destino que se esperaba que no tuviera colectivos
    if destino in ZONAS_SIN_COLECTIVO:
        return

    # Destino que se espera que tenga colectivos
    has_file = False

    for file in excel_files:        
        # Reconvertimos el nombre
        converted_name = procesar_destino(destino).replace(" ", "_")
        has_file = file.name.startswith(converted_name)

        if has_file:
            break

    assert has_file, f"No se encontró una archivo asociado a la categoría {destino}"

@pytest.mark.parametrize("file", excel_files)
def test_nombre_de_archivo_valido(file):
    # Verificar que el nombre del archivo sigue un formato esperado
    assert re.fullmatch(r"[A-Za-z0-9._-]+", file.name.replace("ñ", "n")) is not None, f"El nombre del archivo {file.name} contiene espacios o caractéres inválidos."