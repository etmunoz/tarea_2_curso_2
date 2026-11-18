# --8<-- encabezado-grupo
# Archivo: src/config/usuarios.py
# Objetivo: Usuarios del frontend: claves hasheadas (PBKDF2), cambio obligatorio al primer ingreso y reset por admin (SQLite).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 2055
# Última modificación: 20261117 2055
# --8<-- fin-encabezado-grupo

"""Almacén de usuarios del frontend web (login con sesión).

Claves hasheadas con PBKDF2-HMAC-SHA256 (salt por usuario). Soporta: alta/seed con una clave inicial
única y `debe_cambiar=1`; verificación; cambio de clave por el propio usuario (quita el flag); reset por
un admin (vuelve a dejar `debe_cambiar=1`). Ruta por env USUARIOS_DB (def. <repo>/logs/usuarios.sqlite).
"""
from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.environ.get("USUARIOS_DB", os.path.join(_RAIZ, "logs", "usuarios.sqlite"))
_TZ = ZoneInfo("America/Santiago")
DDL = ("CREATE TABLE IF NOT EXISTS usuarios (usuario TEXT PRIMARY KEY, salt TEXT, hash TEXT, "
       "debe_cambiar INTEGER NOT NULL DEFAULT 1, rol TEXT NOT NULL DEFAULT 'user', ts TEXT);")


def _ahora() -> str:
    return datetime.now(_TZ).isoformat(timespec="seconds")


def _conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.executescript(DDL)
    return c


def _hash(clave: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", clave.encode(), bytes.fromhex(salt), 120_000).hex()


def crear(usuario: str, clave: str, rol: str = "user", debe_cambiar: int = 1) -> None:
    """Objetivo: crear/reemplazar un usuario con su clave hasheada."""
    salt = secrets.token_hex(16)
    with _conn() as c:
        c.execute("INSERT OR REPLACE INTO usuarios (usuario, salt, hash, debe_cambiar, rol, ts) "
                  "VALUES (?,?,?,?,?,?)", (usuario, salt, _hash(clave, salt), debe_cambiar, rol, _ahora()))


def hay_usuarios() -> bool:
    with _conn() as c:
        return c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0] > 0


def seed(usuarios: list[str], clave_inicial: str, admin: str = "") -> bool:
    """Objetivo: si la tabla está vacía, crear los usuarios con la clave inicial única y cambio obligatorio.
    El usuario `admin` queda con rol 'admin'. Salida: True si sembró."""
    if hay_usuarios() or not clave_inicial or not usuarios:
        return False
    for u in usuarios:
        crear(u, clave_inicial, rol=("admin" if u == admin else "user"), debe_cambiar=1)
    return True


def verificar(usuario: str, clave: str) -> bool:
    """Objetivo: True si la clave coincide (tiempo constante)."""
    with _conn() as c:
        r = c.execute("SELECT salt, hash FROM usuarios WHERE usuario=?", (usuario,)).fetchone()
    if not r:
        return False
    return hmac.compare_digest(_hash(clave, r["salt"]), r["hash"])


def debe_cambiar(usuario: str) -> bool:
    with _conn() as c:
        r = c.execute("SELECT debe_cambiar FROM usuarios WHERE usuario=?", (usuario,)).fetchone()
    return bool(r and r["debe_cambiar"])


def es_admin(usuario: str) -> bool:
    with _conn() as c:
        r = c.execute("SELECT rol FROM usuarios WHERE usuario=?", (usuario,)).fetchone()
    return bool(r and r["rol"] == "admin")


def cambiar_clave(usuario: str, nueva: str) -> bool:
    """Objetivo: el propio usuario cambia su clave (quita el flag de cambio obligatorio)."""
    if not nueva or len(nueva) < 6:
        return False
    salt = secrets.token_hex(16)
    with _conn() as c:
        cur = c.execute("UPDATE usuarios SET salt=?, hash=?, debe_cambiar=0, ts=? WHERE usuario=?",
                        (salt, _hash(nueva, salt), _ahora(), usuario))
    return cur.rowcount > 0


def resetear_clave(usuario: str, nueva: str) -> bool:
    """Objetivo: un admin resetea la clave de un usuario (vuelve a exigir cambio al entrar)."""
    if not nueva or len(nueva) < 6:
        return False
    salt = secrets.token_hex(16)
    with _conn() as c:
        cur = c.execute("UPDATE usuarios SET salt=?, hash=?, debe_cambiar=1, ts=? WHERE usuario=?",
                        (salt, _hash(nueva, salt), _ahora(), usuario))
    return cur.rowcount > 0


def listar() -> list[dict]:
    with _conn() as c:
        return [dict(x) for x in c.execute(
            "SELECT usuario, rol, debe_cambiar, ts FROM usuarios ORDER BY usuario").fetchall()]
