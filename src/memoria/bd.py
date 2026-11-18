# --8<-- encabezado-grupo
# Archivo: src/memoria/bd.py
# Objetivo: Memoria de largo plazo en SQLite: conversación, destinatarios (allowlist), despachos y accesos.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1544
# Última modificación: 20261117 1627
# --8<-- fin-encabezado-grupo

"""Memoria de largo plazo en SQLite (stdlib).

Tablas: `conversaciones` (historial por sesión), `destinatarios` (allowlist autogestionada, §7),
`despachos` (bitácora de correos) y `accesos` (bitácora de llamadas al gateway FastAPI, para el monitor).
Ruta por env MEMORIA_DB (def. `<repo>/logs/memoria.sqlite`). Horas en America/Santiago.
"""
from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.environ.get("MEMORIA_DB", os.path.join(_RAIZ, "logs", "memoria.sqlite"))
_TZ = ZoneInfo("America/Santiago")

DDL = """
CREATE TABLE IF NOT EXISTS conversaciones (
  id INTEGER PRIMARY KEY AUTOINCREMENT, sesion TEXT NOT NULL, rol TEXT NOT NULL,
  contenido TEXT NOT NULL, agente TEXT, ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS destinatarios (
  correo TEXT PRIMARY KEY, nombre TEXT, activo INTEGER NOT NULL DEFAULT 1, alta_ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS despachos (
  id INTEGER PRIMARY KEY AUTOINCREMENT, destinatario TEXT NOT NULL, asunto TEXT,
  estado TEXT NOT NULL, ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS accesos (
  id INTEGER PRIMARY KEY AUTOINCREMENT, ruta TEXT NOT NULL, metodo TEXT NOT NULL,
  status INTEGER NOT NULL, con_api_key INTEGER NOT NULL, ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS eventos (
  id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT, evento TEXT NOT NULL, ts TEXT NOT NULL
);
"""


def _ahora() -> str:
    return datetime.now(_TZ).isoformat(timespec="seconds")


def _conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.executescript(DDL)
    return c


# --- Historial de conversación ---
def guardar_mensaje(sesion: str, rol: str, contenido: str, agente: str | None = None) -> None:
    """Objetivo: registrar un turno (rol 'usuario'|'asistente') de una sesión."""
    with _conn() as c:
        c.execute("INSERT INTO conversaciones (sesion, rol, contenido, agente, ts) VALUES (?,?,?,?,?)",
                  (sesion, rol, contenido, agente, _ahora()))


def historial(sesion: str, limite: int = 50) -> list[dict]:
    """Objetivo: últimos turnos de una sesión, en orden cronológico."""
    with _conn() as c:
        filas = c.execute("SELECT rol, contenido, agente, ts FROM conversaciones WHERE sesion=? "
                          "ORDER BY id DESC LIMIT ?", (sesion, limite)).fetchall()
    return [dict(f) for f in reversed(filas)]


def historial_reciente(limite: int = 50) -> list[dict]:
    """Objetivo: últimos turnos de cualquier sesión (para el monitor)."""
    with _conn() as c:
        filas = c.execute("SELECT sesion, rol, contenido, agente, ts FROM conversaciones "
                          "ORDER BY id DESC LIMIT ?", (limite,)).fetchall()
    return [dict(f) for f in filas]


# --- Destinatarios (allowlist autogestionada, §7) ---
def _norm(correo: str) -> str:
    return (correo or "").strip().lower()


def registrar_destinatario(correo: str, nombre: str = "") -> dict:
    """Objetivo: alta idempotente de un destinatario (lo deja activo)."""
    c0 = _norm(correo)
    with _conn() as c:
        existe = c.execute("SELECT alta_ts FROM destinatarios WHERE correo=?", (c0,)).fetchone()
        alta = existe["alta_ts"] if existe else _ahora()
        c.execute("INSERT OR REPLACE INTO destinatarios (correo, nombre, activo, alta_ts) VALUES (?,?,1,?)",
                  (c0, nombre, alta))
    return {"correo": c0, "nombre": nombre, "activo": 1, "alta_ts": alta}


def baja_destinatario(correo: str) -> bool:
    """Objetivo: baja lógica (activo=0). Salida: True si existía."""
    with _conn() as c:
        cur = c.execute("UPDATE destinatarios SET activo=0 WHERE correo=?", (_norm(correo),))
        return cur.rowcount > 0


def listar_destinatarios(solo_activos: bool = True) -> list[dict]:
    """Objetivo: destinatarios registrados (por defecto solo los activos)."""
    q = "SELECT correo, nombre, activo, alta_ts FROM destinatarios"
    if solo_activos:
        q += " WHERE activo=1"
    with _conn() as c:
        return [dict(f) for f in c.execute(q + " ORDER BY correo").fetchall()]


def es_destinatario_permitido(correo: str) -> bool:
    """Objetivo: True si el correo está en la allowlist y activo."""
    with _conn() as c:
        r = c.execute("SELECT 1 FROM destinatarios WHERE correo=? AND activo=1", (_norm(correo),)).fetchone()
    return r is not None


def correo_de_usuario(usuario: str):
    """Objetivo: el correo activo registrado por un usuario (guardado con nombre=usuario), o None."""
    with _conn() as c:
        r = c.execute("SELECT correo FROM destinatarios WHERE nombre=? AND activo=1 ORDER BY alta_ts DESC LIMIT 1", (usuario,)).fetchone()
    return r["correo"] if r else None


# --- Bitácora de despachos ---
def registrar_despacho(destinatario: str, asunto: str, estado: str) -> int:
    """Objetivo: registrar un intento/resultado de envío. Salida: id del despacho."""
    with _conn() as c:
        cur = c.execute("INSERT INTO despachos (destinatario, asunto, estado, ts) VALUES (?,?,?,?)",
                        (_norm(destinatario), asunto, estado, _ahora()))
        return cur.lastrowid


def despachos(limite: int = 50) -> list[dict]:
    """Objetivo: últimos despachos registrados."""
    with _conn() as c:
        filas = c.execute("SELECT destinatario, asunto, estado, ts FROM despachos "
                          "ORDER BY id DESC LIMIT ?", (limite,)).fetchall()
    return [dict(f) for f in filas]


# --- Bitácora de accesos al gateway (para el monitor) ---
def registrar_acceso(ruta: str, metodo: str, status: int, con_api_key: bool) -> None:
    """Objetivo: registrar una llamada al gateway (sin guardar la clave; solo si venía o no)."""
    with _conn() as c:
        c.execute("INSERT INTO accesos (ruta, metodo, status, con_api_key, ts) VALUES (?,?,?,?,?)",
                  (ruta, metodo, int(status), 1 if con_api_key else 0, _ahora()))


def accesos(limite: int = 50) -> list[dict]:
    """Objetivo: últimos accesos registrados."""
    with _conn() as c:
        filas = c.execute("SELECT ruta, metodo, status, con_api_key, ts FROM accesos "
                          "ORDER BY id DESC LIMIT ?", (limite,)).fetchall()
    return [dict(f) for f in filas]


def resumen_accesos() -> dict:
    """Objetivo: totales de accesos (permitidos vs rechazados) para el panel del monitor."""
    with _conn() as c:
        total = c.execute("SELECT COUNT(*) FROM accesos").fetchone()[0]
        permit = c.execute("SELECT COUNT(*) FROM accesos WHERE status < 400").fetchone()[0]
        rechaz = c.execute("SELECT COUNT(*) FROM accesos WHERE status >= 400").fetchone()[0]
    return {"total": total, "permitido": permit, "rechazado": rechaz}


def registrar_evento(usuario: str, evento: str) -> None:
    """Objetivo: registrar un evento de sesion de usuario (login/logout/cambio_clave/reset_admin)."""
    with _conn() as c:
        c.execute("INSERT INTO eventos (usuario, evento, ts) VALUES (?,?,?)", (usuario or "", evento, _ahora()))


def eventos(limite: int = 50) -> list[dict]:
    """Objetivo: ultimos eventos de sesion de usuario."""
    with _conn() as c:
        filas = c.execute("SELECT usuario, evento, ts FROM eventos ORDER BY id DESC LIMIT ?", (limite,)).fetchall()
    return [dict(f) for f in filas]
