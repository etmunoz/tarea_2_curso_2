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
def preferencias_usuario(usuario: str) -> dict:
    """Devuelve las preferencias guardadas del usuario (pasa el login que viene en el contexto del
    sistema, p. ej. 'ezequiel'): {nombre, idioma, saludo}. Un valor None significa que no está guardado
    (pregúntalo si corresponde). 'idioma' None ⇒ usa español por defecto."""
    from src.memoria import bd  # import tardío
    p = bd.obtener_perfil(usuario)
    return {"usuario": usuario, **p}


@tool
def recordar_preferencias(usuario: str, nombre: str = "", idioma: str = "", saludo: str = "") -> dict:
    """Guarda preferencias del usuario para futuras conversaciones (memoria durable). Pasa el login del
    contexto como `usuario` y SOLO los campos que quieras actualizar:
    - `nombre`: cómo prefiere que le digan.
    - `idioma`: idioma en que prefiere conversar (p. ej. 'español', 'inglés'). El sistema es en español
      por defecto; solo cámbialo si la persona lo pide o escribe claramente en otro idioma.
    - `saludo`: la forma de saludar que usa la persona (p. ej. 'wena', '¡buenas!', 'hey') para replicarla.
    Los campos vacíos no se modifican."""
    from src.memoria import bd  # import tardío
    bd.guardar_perfil(usuario, nombre=nombre, idioma=idioma, saludo=saludo)
    return {"ok": True, "usuario": usuario, **bd.obtener_perfil(usuario)}


HERRAMIENTAS = [listar_agentes, describir_agente, saludo_hora, preferencias_usuario, recordar_preferencias]
