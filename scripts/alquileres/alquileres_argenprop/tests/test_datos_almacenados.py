import pytest
import pandas as pd
from pathlib import Path
import re
import pytest_check as check

# Datos y funciones auxiliares
PATH_DATOS = "data/alquileres/argenprop"

excel_files = sorted(Path(PATH_DATOS).glob("*.xlsx"))

def hay_fila_vacia(df, nombre_columna):
    vacias = df[nombre_columna].isna() | df[nombre_columna].astype(str).str.strip().eq("")

    return vacias.any()

# Tests
@pytest.mark.parametrize("file", excel_files)
def test_columnas_no_vacias(file):
    df = pd.read_excel(file)

    for col in ["Barrio", "Precio"]:
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

@pytest.mark.parametrize("file", excel_files)
def test_nombre_de_archivo_valido(file):
    # Verificar que el nombre del archivo sigue un formato esperado
    assert re.fullmatch(r"[A-Za-z0-9._-]+", file.name) is not None, f"El nombre del archivo {file.name} contiene espacios o caractéres inválidos."