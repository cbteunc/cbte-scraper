def limpiar_precio(texto_precio):
    """
    Limpia el precio.
    """
    # Quitar espacios en blanco
    texto_precio = texto_precio.strip()
    
    # Quitar símbolos comunes 
    for simbolo in ['$', '€']:
        texto_precio = texto_precio.replace(simbolo, '')
    
    # Quitar puntos de miles y cambiar coma decimal por punto
    texto_precio = texto_precio.replace('.', '').replace(',', '.')
    
    # Quitar el prefijo "ARS"
    texto_precio = texto_precio.removeprefix("ARS ")
    
    try:
        precio_float = float(texto_precio)
    except ValueError:
        precio_float = None  # N/A
    
    # Formatear con 3 decimales para conservar ceros finales 
    precio_formateado = f"{precio_float:.3f}" if precio_float is not None else None
    
    return precio_formateado

# Nombre limpio a mano para No cargar tanto el scraping
def procesar_destino(destino_completo):
    partes = destino_completo.split("/")
    destino_con_guiones = partes[0]
    return destino_con_guiones.replace("-", " ")