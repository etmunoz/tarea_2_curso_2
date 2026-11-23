# --8<-- encabezado-grupo
# Archivo: scripts/descubre_mcp.py
# Objetivo: Descubrir y mostrar las herramientas expuestas por el MCP Meteosource.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261122 0000
# Última modificación: 20261122 0000
# --8<-- fin-encabezado-grupo

"""Descubre las tools de Meteosource mediante el adaptador MCP del proyecto."""
from __future__ import annotations

import asyncio
import json
import sys
import textwrap
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.integraciones.mcp_langchain import ClienteMCP  # noqa: E402


def _esquema_diccionario(esquema: Any) -> dict[str, Any]:
    """Normaliza el inputSchema MCP a un diccionario."""
    if isinstance(esquema, dict):
        return esquema
    if hasattr(esquema, "model_dump"):
        return esquema.model_dump(mode="json")
    return {}


def _primera_linea(descripcion: Any) -> str:
    """Obtiene sólo la primera línea de la descripción de una tool."""
    texto = str(descripcion or "").strip()
    return texto.splitlines()[0].strip() if texto else "Sin descripción"


def _tipo_argumento(esquema: dict[str, Any]) -> str:
    """Obtiene el tipo legible declarado en el esquema JSON."""
    tipo = esquema.get("type")
    if isinstance(tipo, list):
        tipo = " | ".join(str(valor) for valor in tipo)
    if tipo:
        return str(tipo)
    if "enum" in esquema:
        return "enum"
    if "properties" in esquema:
        return "object"
    return "any"


def _argumentos(tool: Any) -> list[str]:
    """Formatea los argumentos de una tool, uno por línea."""
    esquema_original = getattr(tool, "inputSchema", None)
    if esquema_original is None:
        esquema_original = getattr(tool, "input_schema", None)
    esquema = _esquema_diccionario(esquema_original)
    propiedades = esquema.get("properties") or {}
    obligatorios = set(esquema.get("required") or ())
    if not propiedades:
        return []

    salida = []
    for nombre in sorted(propiedades):
        definicion = propiedades[nombre]
        definicion = definicion if isinstance(definicion, dict) else {}
        marca = " (obligatorio)" if nombre in obligatorios else ""
        salida.append(f"{nombre}: {_tipo_argumento(definicion)}{marca}")
    return salida


def formatear_herramientas(herramientas: list[Any]) -> str:
    """Devuelve un informe legible en terminal, ordenado por nombre."""
    ordenadas = sorted(herramientas, key=lambda item: str(getattr(item, "name", "")).lower())
    lineas = [
        f"HERRAMIENTAS MCP METEOSOURCE ({len(ordenadas)})",
        "=" * 72,
    ]

    for indice, tool in enumerate(ordenadas, start=1):
        nombre = str(getattr(tool, "name", "sin_nombre"))
        descripcion = _primera_linea(getattr(tool, "description", ""))
        argumentos = _argumentos(tool)
        descripcion_envuelta = textwrap.wrap(
            descripcion,
            width=84,
            initial_indent="   Descripción: ",
            subsequent_indent="                ",
        )
        lineas.extend([f"{indice}. {nombre}", *descripcion_envuelta])
        if argumentos:
            lineas.append("   Argumentos:")
            lineas.extend(f"      • {argumento}" for argumento in argumentos)
        else:
            lineas.append("   Argumentos: ninguno")
        if indice != len(ordenadas):
            lineas.append("")

    return "\n".join(lineas)


def _decodificar_json(respuesta: str) -> Any:
    """Decodifica una respuesta JSON del servidor, si corresponde."""
    try:
        return json.loads(respuesta)
    except (TypeError, json.JSONDecodeError):
        return None


def _mostrar_respuesta(respuesta: str) -> str:
    """Formatea una respuesta MCP sin modificar su contenido."""
    datos = _decodificar_json(respuesta)
    if datos is not None:
        return json.dumps(datos, ensure_ascii=False, indent=2)
    return respuesta


def _primer_place_id(respuesta: str) -> str | None:
    """Obtiene el primer place_id de una respuesta search_places."""
    datos = _decodificar_json(respuesta)
    if not isinstance(datos, list) or not datos:
        return None
    primero = datos[0]
    return str(primero["place_id"]) if isinstance(primero, dict) and primero.get("place_id") else None


async def _pruebas_mcp(cliente: ClienteMCP) -> None:
    """Ejecuta búsquedas de ciudades y un pronóstico usando sus place_id."""
    ciudades = (
        ("Berlín, Alemania", "Berlin, Germany"),
        ("Santiago de Chile", "Santiago, Chile"),
    )
    lugares: list[dict[str, str]] = []

    print("\nPRUEBAS DE HERRAMIENTAS")
    print("=" * 72)
    for etiqueta, consulta in ciudades:
        respuesta = await cliente.ejecutar(
            "search_places",
            {"query": consulta, "language": "en"},
        )
        print(f"\nsearch_places — {etiqueta}")
        print(_mostrar_respuesta(respuesta))
        place_id = _primer_place_id(respuesta)
        if place_id:
            lugares.append({"place_id": place_id, "label": etiqueta})

    if len(lugares) != len(ciudades):
        print("\nNo se ejecutó get_forecast porque no se obtuvieron todos los place_id.")
        return

    respuesta = await cliente.ejecutar(
        "get_forecast",
        {
            "locations": lugares,
            "sections": "current,daily",
            "days": 2,
            "units": "metric",
            "timezone": "auto",
            "language": "en",
        },
    )
    print("\nget_forecast — Berlín y Santiago de Chile")
    print(_mostrar_respuesta(respuesta))


async def main() -> int:
    """Conecta al MCP, descubre sus tools y muestra la tabla."""
    try:
        async with ClienteMCP.conectar_meteosource() as cliente:
            herramientas = await cliente.listar_herramientas()
            if not herramientas:
                print("El servidor MCP respondió, pero no expone herramientas.")
                return 0
            print(formatear_herramientas(herramientas))
            await _pruebas_mcp(cliente)
    except Exception:  # noqa: BLE001
        print("No fue posible conectarse al servidor MCP Meteosource.")
        print("Verifica MCP_SERVER_METEOSOURCE, la autenticación y la disponibilidad del servidor.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
