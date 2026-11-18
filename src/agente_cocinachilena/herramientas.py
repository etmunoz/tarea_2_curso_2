# --8<-- encabezado-grupo
# Archivo: src/agente_cocinachilena/herramientas.py
# Objetivo: Herramientas del agente de cocina chilena (recetas + costeo desde SQLite).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261110 2013
# Última modificación: 20261111 2049
# --8<-- fin-encabezado-grupo

"""Herramientas del agente de cocina chilena (recetas + costeo desde SQLite)."""
from __future__ import annotations

from langchain_core.tools import tool

from src.agente_cocinachilena import bd_recetas


@tool
def listar_recetas() -> list[dict]:
    """Lista las recetas chilenas disponibles (nombre, porciones base y descripción)."""
    return bd_recetas.listar_recetas()


@tool
def ver_receta(nombre: str) -> dict:
    """Muestra una receta: sus ingredientes con cantidad y unidad. Acepta nombre parcial."""
    return bd_recetas.ver_receta(nombre)


@tool
def costear_receta(nombre: str, personas: int = 4) -> dict:
    """Calcula cuánto cuesta producir una receta para `personas` (por defecto 4).
    Devuelve el costo por ingrediente (cantidad escalada × precio por su unidad, sin
    conversión), el costo total y el costo por persona, todo en CLP."""
    return bd_recetas.costear_receta(nombre, personas=personas)


@tool
def recomendar_recetas(restriccion: str, personas: int = 4) -> dict:
    """Recomienda recetas chilenas según una restricción alimentaria o de presupuesto:
    'vegetariano', 'vegano', 'sin gluten' o 'economica' (costo por persona bajo). La clasificación
    se deriva de los ingredientes de cada receta. Devuelve {restriccion, recetas:[{receta,
    por_persona_clp}]} ordenadas por costo, o una nota con las restricciones válidas."""
    return bd_recetas.recetas_por_restriccion(restriccion, personas=personas)


@tool
def info_nutricional(nombre: str, personas: int = 4) -> dict:
    """Estimación nutricional APROXIMADA (kcal total y por persona) de una receta para `personas`.
    Es una estimación a partir de valores tipo por ingrediente, NO asesoría nutricional. Devuelve
    {receta, personas, kcal_total_aprox, kcal_por_persona_aprox, nota}."""
    return bd_recetas.info_nutricional(nombre, personas=personas)


HERRAMIENTAS = [listar_recetas, ver_receta, costear_receta, recomendar_recetas, info_nutricional]
