import pytest
import pandas as pd
from pathlib import Path
import pytest_check as check
from ..config import categorias_deseadas


# Datos y funciones auxiliares
CANTIDAD_CATEGORIAS_ESPERADAS = 49
PATH_DATOS = "data/supermercados/carrefour"

excel_files = sorted(Path(PATH_DATOS).glob("*.xlsx"))

def columna_vacia(df, nombre_columna):
    vacias = df[nombre_columna].isna() | df[nombre_columna].astype(str).str.strip().eq("")

    return vacias.any()

# Tests
@pytest.mark.parametrize("file", excel_files)
def test_columnas_no_vacias(file):
    df = pd.read_excel(file)
    cols = ["Producto", "Precio", "Precio original", "Tiene oferta", "Beneficio Mi CRF", "Precio x kg/lt"]

    for col in cols:
        vacias = df[col].isna() | df[col].astype(str).str.strip().eq("")
        check.is_false(
            vacias.any(),
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
def test_precio_original_es_numero(file):
    df = pd.read_excel(file)
    col = "Precio original"

    converted = pd.to_numeric(df[col], errors="coerce")
    errores = df[converted.isna()]

    assert (
        errores.empty
    ), f"Hay valores de '{col}' no convertibles a float en el archivo {file}."


def test_estan_todas_categorias():
    assert (
        len(categorias_deseadas) == CANTIDAD_CATEGORIAS_ESPERADAS
    ), f"Se esperaba tener que scrapear {CANTIDAD_CATEGORIAS_ESPERADAS} categorías, pero está configurado para que se scrapeen solo {len(categorias_deseadas)}."


def test_cantidad_categorias():
    assert len(excel_files) == len(
        categorias_deseadas
    ), "Hay una cantidad distinta de archivos guardados a la cantidad de categorías deseadas."

@pytest.mark.parametrize("categoria", sorted(categorias_deseadas))
def test_categorias_scrapeadas(categoria):
    has_file = False

    for file in excel_files:        
        # Esta conversión la hace automaticamente guardar_excel
        converted_name = categoria.replace("/", "_").replace("&", "_").replace("?", "_")
        has_file = file.name.startswith(converted_name)

        if has_file:
            break

    assert has_file, f"No se encontró una archivo asociado a la categoría {categoria}"
