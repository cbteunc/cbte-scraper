import requests
import json
import time
import pandas as pd
import logging
import logging.config

logging.config.fileConfig('logging_config/logging.conf')
logger = logging.getLogger('root')

# -------------------------
# CONFIG
# -------------------------
base_search = "https://clasificados.lavoz.com.ar/api/search?page={}&filters=tid%3A6330+tid%3A6334+tid%3A3173+tid_location_should%3A3194+ss_operacion%3AAlquileres+ss_tipo_unidad_dpto%3ADepartamento+ss_cantidad_dormitorios%3A%221+Dormitorio%22"
base_ad = "https://clasificados.lavoz.com.ar/api/ad/{}"

# -------------------------
# 1. OBTENER LAST PAGE
# -------------------------
first = requests.get(base_search.format(1))
first.raise_for_status()
first_data = first.json()

last_page = first_data["data"]["results"]["meta"]["last_page"]
logger.info("Total páginas:", last_page)

# -------------------------
# 2. OBTENER TODOS LOS IDS
# -------------------------
all_ids = []

for page in range(1, last_page):
    logger.info("Descargando página:", page)

    r = requests.get(base_search.format(page))
    r.raise_for_status()
    data = r.json()

    items = data["data"]["results"]["data"]
    ids = [item["id"] for item in items]

    all_ids.extend(ids)

logger.info("Total IDs:", len(all_ids))

# -------------------------
# 3. DESCARGAR TODOS LOS ADS
# -------------------------
all_ads = []

for ad_id in all_ids:
    logger.info("Descargando:", ad_id)

    r = requests.get(base_ad.format(ad_id))
    r.raise_for_status()

    ad = r.json()
    all_ads.append(ad)

    time.sleep(5) 

# -------------------------
# 4. GUARDAR JSON COMPLETO
# -------------------------
with open("ads_completos.json", "w", encoding="utf-8") as f:
    json.dump(all_ads, f, ensure_ascii=False, indent=4)

logger.info("JSON completo guardado")

# -------------------------
# 5. CONVERTIR A EXCEL
# -------------------------
rows = []

for ad in all_ads:
    data = ad.get("data", {})

    rows.append({
        "id": data.get("id"),
        "precio": data.get("price", {}).get("amount"),
        "moneda": data.get("price", {}).get("currency"),
        "expensas": data.get("price", {}).get("expenses"),
        "barrio": data.get("address", {}).get("neighborhood"),
    })

df = pd.DataFrame(rows)

df.to_excel("ads.xlsx", index=False)

logger.info("Excel generado: ads.xlsx")