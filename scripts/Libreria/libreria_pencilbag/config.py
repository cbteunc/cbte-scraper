# Definir la URL base y las categorías
base_url = "https://pencilbaglibreria.com.ar/"

categorias_deseadas = ["escritura1/lapices-grafito/",
                        "escritura1/resaltadores1/",
                        "gomas/",
                        "escritura1/boligrafos/clasicos/",
                        "cuadernos1/"]
# Obtener los links de las categorías
links_categorias = [f"{base_url}{cat}" for cat in categorias_deseadas]
