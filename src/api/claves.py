# --8<-- encabezado-grupo
# Archivo: src/api/claves.py
# Objetivo: Validación de la API_KEY del gateway (stdlib; comparación en tiempo constante).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1544
# Última modificación: 20261117 1544
# --8<-- fin-encabezado-grupo

"""Validación de la API_KEY del gateway, aislada (solo stdlib) para poder probarla sin FastAPI."""
from __future__ import annotations

import hmac


def clave_valida(provista: str | None, esperada: str | None) -> bool:
    """Objetivo: True solo si ambas no son vacías y coinciden (comparación en tiempo constante)."""
    if not provista or not esperada:
        return False
    return hmac.compare_digest(str(provista), str(esperada))
