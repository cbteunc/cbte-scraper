import re

def limpiar_nombre(nombre):
    """Elimina la palabra 'Producto' al inicio del nombre, con o sin espacio."""
    return re.sub(r"^Producto\s*", "", nombre)  

def limpiar_precio(texto_precio):
    """
    Limpia el precio.
    """
    # Quitar espacios en blanco
    texto_precio = texto_precio.strip()
    
    # Quitar detalles del descuento
    texto_precio = texto_precio.split("-")[0]
    
    # Quitar símbolos comunes (ejemplo $, €, %, espacios)
    for simbolo in ['$', '€', '%', ' ', '/mes', 'c/u']:
        texto_precio = texto_precio.replace(simbolo, '')
    
    # Quitar puntos de miles y cambiar coma decimal por punto
    texto_precio = texto_precio.replace('.', '').replace(',', '.')
    
    try:
        precio_float = float(texto_precio)
    except ValueError:
        precio_float = None  

    precio_formateado = f"{precio_float:.3f}" if precio_float is not None else None
    
    return precio_formateado

def filtrar_productos(productos):
    """Filtra los productos que son 'slider' o tienen todos los atributos 'No disponible'."""
    productos_filtrados = []
    for producto in productos:
        # Filtrar productos llamados 'slider' o con atributos 'No disponible'
        if "slider" not in producto["Producto"].lower() and \
            not (producto["Precio"] == "No disponible" and
                producto["Precio original"] == "No disponible" and
                producto["Beneficio Mi CRF"] == "No"):
            productos_filtrados.append(producto)

    return productos_filtrados

def limpiar_url(url):
    return re.sub(r"^https://www\.carrefour\.com\.ar/", "", url)