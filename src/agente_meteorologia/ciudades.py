# --8<-- encabezado-grupo
# Archivo: src/agente_meteorologia/ciudades.py
# Objetivo: Catálogo de ciudades de Chile con coordenadas (lat, lon) y normalización de nombres.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1534
# Última modificación: 20261117 1534
# --8<-- fin-encabezado-grupo

"""Catálogo de ciudades de Chile (lat, lon) y utilidades de normalización de nombres (sin tildes)."""
from __future__ import annotations

import unicodedata

CIUDADES: dict[str, tuple[float, float]] = {
    "arica": (-18.4783, -70.3126),
    "iquique": (-20.2307, -70.1357),
    "antofagasta": (-23.6509, -70.3975),
    "calama": (-22.4544, -68.9294),
    "copiapo": (-27.3668, -70.3314),
    "la serena": (-29.9027, -71.2519),
    "valparaiso": (-33.0472, -71.6127),
    "santiago": (-33.4489, -70.6693),
    "rancagua": (-34.1708, -70.7444),
    "talca": (-35.4264, -71.6554),
    "chillan": (-36.6066, -72.1034),
    "concepcion": (-36.8201, -73.0444),
    "temuco": (-38.7359, -72.5904),
    "valdivia": (-39.8142, -73.2459),
    "osorno": (-40.5725, -73.1353),
    "puerto montt": (-41.4693, -72.9424),
    "coyhaique": (-45.5712, -72.0685),
    "punta arenas": (-53.1638, -70.9171),
}


def normalizar(ciudad: str) -> str:
    """Objetivo: pasar un nombre de ciudad a su clave canónica (minúsculas, sin tildes, sin espacios extra)."""
    t = unicodedata.normalize("NFKD", (ciudad or "").strip().lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def coords(ciudad: str) -> tuple[float, float] | None:
    """Objetivo: coordenadas (lat, lon) de una ciudad de Chile, o None si no está en el catálogo."""
    return CIUDADES.get(normalizar(ciudad))


def listado() -> str:
    """Objetivo: nombres de las ciudades disponibles, legibles, en una cadena."""
    return ", ".join(n.title() for n in CIUDADES)
