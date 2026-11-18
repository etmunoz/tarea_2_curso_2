# --8<-- encabezado-grupo
# Archivo: src/config/bootstrap.py
# Objetivo: Volcar los ajustes guardados por la web al entorno, SIN pisar las variables ya definidas (.env gana).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1845
# Última modificación: 20261117 1845
# --8<-- fin-encabezado-grupo

"""Al importarse, carga los ajustes del almacén web en os.environ como FALLBACK.

Regla: el entorno (.env / EnvironmentFile) tiene prioridad; solo se rellena lo que falte. Así la config
web es un ingreso ALTERNATIVO de secretos (p. ej. GOOGLE_API_KEY) cuando no se pusieron en el .env.
"""
from __future__ import annotations

import os

try:
    from src.config import ajustes

    for _k, _v in ajustes.todos().items():
        if _v and not os.environ.get(_k):
            os.environ[_k] = _v
except Exception:  # noqa: BLE001
    pass
