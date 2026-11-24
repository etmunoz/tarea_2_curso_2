# --8<-- encabezado-grupo
# Archivo: tools/reset_evaluador.py
# Objetivo: Dejar "en cero" el contexto de un usuario (p. ej. el evaluador) para probar de nuevo.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261123 1900
# Última modificación: 20261123 1900
# --8<-- fin-encabezado-grupo
"""Reseteador de contexto para pruebas de evaluación.

Borra TODO lo que un usuario (por defecto ``evaluador``) va acumulando al probar el sistema, para
poder repetir la prueba desde cero: el historial de conversación (y, por tanto, la memoria de
seguimiento), su perfil recordado (nombre/idioma/saludo), sus eventos, su correo en la allowlist y
los checkpoints del coordinador en Postgres de sus hilos. No toca la cuenta de login (puedes volver
a entrar con el mismo usuario/clave) ni el código ni los secretos.

Uso (desde la raíz del repo, con el venv):

    .venv/bin/python tools/reset_evaluador.py                 # resetea al usuario 'evaluador'
    .venv/bin/python tools/reset_evaluador.py --usuario juan  # otro usuario
    .venv/bin/python tools/reset_evaluador.py --dry-run       # muestra qué borraría, sin borrar
    .venv/bin/python tools/reset_evaluador.py --logs-globales # además: accesos, despachos y TODA la allowlist

Lee la configuración del ``.env`` (incluido ``PG_DSN`` para Postgres). Si Postgres no está, avisa y
sigue con SQLite (el gateway cae a InMemorySaver de todos modos).
"""
from __future__ import annotations

import argparse
import os
import pathlib
import sqlite3
import sys

# Permite ejecutar el script directamente (python tools/reset_evaluador.py): añade la raíz del repo.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))


def _cargar_env() -> None:
    """Carga el .env al entorno sin pisar variables ya definidas."""
    env = pathlib.Path(".env")
    if not env.exists():
        return
    for linea in env.read_text().splitlines():
        if "=" in linea and not linea.strip().startswith("#"):
            clave, valor = linea.split("=", 1)
            os.environ.setdefault(clave.strip(), valor.strip())


def _ruta_memoria() -> str:
    """Descubre la ruta del SQLite de memoria que usa el proyecto."""
    from src.memoria import bd as memoria  # noqa: PLC0415

    for valor in vars(memoria).values():
        if isinstance(valor, (str, pathlib.Path)) and str(valor).endswith(".sqlite") and "memoria" in str(valor):
            return str(valor)
    # respaldo: ubicación habitual
    return "logs/memoria.sqlite"


def _reset_sqlite(usuario: str, logs_globales: bool, dry_run: bool) -> dict[str, int]:
    """Borra del SQLite de memoria el rastro del usuario. Devuelve {tabla: filas_afectadas}."""
    ruta = _ruta_memoria()
    con = sqlite3.connect(ruta)
    prefijo = f"{usuario}:%"  # los hilos son 'usuario:sesion'
    plan: list[tuple[str, str, tuple]] = [
        ("conversaciones (hilos del usuario)", "DELETE FROM conversaciones WHERE sesion LIKE ?", (prefijo,)),
        ("perfiles (perfil recordado)", "DELETE FROM perfiles WHERE usuario = ?", (usuario,)),
        ("eventos (login/logout/cambios)", "DELETE FROM eventos WHERE usuario = ?", (usuario,)),
        ("destinatarios (correo registrado por el usuario)", "DELETE FROM destinatarios WHERE nombre = ?", (usuario,)),
    ]
    if logs_globales:
        plan += [
            ("destinatarios (TODA la allowlist)", "DELETE FROM destinatarios", ()),
            ("despachos (log de correos)", "DELETE FROM despachos", ()),
            ("accesos (log 200/401)", "DELETE FROM accesos", ()),
        ]
    afectadas: dict[str, int] = {}
    for etiqueta, sql, args in plan:
        contar = sql.replace("DELETE FROM", "SELECT COUNT(*) FROM", 1)
        n = con.execute(contar, args).fetchone()[0]
        if not dry_run and n:
            con.execute(sql, args)
        afectadas[etiqueta] = n
    if not dry_run:
        con.commit()
    con.close()
    return afectadas


def _reset_postgres(usuario: str, dry_run: bool) -> str:
    """Borra los checkpoints del coordinador (Postgres) de los hilos del usuario. Devuelve un resumen."""
    dsn = os.environ.get("PG_DSN", "").strip()
    if not dsn:
        return "Postgres: sin PG_DSN (nada que borrar; el coordinador usa memoria volátil)."
    try:
        from psycopg_pool import ConnectionPool  # noqa: PLC0415
        from langgraph.checkpoint.postgres import PostgresSaver  # noqa: PLC0415

        pool = ConnectionPool(conninfo=dsn, open=True, timeout=5,
                              kwargs={"autocommit": True, "prepare_threshold": 0})
        with pool.connection() as c:
            filas = [r[0] for r in c.execute(
                "SELECT DISTINCT thread_id FROM checkpoints WHERE thread_id LIKE %s", (f"{usuario}:%",))]
        if dry_run:
            pool.close()
            return f"Postgres: {len(filas)} hilo(s) del usuario se borrarían (dry-run)."
        cp = PostgresSaver(pool)
        for thread_id in filas:
            cp.delete_thread(thread_id)
        pool.close()
        return f"Postgres: {len(filas)} hilo(s) del usuario borrados de checkpoints."
    except Exception as error:  # noqa: BLE001
        return f"Postgres: no se pudo limpiar ({type(error).__name__}: {str(error)[:80]})."


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--usuario", default="evaluador", help="Usuario a resetear (def. evaluador).")
    ap.add_argument("--logs-globales", action="store_true",
                    help="Además borra accesos, despachos y TODA la allowlist (deja todo pristino).")
    ap.add_argument("--dry-run", action="store_true", help="Muestra qué borraría, sin borrar nada.")
    args = ap.parse_args()

    _cargar_env()
    print(f"{'DRY-RUN · ' if args.dry_run else ''}Reseteando el contexto de «{args.usuario}»\n")

    sql = _reset_sqlite(args.usuario, args.logs_globales, args.dry_run)
    print("SQLite (memoria):")
    for etiqueta, n in sql.items():
        marca = "·" if n == 0 else ("→" if args.dry_run else "✓")
        print(f"  {marca} {etiqueta}: {n} fila(s)")

    print("\n" + _reset_postgres(args.usuario, args.dry_run))

    if args.dry_run:
        print("\n(Nada se borró — quita --dry-run para aplicar.)")
    else:
        print(f"\nListo: «{args.usuario}» quedó en cero EN EL SERVIDOR.")
        print("\n  OJO (lado navegador — esto NO lo puede borrar un script del servidor):")
        print("   - El login es una cookie y el historial del chat vive en sessionStorage del navegador.")
        print("   - Para una demo 100% limpia (pide credenciales + chat vacío + onboarding de correo):")
        print("       >>> abre una ventana de INCÓGNITO (Chrome: Cmd+Shift+N) en http://127.0.0.1:8797/")
        print("     Alternativa: 🚪 Salir (cerrar sesión) + 🔄 Nueva conversación en la misma ventana.")


if __name__ == "__main__":
    main()
