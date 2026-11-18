# --8<-- encabezado-grupo
# Archivo: src/config/ajustes.py
# Objetivo: Almacén de ajustes en SQLite (clave/valor) para configurar secretos por la web (p. ej. GOOGLE_API_KEY).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1845
# Última modificación: 20261117 1845
# --8<-- fin-encabezado-grupo

"""Almacén de ajustes (clave/valor) en SQLite, como alternativa al .env para ciertos secretos.

Solo se admiten claves de una allowlist (PERMITIDAS). El `.env`/EnvironmentFile SIEMPRE tiene prioridad
(ver src/config/bootstrap.py): esto es un ingreso alternativo, no un reemplazo. Ruta por env CONFIG_DB
(def. <repo>/logs/config.sqlite).
"""
from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.environ.get("CONFIG_DB", os.path.join(_RAIZ, "logs", "config.sqlite"))
_TZ = ZoneInfo("America/Santiago")

PERMITIDAS = ("GOOGLE_API_KEY", "API_KEY", "SMTP_PASS")
DDL = "CREATE TABLE IF NOT EXISTS config (clave TEXT PRIMARY KEY, valor TEXT, ts TEXT);"


def _conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    c = sqlite3.connect(DB)
    c.executescript(DDL)
    return c


def set(clave: str, valor: str) -> bool:
    """Objetivo: guardar un ajuste permitido. Salida: True si se guardó."""
    if clave not in PERMITIDAS or not valor:
        return False
    with _conn() as c:
        c.execute("INSERT OR REPLACE INTO config (clave, valor, ts) VALUES (?,?,?)",
                  (clave, valor, datetime.now(_TZ).isoformat(timespec="seconds")))
    return True


def get(clave: str, default=None):
    """Objetivo: leer un ajuste. Salida: su valor o default."""
    with _conn() as c:
        r = c.execute("SELECT valor FROM config WHERE clave=?", (clave,)).fetchone()
    return r[0] if r else default


def todos() -> dict:
    """Objetivo: todos los ajustes (para el bootstrap)."""
    with _conn() as c:
        return {k: v for k, v in c.execute("SELECT clave, valor FROM config").fetchall()}


def estados() -> dict:
    """Objetivo: por cada clave permitida, si está definida (True/False) — sin exponer el valor."""
    t = todos()
    return {k: bool(t.get(k)) for k in PERMITIDAS}
