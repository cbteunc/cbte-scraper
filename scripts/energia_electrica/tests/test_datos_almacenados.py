import pytest
import pandas as pd
from pathlib import Path
import pytest_check as check

PATH_DATOS = "data/electricidad"

excel_files = sorted(Path(PATH_DATOS).glob("*.xlsx"))


def hay_vacios(df, columna):
    vacios = df[columna].isna() | df[columna].astype(str).str.strip().eq("")
    return vacios.any()


@pytest.mark.parametrize("file", excel_files)
def test_columnas_no_vacias(file):
    df = pd.read_excel(file)

    columnas = [
        "consumo_total (kWh)",
        "importe_total",
        "categoria",
        "porcentaje_categoria",
        "kwh_categoria",
        "equipo",
        "kwh_equipo",
    ]

    for col in columnas:
        check.is_false(
            hay_vacios(df, col),
            f"La columna '{col}' del archivo '{file}' tiene valores vacíos."
        )

@pytest.mark.parametrize("file", excel_files)
def test_columnas_numericas(file):
    df = pd.read_excel(file)

    columnas_numericas = [
        "consumo_total (kWh)",
        "importe_total",
        "kwh_categoria",
        "kwh_equipo",
    ]

    for col in columnas_numericas:
        converted = pd.to_numeric(df[col], errors="coerce")

        assert converted.notna().all(), \
            f"La columna {col} tiene valores no numéricos en {file}"

@pytest.mark.parametrize("file", excel_files)
def test_kwh_categoria_correcto(file):
    df = pd.read_excel(file)

    grouped = df.groupby("categoria")

    for categoria, grupo in grouped:
        suma_equipos = grupo["kwh_equipo"].sum()
        kwh_categoria = grupo["kwh_categoria"].iloc[0]

        assert abs(suma_equipos - kwh_categoria) < 0.01, \
            f"Error en {categoria}: suma equipos {suma_equipos} != categoria {kwh_categoria}"

@pytest.mark.parametrize("file", excel_files)
def test_consumo_total(file):
    df = pd.read_excel(file)

    consumo_total = df["consumo_total (kWh)"].iloc[0]
    suma_equipos = df["kwh_equipo"].sum()

    assert abs(consumo_total - suma_equipos) < 0.5, \
        f"Consumo total incorrecto en {file}"

@pytest.mark.parametrize("file", excel_files)
def test_porcentaje_formato(file):
    df = pd.read_excel(file)

    assert df["porcentaje_categoria"].str.endswith("%").all(), \
        f"Hay porcentajes mal formateados en {file}"

@pytest.mark.parametrize("file", excel_files)
def test_esquema(file):
    df = pd.read_excel(file)

    expected_columns = [
        "consumo_total (kWh)",
        "importe_total",
        "categoria",
        "porcentaje_categoria",
        "kwh_categoria",
        "equipo",
        "kwh_equipo",
    ]

    assert list(df.columns) == expected_columns
