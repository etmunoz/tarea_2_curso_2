# --8<-- encabezado-grupo
# Archivo: src/agente_meteorologia/herramientas.py
# Objetivo: Herramientas del Agente de Meteorología: clima REAL (Open-Meteo) + historial/comparación (SQLite).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1534
# Última modificación: 20261117 1534
# --8<-- fin-encabezado-grupo

"""Herramientas del Agente de Meteorología.

La lógica real vive en módulos de stdlib (`ciudades`, `openmeteo`, `bd_clima`); aquí solo se envuelven
con @tool. `pronostico_hoy`/`pronostico_semana` consultan Open-Meteo y guardan el snapshot del día en
SQLite; `historial_pronostico` lee lo guardado; `comparar_pronostico_vs_real` cruza pronóstico y
observado real.
"""
from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from langchain_core.tools import tool

from src.agente_meteorologia import bd_clima, ciudades, openmeteo


def _hoy_santiago() -> str:
    return datetime.now(ZoneInfo("America/Santiago")).date().isoformat()


@tool
def pronostico_hoy(ciudad: str) -> dict | str:
    """Clima REAL de HOY para una ciudad de Chile: temperatura actual, mínima/máxima, condición y
    precipitación (Open-Meteo). Guarda además el pronóstico de la semana en el historial (SQLite)."""
    cc = ciudades.coords(ciudad)
    if not cc:
        return f"No tengo coordenadas para '{ciudad}'. Ciudades disponibles: {ciudades.listado()}."
    try:
        p = openmeteo.pronostico(cc[0], cc[1], dias=7)
    except Exception as e:  # noqa: BLE001
        return f"No pude consultar el clima de {ciudad} ahora ({type(e).__name__}). Intenta más tarde."
    try:
        bd_clima.guardar_pronostico(ciudades.normalizar(ciudad), _hoy_santiago(), p["dias"])
    except Exception:  # noqa: BLE001
        pass
    hoy = p["dias"][0]
    return {"ciudad": ciudad, "fecha": hoy["fecha"], "temperatura_actual_c": p["actual"]["temp_c"],
            "min_c": hoy["min_c"], "max_c": hoy["max_c"], "precip_mm": hoy["precip_mm"],
            "condicion": hoy["condicion"]}


@tool
def pronostico_semana(ciudad: str) -> dict | str:
    """Clima REAL de los próximos 7 días para una ciudad de Chile (Open-Meteo). Guarda el pronóstico en
    el historial (SQLite) para poder consultarlo y compararlo después."""
    cc = ciudades.coords(ciudad)
    if not cc:
        return f"No tengo coordenadas para '{ciudad}'. Ciudades disponibles: {ciudades.listado()}."
    try:
        p = openmeteo.pronostico(cc[0], cc[1], dias=7)
    except Exception as e:  # noqa: BLE001
        return f"No pude consultar el clima de {ciudad} ahora ({type(e).__name__}). Intenta más tarde."
    emision = _hoy_santiago()
    try:
        bd_clima.guardar_pronostico(ciudades.normalizar(ciudad), emision, p["dias"])
    except Exception:  # noqa: BLE001
        pass
    return {"ciudad": ciudad, "emitido": emision, "dias": p["dias"]}


@tool
def historial_pronostico(ciudad: str, fecha: str) -> dict | str:
    """Lo que se PRONOSTICÓ (y quedó guardado) para una fecha dada (YYYY-MM-DD) en una ciudad de Chile."""
    row = bd_clima.pronostico_guardado(ciudades.normalizar(ciudad), fecha)
    if not row:
        return f"No tengo pronóstico guardado para {ciudad} en {fecha}."
    return {"ciudad": ciudad, "fecha": fecha, "emitido": row[0], "min_c": row[1], "max_c": row[2],
            "precip_mm": row[3], "condicion": row[4]}


@tool
def comparar_pronostico_vs_real(ciudad: str, fecha: str) -> dict | str:
    """Compara, para una fecha pasada (YYYY-MM-DD) en una ciudad de Chile, lo PRONOSTICADO (guardado)
    con lo REALMENTE OBSERVADO (Open-Meteo archive), con la diferencia de temperaturas."""
    cc = ciudades.coords(ciudad)
    if not cc:
        return f"No tengo coordenadas para '{ciudad}'. Ciudades disponibles: {ciudades.listado()}."
    norm = ciudades.normalizar(ciudad)
    pron = bd_clima.pronostico_guardado(norm, fecha)
    obs = bd_clima.observado_guardado(norm, fecha)
    if not obs:
        try:
            o = openmeteo.observado(cc[0], cc[1], fecha)
        except Exception:  # noqa: BLE001
            o = None
        if o and o.get("max_c") is not None:
            bd_clima.guardar_observado(norm, o)
            obs = (o["min_c"], o["max_c"], o["precip_mm"], o["condicion"])
    if not pron and not obs:
        return f"No tengo ni pronóstico guardado ni observado para {ciudad} en {fecha}."
    salida: dict = {"ciudad": ciudad, "fecha": fecha}
    if pron:
        salida["pronosticado"] = {"min_c": pron[1], "max_c": pron[2], "condicion": pron[4]}
    if obs:
        salida["observado"] = {"min_c": obs[0], "max_c": obs[1], "condicion": obs[3]}
    if pron and obs and pron[2] is not None and obs[1] is not None:
        salida["diferencia_max_c"] = round(obs[1] - pron[2], 1)
        if pron[1] is not None and obs[0] is not None:
            salida["diferencia_min_c"] = round(obs[0] - pron[1], 1)
    return salida


HERRAMIENTAS = [pronostico_hoy, pronostico_semana, historial_pronostico, comparar_pronostico_vs_real]
