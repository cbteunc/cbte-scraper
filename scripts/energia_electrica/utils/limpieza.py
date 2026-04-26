import re

def limpiar_kwh(texto):
    """Extrae solo el número de un texto con kWh. Ej: '90 kWh' -> '90.000'"""
    numeros = re.findall(r"\d+\.?\d*", texto)
    if numeros:
        return f"{float(numeros[0]):.3f}"
    return None

def limpiar_importe(texto_importe):
    """Limpia el importe. Ej: '26124.2' -> '26124.200'"""
    texto_importe = str(texto_importe).strip()
    
    for simbolo in ['$', '€', '%', ' ', '/mes']:
        texto_importe = texto_importe.replace(simbolo, '')
    
    texto_importe = texto_importe.replace('.', '').replace(',', '.')
    
    try:
        importe_float = float(texto_importe)
    except ValueError:
        importe_float = None
    
    return f"{importe_float:.3f}" if importe_float is not None else None

def aplanar_datos(datos):
    """
    Convierte la estructura anidada en una lista de filas planas para Excel.
    Cada fila representa un equipo con sus datos de contexto.
    """
    filas = []
    consumo_total = limpiar_kwh(datos["Consumo"])
    importe_total = limpiar_importe(datos["Importe"])
    
    for categoria in datos["categorias"]:
        nombre_categoria = categoria["categoria"]
        porcentaje = categoria["porcentaje"]
        kwh_categoria = limpiar_kwh(categoria["kwh"])
        
        for equipo in categoria["equipos"]:
            fila = {
                "consumo_total (kWh)": consumo_total,
                "importe_total": importe_total,
                "categoria": nombre_categoria,
                "porcentaje_categoria": porcentaje,
                "kwh_categoria": kwh_categoria,
                "equipo": equipo["nombre"],
                "kwh_equipo": limpiar_kwh(equipo["kwh"]),
            }
            filas.append(fila)
    
    return filas
