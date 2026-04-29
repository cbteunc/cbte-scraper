import re

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

def limpiar_precio(texto_precio):
    # Extrae solo números, puntos y comas
    match = re.search(r'[\d\.,]+', texto_precio)
    
    if not match:
        return None
    
    numero = match.group()
    
    # Formato argentino: 350.000 → 350000
    numero = numero.replace('.', '').replace(',', '.')

    try: 
        return float(numero)
    except ValueError:
        return None

def extraer_cantidad_compañeros(texto):
    match = re.search(r'\d+', texto)
    return int(match.group()) if match else None
