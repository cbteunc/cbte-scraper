import re

def limpiar_precio(texto_precio):
    """
    Limpia el precio.
    """
    # Quitar espacios en blanco
    texto_precio = texto_precio.strip()
    
    # Quitar símbolos comunes (ejemplo $, €, %, espacios)
    for simbolo in ['$', '€', '%', ' ', '/mes']:
        texto_precio = texto_precio.replace(simbolo, '')
    
    # Quitar puntos de miles y cambiar coma decimal por punto
    texto_precio = texto_precio.replace('.', '').replace(',', '.')
    
    try:
        precio_float = float(texto_precio)
    except ValueError:
        precio_float = None  # O el valor que quieras poner si no se puede parsear
    
    # Formatear con 3 decimales para conservar ceros finales si querés string
    precio_formateado = f"{precio_float:.3f}" if precio_float is not None else None
    
    return precio_formateado


def limpiar_oferta(oferta):
    """Elimina todas las letras y deja solo los números en la oferta."""
    numeros = re.findall(r"\d+", oferta)  # Buscar solo números
    return " ".join(numeros) if numeros else ""  # Unir números separados por espacios
