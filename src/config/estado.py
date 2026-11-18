# --8<-- encabezado-grupo
# Archivo: src/config/estado.py
# Objetivo: Estado runtime de la clave Gemini (p. ej. cuota/tokens agotados) para avisar por la web.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1850
# Última modificación: 20261117 1850
# --8<-- fin-encabezado-grupo

"""Estado runtime de la clave Gemini: OK o 'cuota/tokens agotados', con marca de tiempo.

Lo escribe el gateway al invocar a los agentes; lo lee el monitor/web para avisar. Guarda en el mismo
SQLite de configuración (CONFIG_DB). `es_cuota(texto)` clasifica el error del proveedor.
"""
from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.environ.get("CONFIG_DB", os.path.join(_RAIZ, "logs", "config.sqlite"))
_TZ = ZoneInfo("America/Santiago")
DDL = "CREATE TABLE IF NOT EXISTS estado (clave TEXT PRIMARY KEY, ok INTEGER, detalle TEXT, ts TEXT);"

_PATRONES = ("quota", "resource_exhausted", "resourceexhausted", "429", "rate limit",
             "exceeded", "insufficient", "sin cuota")


def es_cuota(texto: str) -> bool:
    """Objetivo: True si el texto de error parece de cuota/tokens agotados."""
    t = (texto or "").lower()
    return any(p in t for p in _PATRONES)


def _conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    c = sqlite3.connect(DB)
    c.executescript(DDL)
    return c


def set_gemini(ok: bool, detalle: str = "") -> None:
    """Objetivo: registrar el estado de la clave Gemini."""
    with _conn() as c:
        c.execute("INSERT OR REPLACE INTO estado (clave, ok, detalle, ts) VALUES ('gemini',?,?,?)",
                  (1 if ok else 0, detalle, datetime.now(_TZ).isoformat(timespec="seconds")))


def gemini() -> dict:
    """Objetivo: estado actual de la clave Gemini. Salida: {ok, detalle, ts} (ok None si nunca se usó)."""
    with _conn() as c:
        r = c.execute("SELECT ok, detalle, ts FROM estado WHERE clave='gemini'").fetchone()
    if not r:
        return {"ok": None, "detalle": "sin uso aún", "ts": None}
    return {"ok": bool(r[0]), "detalle": r[1], "ts": r[2]}
