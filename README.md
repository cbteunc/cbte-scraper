## Canasta Básica Total Estudiantil
### Elaborado por y para estudiantes

## Ejecución del scraping

1. Descargar código
   
> Andá al repositorio en GitHub. 
>Hacé clic en el botón verde que dice Code.
>Elegí la opción "Download ZIP".
>Descomprimí el archivo ZIP en tu computadora. O directamente podés hacer `git clone`. 

2. Ejecutar las siguientes lineas en Windows Powershell o la terminal que sea
> ir a la carpeta CBTE con el comando cd. Ejemplo: cd ./Descargas/CBTE
> `python -m venv venv` -> `./venv/Scripts/activate` -> `pip install -r requirements.txt` -> `python scripts/supermercados/supermercados_vea/main.py`, por ejemplo. Si tu compu es buena, `python scripts/run_all.py`

## Ejecución de tests

Para ejecutar tests, simplemente:

1. Modificar en el archivo `scripts/run_tests.py` la lista de test que se quieren ejecutar
2. En la terminal, estando en la carpeta raíz del proyecto (CBTE), usar `python3 run_tests.py`

## Configuración de credenciales

Este proyecto utiliza la API de Google Drive para subir la carpeta data a la carpeta de drive del proyecto. 

**⚠️ Si no lo querés usar y querés correr todo de una, tenés que comentar la linea que lo ejecuta en el archivo `run_all.py` en la carpeta `scripts`. Tiene que quedar así:**

```
# Lista de paths a cada main.py
scripts = [
    "alquileres/alquileres_argenprop/main.py",
    "alquileres/alquileres_lavoz/main.py",
    "libreria/libreria_ferniplast/main.py",
    "libreria/libreria_grafitti/main.py",
    "libreria/libreria_pencilbag/main.py",
    "supermercados/supermercados_carrefour/main.py",
    "supermercados/supermercados_cordiez/main.py",  
    "supermercados/supermercados_disco/main.py",
    "supermercados/supermercados_vea/main.py",
    "internet/main.py",
    "telefonia/main.py"
]
```

Para poder usarlo, tenés que

1. Ir a [Drive Sync](https://expertbeacon.com/how-to-upload-files-to-google-drive-with-python-in-2023/#google_vignette)
2. Seguir los pasos 1 y 2