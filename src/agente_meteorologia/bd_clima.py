# --8<-- encabezado-grupo
# Archivo: src/agente_meteorologia/bd_clima.py
# Objetivo: Persistencia SQLite del clima: pronósticos diarios y observados reales (para comparar).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1534
# Última modificación: 20261117 1534
# --8<-- fin-encabezado-grupo

"""Persistencia en SQLite (stdlib) de pronósticos diarios y observados reales del clima.

Dos tablas: `pronosticos` (snapshot por ciudad, fecha de emisión y fecha pronosticada) y `observados`
(valor real por ciudad y fecha). La ruta del archivo se toma de la variable de entorno CLIMA_DB; por
defecto `<repo>/logs/clima.sqlite` (ruta relativa al propio módulo, sin rutas absolutas incrustadas).
"""
from __future__ import annotations

import os
import sqlite3

_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.environ.get("CLIMA_DB", os.path.join(_RAIZ, "logs", "clima.sqlite"))

DDL = """
CREATE TABLE IF NOT EXISTS pronosticos (
  ciudad TEXT NOT NULL, fecha_emision TEXT NOT NULL, fecha_pronosticada TEXT NOT NULL,
  min_c REAL, max_c REAL, precip_mm REAL, codigo INTEGER, condicion TEXT,
  PRIMARY KEY (ciudad, fecha_emision, fecha_pronosticada)
);
CREATE TABLE IF NOT EXISTS observados (
  ciudad TEXT NOT NULL, fecha TEXT NOT NULL,
  min_c REAL, max_c REAL, precip_mm REAL, codigo INTEGER, condicion TEXT,
  PRIMARY KEY (ciudad, fecha)
);
"""


def _conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    c = sqlite3.connect(DB)
    c.executescript(DDL)
    return c


def guardar_pronostico(ciudad: str, fecha_emision: str, dias: list[dict]) -> int:
    """Objetivo: guardar/actualizar el snapshot de pronóstico de una ciudad. Salida: filas escritas."""
    with _conn() as c:
        n = 0
        for d in dias:
            c.execute(
                "INSERT OR REPLACE INTO pronosticos VALUES (?,?,?,?,?,?,?,?)",
                (ciudad, fecha_emision, d["fecha"], d.get("min_c"), d.get("max_c"),
                 d.get("precip_mm"), d.get("codigo"), d.get("condicion")),
            )
            n += 1
        return n


def guardar_observado(ciudad: str, obs: dict) -> None:
    """Objetivo: guardar/actualizar el valor observado real de una ciudad en una fecha."""
    with _conn() as c:
        c.execute(
            "INSERT OR REPLACE INTO observados VALUES (?,?,?,?,?,?,?)",
            (ciudad, obs["fecha"], obs.get("min_c"), obs.get("max_c"),
             obs.get("precip_mm"), obs.get("codigo"), obs.get("condicion")),
        )


def pronostico_guardado(ciudad: str, fecha: str):
    """Objetivo: el pronóstico más reciente EMITIDO para esa fecha. Salida: (emision,min,max,precip,condicion) o None."""
    with _conn() as c:
        return c.execute(
            "SELECT fecha_emision, min_c, max_c, precip_mm, condicion FROM pronosticos "
            "WHERE ciudad=? AND fecha_pronosticada=? ORDER BY fecha_emision DESC LIMIT 1",
            (ciudad, fecha),
        ).fetchone()


def observado_guardado(ciudad: str, fecha: str):
    """Objetivo: el observado real guardado. Salida: (min,max,precip,condicion) o None."""
    with _conn() as c:
        return c.execute(
            "SELECT min_c, max_c, precip_mm, condicion FROM observados WHERE ciudad=? AND fecha=?",
            (ciudad, fecha),
        ).fetchone()
