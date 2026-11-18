# --8<-- encabezado-grupo
# Archivo: src/agente_meteorologia/openmeteo.py
# Objetivo: Cliente de Open-Meteo (gratis, sin API key): pronóstico y observado real, vía urllib (stdlib).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1534
# Última modificación: 20261117 1534
# --8<-- fin-encabezado-grupo

"""Cliente de Open-Meteo con la biblioteca estándar (sin dependencias ni API key).

- `pronostico(lat, lon, dias)` -> clima actual + pronóstico diario (mín/máx, precipitación, condición).
- `observado(lat, lon, fecha)` -> valores observados de una fecha pasada (API archive, ERA5).
Zona horaria fija America/Santiago; los códigos WMO se traducen a texto en español.
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
TZ = "America/Santiago"

WMO = {
    0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado", 3: "Nublado",
    45: "Niebla", 48: "Niebla con escarcha", 51: "Llovizna débil", 53: "Llovizna moderada",
    55: "Llovizna densa", 56: "Llovizna helada débil", 57: "Llovizna helada densa",
    61: "Lluvia débil", 63: "Lluvia moderada", 65: "Lluvia fuerte", 66: "Lluvia helada débil",
    67: "Lluvia helada fuerte", 71: "Nieve débil", 73: "Nieve moderada", 75: "Nieve fuerte",
    77: "Granos de nieve", 80: "Chubascos débiles", 81: "Chubascos moderados", 82: "Chubascos violentos",
    85: "Chubascos de nieve débiles", 86: "Chubascos de nieve fuertes", 95: "Tormenta",
    96: "Tormenta con granizo", 99: "Tormenta con granizo fuerte",
}


def condicion(codigo) -> str:
    """Objetivo: traducir un código WMO a texto en español."""
    if codigo is None:
        return "—"
    return WMO.get(int(codigo), f"Código {codigo}")


def _get(url: str, params: dict) -> dict:
    q = urllib.parse.urlencode(params)
    with urllib.request.urlopen(f"{url}?{q}", timeout=20) as r:
        return json.load(r)


def pronostico(lat: float, lon: float, dias: int = 7) -> dict:
    """Objetivo: clima actual + pronóstico diario para (lat, lon). Salida: {actual, dias:[...]}"""
    d = _get(FORECAST_URL, {
        "latitude": lat, "longitude": lon, "timezone": TZ, "forecast_days": dias,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
        "current_weather": "true",
    })
    diario = d.get("daily", {})
    dias_list = []
    for i, f in enumerate(diario.get("time", [])):
        cod = diario["weather_code"][i]
        dias_list.append({
            "fecha": f, "min_c": diario["temperature_2m_min"][i], "max_c": diario["temperature_2m_max"][i],
            "precip_mm": diario["precipitation_sum"][i], "codigo": cod, "condicion": condicion(cod),
        })
    cw = d.get("current_weather", {})
    return {
        "actual": {"temp_c": cw.get("temperature"), "codigo": cw.get("weathercode"),
                   "condicion": condicion(cw.get("weathercode"))},
        "dias": dias_list,
    }


def observado(lat: float, lon: float, fecha: str) -> dict | None:
    """Objetivo: valores observados reales de una fecha pasada (YYYY-MM-DD). None si no hay dato aún."""
    d = _get(ARCHIVE_URL, {
        "latitude": lat, "longitude": lon, "timezone": TZ, "start_date": fecha, "end_date": fecha,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
    })
    diario = d.get("daily", {})
    t = diario.get("time", [])
    if not t or diario.get("temperature_2m_max", [None])[0] is None:
        return None
    cod = diario["weather_code"][0]
    return {"fecha": t[0], "min_c": diario["temperature_2m_min"][0], "max_c": diario["temperature_2m_max"][0],
            "precip_mm": diario["precipitation_sum"][0], "codigo": cod, "condicion": condicion(cod)}
