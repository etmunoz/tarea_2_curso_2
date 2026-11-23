# --8<-- encabezado-grupo
# Archivo: src/agente_meteo_mcp/herramientas.py
# Objetivo: Herramientas LangChain del agente meteo_mcp sobre Meteosource MCP.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261122 0000
# Última modificación: 20261122 0000
# --8<-- fin-encabezado-grupo

"""Herramientas del agente meteo_mcp.

Estas funciones no implementan un cliente MCP. Reutilizan exclusivamente
``ClienteMCP`` y fuerzan el descubrimiento de tools con ``list_tools()``
antes de cada ejecución.
"""
from __future__ import annotations

from typing import Any

from langchain_core.tools import tool

from src.integraciones.mcp_langchain import ClienteMCP


def _solo_place_id(locations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Evita enviar latitud/longitud junto con place_id al servidor MCP."""
    normalizadas = []
    for ubicacion in locations:
        if ubicacion.get("place_id"):
            item = {"place_id": str(ubicacion["place_id"])}
            if ubicacion.get("label"):
                item["label"] = str(ubicacion["label"])
            normalizadas.append(item)
        else:
            normalizadas.append(ubicacion)
    return normalizadas


async def _ejecutar_tool(nombre: str, argumentos: dict[str, Any]) -> str:
    """Descubre las tools disponibles y ejecuta sólo la solicitada."""
    try:
        async with ClienteMCP.conectar_meteosource() as cliente:
            herramientas = await cliente.listar_herramientas()
            disponibles = {
                str(getattr(herramienta, "name", "")) for herramienta in herramientas
            }
            if nombre not in disponibles:
                return f"La herramienta meteorológica «{nombre}» no está disponible."
            return await cliente.ejecutar(nombre, argumentos)
    except Exception as error:  # noqa: BLE001
        return f"No pude consultar el servidor meteorológico ({type(error).__name__})."


@tool("search_places")
async def search_places(ciudad: str) -> str:
    """Busca una ciudad o localidad y devuelve sus coincidencias y place_id."""
    return await _ejecutar_tool(
        "search_places",
        {"query": ciudad, "language": "es"},
    )


@tool("get_forecast")
async def get_forecast(
    locations: list[dict[str, Any]],
    sections: str = "current,daily",
    days: int = 3,
    timezone: str = "auto",
    units: str = "metric",
    language: str = "es",
) -> str:
    """Obtiene el pronóstico usando locations con place_id encontrados previamente."""
    return await _ejecutar_tool(
        "get_forecast",
        {
            "locations": _solo_place_id(locations),
            "sections": sections,
            "days": days,
            "timezone": timezone,
            "units": units,
            "language": language,
        },
    )


@tool("get_weather_history")
async def get_weather_history(
    locations: list[dict[str, Any]],
    date_from: str,
    date_to: str,
    granularity: str = "daily",
    variables: list[str] | None = None,
    normals: bool = False,
    timezone: str = "auto",
    units: str = "metric",
) -> str:
    """Obtiene datos meteorológicos históricos usando locations con place_id."""
    return await _ejecutar_tool(
        "get_weather_history",
        {
            "locations": _solo_place_id(locations),
            "date_from": date_from,
            "date_to": date_to,
            "granularity": granularity,
            "variables": variables,
            "normals": normals,
            "timezone": timezone,
            "units": units,
        },
    )


HERRAMIENTAS = [search_places, get_forecast, get_weather_history]
