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

from datetime import datetime
from zoneinfo import ZoneInfo

from langchain_core.tools import tool

from src.fichas import FICHAS

_YO = "agente_administrador"
_TZ = ZoneInfo("America/Santiago")


def _franja(hora: int) -> str:
    """Objetivo: franja de saludo según la hora (0-23) en Santiago de Chile."""
    if 5 <= hora < 12:
        return "buenos días"
    if 12 <= hora < 20:
        return "buenas tardes"
    return "buenas noches"


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


@tool
def saludo_hora() -> dict:
    """Saludo según la hora actual de Santiago de Chile. Úsalo al saludar o dar la bienvenida.
    Devuelve {saludo: 'buenos días'|'buenas tardes'|'buenas noches', hora: 'HH:MM', fecha}."""
    ahora = datetime.now(_TZ)
    return {"saludo": _franja(ahora.hour), "hora": ahora.strftime("%H:%M"),
            "fecha": ahora.strftime("%d-%m-%Y")}


@tool
def nombre_usuario(usuario: str) -> dict:
    """Devuelve el nombre preferido guardado del usuario (pasa el login que viene en el contexto del
    sistema, p. ej. 'ezequiel'). Si no hay nombre guardado, devuelve nombre=None para que lo preguntes."""
    from src.memoria import bd  # import tardío
    n = bd.obtener_nombre(usuario)
    return {"usuario": usuario, "nombre": n} if n else {"usuario": usuario, "nombre": None,
                                                        "nota": "sin nombre guardado; pregúntaselo"}


@tool
def recordar_nombre(usuario: str, nombre: str) -> dict:
    """Guarda el nombre preferido del usuario para futuras conversaciones (memoria durable). Pasa el
    login que viene en el contexto del sistema como `usuario` y el nombre que dio la persona."""
    from src.memoria import bd  # import tardío
    bd.guardar_nombre(usuario, nombre)
    return {"ok": True, "usuario": usuario, "nombre": nombre.strip()}


HERRAMIENTAS = [listar_agentes, describir_agente, saludo_hora, nombre_usuario, recordar_nombre]
