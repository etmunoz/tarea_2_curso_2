# --8<-- encabezado-grupo
# Archivo: src/agente_administrador/herramientas.py
# Objetivo: Herramientas del agente administrador: conoce el catálogo de agentes (lee fichas).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1508
# Última modificación: 20261117 1508
# --8<-- fin-encabezado-grupo

"""Herramientas del agente administrador: listar_agentes y describir_agente, leyendo src/fichas.py.

La fuente de verdad son las fichas (name + description) de los demás agentes; el administrador no
inventa capacidades. Se excluye a sí mismo del catálogo que entrega.
"""
from __future__ import annotations

from langchain_core.tools import tool

from src.fichas import FICHAS

_YO = "agente_administrador"


def _otros() -> dict[str, dict[str, str]]:
    """Objetivo: fichas de los demás agentes (sin el administrador)."""
    return {gid: f for gid, f in FICHAS.items() if gid != _YO}


@tool
def listar_agentes() -> list[dict]:
    """Lista todos los agentes disponibles con su nombre y una línea de qué hace cada uno.

    Úsala para responder "¿qué agentes hay?", "¿qué pueden hacer?" o para dar la bienvenida.
    """
    return [
        {"agente": gid, "nombre": f["name"], "descripcion": f["description"]}
        for gid, f in _otros().items()
    ]


@tool
def describir_agente(nombre: str) -> dict:
    """Describe UN agente por su identificador (p. ej. 'agente_reiki') o por su nombre.

    Devuelve qué hace, qué no hace y cuándo conviene. Si no existe, lo dice y lista los disponibles.
    """
    consulta = (nombre or "").strip().lower()
    for gid, f in _otros().items():
        if consulta and (consulta == gid.lower() or consulta in f["name"].lower()):
            return {"agente": gid, "nombre": f["name"], "descripcion": f["description"]}
    return {"error": f"No conozco un agente llamado '{nombre}'.", "disponibles": list(_otros().keys())}


HERRAMIENTAS = [listar_agentes, describir_agente]
