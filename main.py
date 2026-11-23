# --8<-- encabezado-grupo
# Archivo: main.py
# Objetivo: CLI para ejecutar agentes locales, mostrar saltos o imprimir diagramas.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261122 0000
# Última modificación: 20261122 0000
# --8<-- fin-encabezado-grupo

"""Uso: python main.py meteo_mcp "pregunta" [--saltos|--diagrama]."""
from __future__ import annotations

import argparse
import asyncio
import uuid


def _argumentos() -> argparse.Namespace:
    """Procesa los argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("agente", choices=["meteo_mcp"])
    parser.add_argument("pregunta", nargs="?")
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument("--saltos", action="store_true")
    grupo.add_argument("--diagrama", action="store_true")
    return parser.parse_args()


async def _ejecutar(args: argparse.Namespace) -> None:
    from src.agente_meteo_mcp import graph
    from src.agente_meteo_mcp.graph import _limpiar_respuesta

    if args.diagrama:
        graph.diagrama()
        return
    if not args.pregunta:
        raise SystemExit("Debes indicar una pregunta, salvo cuando uses --diagrama.")
    if args.saltos:
        respuesta = await graph.saltos(args.pregunta)
    else:
        respuesta = await graph.responder(args.pregunta, f"terminal-{uuid.uuid4()}")
    # Última barrera: la CLI nunca debe mostrar metadatos técnicos del proveedor.
    print(_limpiar_respuesta(respuesta))


def main() -> None:
    """Punto de entrada de la CLI."""
    asyncio.run(_ejecutar(_argumentos()))


if __name__ == "__main__":
    main()
