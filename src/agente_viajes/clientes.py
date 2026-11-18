# --8<-- encabezado-grupo
# Archivo: src/agente_viajes/clientes.py
# Objetivo: Clientes REALES sin API key para el agente de viajes (geocoding, país, cambio, Wikipedia).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261118 1240
# Última modificación: 20261118 1240
# --8<-- fin-encabezado-grupo

"""Clientes de datos de viaje con APIs públicas SIN API key (stdlib urllib).

- `geocodificar(ciudad)` -> ubicación (Open-Meteo Geocoding, en vivo).
- `pais_info(cc)` -> capital/moneda/idiomas desde una tabla de referencia incluida (ISO país→moneda;
  restcountries quedó deprecado). El país, la zona horaria y las coordenadas vienen en vivo del geocoding.
- `convertir(monto, desde, hacia)` y `clp_por_unidad(moneda)` -> cambio real (open.er-api.com).
- `resumen(titulo)` -> resumen de Wikipedia (REST summary en español).
El acceso a red (`_get`) está aislado para poder testear el parseo con JSON de ejemplo.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"
FX = "https://open.er-api.com/v6/latest"
WIKI = "https://es.wikipedia.org/api/rest_v1/page/summary"


def _get(url: str, params: dict | None = None) -> dict:
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "t2c2-viajes"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def geocodificar(ciudad: str) -> dict | None:
    """Objetivo: ubicar una ciudad. Salida: {nombre, pais, cc, lat, lon, timezone, poblacion, region}."""
    d = _get(GEOCODING, {"name": ciudad, "count": 1, "language": "es", "format": "json"})
    res = d.get("results") or []
    if not res:
        return None
    r = res[0]
    return {"nombre": r.get("name"), "pais": r.get("country"), "cc": r.get("country_code"),
            "lat": r.get("latitude"), "lon": r.get("longitude"), "timezone": r.get("timezone"),
            "poblacion": r.get("population"), "region": r.get("admin1")}


# Tabla de referencia (ISO-3166-1 alfa-2 → capital, moneda ISO-4217, idiomas). Datos de referencia
# canónicos incluidos (como la tabla WMO del clima); restcountries quedó deprecado.
PAISES: dict[str, dict] = {
    "CL": {"capital": "Santiago", "moneda": "CLP", "idiomas": ["español"]},
    "PE": {"capital": "Lima", "moneda": "PEN", "idiomas": ["español", "quechua", "aimara"]},
    "BO": {"capital": "Sucre", "moneda": "BOB", "idiomas": ["español", "quechua", "aimara"]},
    "AR": {"capital": "Buenos Aires", "moneda": "ARS", "idiomas": ["español"]},
    "BR": {"capital": "Brasilia", "moneda": "BRL", "idiomas": ["portugués"]},
    "CO": {"capital": "Bogotá", "moneda": "COP", "idiomas": ["español"]},
    "EC": {"capital": "Quito", "moneda": "USD", "idiomas": ["español"]},
    "VE": {"capital": "Caracas", "moneda": "VES", "idiomas": ["español"]},
    "UY": {"capital": "Montevideo", "moneda": "UYU", "idiomas": ["español"]},
    "PY": {"capital": "Asunción", "moneda": "PYG", "idiomas": ["español", "guaraní"]},
    "MX": {"capital": "Ciudad de México", "moneda": "MXN", "idiomas": ["español"]},
    "CR": {"capital": "San José", "moneda": "CRC", "idiomas": ["español"]},
    "PA": {"capital": "Panamá", "moneda": "USD", "idiomas": ["español"]},
    "GT": {"capital": "Ciudad de Guatemala", "moneda": "GTQ", "idiomas": ["español"]},
    "DO": {"capital": "Santo Domingo", "moneda": "DOP", "idiomas": ["español"]},
    "CU": {"capital": "La Habana", "moneda": "CUP", "idiomas": ["español"]},
    "US": {"capital": "Washington D. C.", "moneda": "USD", "idiomas": ["inglés"]},
    "CA": {"capital": "Ottawa", "moneda": "CAD", "idiomas": ["inglés", "francés"]},
    "ES": {"capital": "Madrid", "moneda": "EUR", "idiomas": ["español"]},
    "FR": {"capital": "París", "moneda": "EUR", "idiomas": ["francés"]},
    "GB": {"capital": "Londres", "moneda": "GBP", "idiomas": ["inglés"]},
    "DE": {"capital": "Berlín", "moneda": "EUR", "idiomas": ["alemán"]},
    "IT": {"capital": "Roma", "moneda": "EUR", "idiomas": ["italiano"]},
    "PT": {"capital": "Lisboa", "moneda": "EUR", "idiomas": ["portugués"]},
    "NL": {"capital": "Ámsterdam", "moneda": "EUR", "idiomas": ["neerlandés"]},
    "CH": {"capital": "Berna", "moneda": "CHF", "idiomas": ["alemán", "francés", "italiano"]},
    "JP": {"capital": "Tokio", "moneda": "JPY", "idiomas": ["japonés"]},
    "CN": {"capital": "Pekín", "moneda": "CNY", "idiomas": ["chino mandarín"]},
    "KR": {"capital": "Seúl", "moneda": "KRW", "idiomas": ["coreano"]},
    "AU": {"capital": "Canberra", "moneda": "AUD", "idiomas": ["inglés"]},
}


def pais_info(cc: str) -> dict | None:
    """Objetivo: capital/moneda/idiomas de un país por su código ISO-2 (tabla de referencia incluida).
    Salida: {capital, moneda_codigo, idiomas} o None si el país no está en la tabla."""
    p = PAISES.get((cc or "").upper())
    if not p:
        return None
    return {"capital": p["capital"], "moneda_codigo": p["moneda"], "idiomas": p["idiomas"]}


def clp_por_unidad(moneda: str) -> float | None:
    """Objetivo: cuántos CLP equivale 1 unidad de `moneda` (p. ej. 1 USD = ? CLP)."""
    d = _get(f"{FX}/{moneda.upper()}")
    if d.get("result") != "success":
        return None
    return d.get("rates", {}).get("CLP")


def convertir(monto: float, desde: str, hacia: str) -> dict | None:
    """Objetivo: convertir `monto` de la moneda `desde` a la moneda `hacia` con tasa real.
    Salida: {monto, desde, hacia, tasa, resultado} o None."""
    d = _get(f"{FX}/{desde.upper()}")
    if d.get("result") != "success":
        return None
    tasa = d.get("rates", {}).get(hacia.upper())
    if tasa is None:
        return None
    return {"monto": monto, "desde": desde.upper(), "hacia": hacia.upper(),
            "tasa": tasa, "resultado": round(monto * tasa, 2)}


def resumen(titulo: str) -> dict | None:
    """Objetivo: resumen de Wikipedia (español) de un lugar. Salida: {titulo, resumen, url} o None."""
    t = urllib.parse.quote(titulo.strip().replace(" ", "_"))
    try:
        d = _get(f"{WIKI}/{t}")
    except urllib.error.HTTPError:
        return None
    if d.get("type", "").endswith("not_found") or not d.get("extract"):
        return None
    return {"titulo": d.get("title", titulo), "resumen": d.get("extract", ""),
            "url": d.get("content_urls", {}).get("desktop", {}).get("page", "")}
