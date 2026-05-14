from utils.limpieza import limpiar_precio, procesar_destino
from .extractores import (
    find_seat_type_list,
    find_card_list,
    find_imagen_empresa,
    find_span_nombre_empresa,
    find_seat_type_element,
    find_price_element,
)

# --- Listas ---
def get_seat_type_list(card):
    return find_seat_type_list(card)

def get_card_list(cards_container):
    return find_card_list(cards_container)

# --- Valores finales ---
def get_destino(lugar):
    return procesar_destino(lugar)

def get_nombre_empresa(card):
    try:
        img = find_imagen_empresa(card)
        
        # Nombre de la empresa (alt del logo dentro de su contenedor)
        return img.get_attribute("alt").strip()
    except Exception:
        # Todavía hay chances de que el dato se encuentre en otro lado
        pass
    
    try:
        span = find_span_nombre_empresa(card)
        return span.text.strip()
    except Exception as e:
        # En caso de fallar, elevar la excepcion
        raise e

def get_seat_type(seat_type_button):
    seat_type_element = find_seat_type_element(seat_type_button)
    return seat_type_element.text.strip()

def get_price(seat_type_button):
    price_element = find_price_element(seat_type_button)
    raw_price = price_element.text.strip()
    clean_price = limpiar_precio(raw_price)
    return clean_price

# --- Chequeos ---
def colectivos_no_disponibles(text):
    # Revisar si no hay colectivos
    mensajes_no_disponible = [
        "Por el momento no contamos con servicios disponibles para esta ruta.",
        "Tramo no disponible",
    ]

    return any(msg in text for msg in mensajes_no_disponible)

def fecha_no_disponible(text):
    mensajes_fecha_no_disponible = [
        "No disponemos de servicios para la fecha indicada, para más alternativas, te sugerimos buscar en fechas anteriores o posteriores."
    ]

    return any(msg in text for msg in mensajes_fecha_no_disponible)
