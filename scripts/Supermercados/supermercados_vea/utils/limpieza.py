import re

def limpiar_precio(texto_precio):
    """
    Limpia el precio.
    """
    # Quitar espacios en blanco
    texto_precio = texto_precio.strip()
    
    # Quitar símbolos comunes (ejemplo $, €, %, espacios)
    for simbolo in ['$', '€', '%', ' ', '/mes', 'c/u']:
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

def limpiar_precio_kg_lt(texto):
    texto = texto.lower()
    unidad_match = re.search(r"x\s*(\d*\s*(?:gr\.|kg|lt|un))", texto)
    precio_match = re.search(r"\$\s*([\d\.,]+)", texto)

    if not unidad_match or not precio_match:
        return "No disponible"

    unidad = unidad_match.group(1).replace(' ', '')
    precio_str = precio_match.group(1).replace('.', '').replace(',', '.')

    try:
        precio = float(precio_str)
    except ValueError:
        return "No disponible"

    if unidad in ["kg", "lt", "un"]:
        return f"{precio:.2f}"
    elif unidad.endswith("gr."):
        # Extraer la cantidad en gramos
        try:
            gramos = int(unidad.replace("gr.", ""))
        except ValueError:
            return "No disponible"
        
        factor = 10 if gramos == 100 else 1000 / gramos
        precio_kg = precio * factor
        return f"{precio_kg:.2f}"
    else:
        return "No disponible"

def filtrar_productos(productos):
    """Filtra los productos que son 'slider' o tienen todos los atributos 'No disponible'."""
    productos_filtrados = []
    for producto in productos:
        # Filtrar productos llamados 'slider' o con atributos 'No disponible'
        if "slider" not in producto["Producto"].lower() and \
           not (producto["Precio"] == "No disponible" and
                producto["Producto"] == "No disponible"):
            productos_filtrados.append(producto)

    return productos_filtrados

def limpiar_url(url):
    fixed_url = re.sub(r"^https://www\.vea\.com\.ar/", "", url)
    
    # Simplifica ciertas urls, deja igual a otras
    fixed_url = fixed_url.split("?")[0]
    
    # Convierte espacios en guiones
    fixed_url = fixed_url.replace(" ", "-")
    
    # Convierte enies en enes
    fixed_url = fixed_url.replace('ñ', 'n')
    
    return fixed_url