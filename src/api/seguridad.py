# --8<-- encabezado-grupo
# Archivo: src/api/seguridad.py
# Objetivo: Dependencia de FastAPI que exige la API_KEY (header X-API-Key) en endpoints que invocan agentes.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1544
# Última modificación: 20261117 1544
# --8<-- fin-encabezado-grupo

"""Dependencia de seguridad: valida la API_KEY (env API_KEY) contra el header X-API-Key. Sin ella -> 401."""
from __future__ import annotations

import os

from fastapi import Header, HTTPException, status

from src.api.claves import clave_valida


def verificar_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    """Objetivo: cortar con 401 si la API_KEY es inválida o ausente. No revela la clave real."""
    if not clave_valida(x_api_key, os.environ.get("API_KEY", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API_KEY inválida o ausente")
