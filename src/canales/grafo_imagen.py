# --8<-- encabezado-grupo
# Archivo: src/canales/grafo_imagen.py
# Objetivo: Diagrama del grafo del coordinador (Mermaid) y su PNG para embeber en el correo.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1552
# Última modificación: 20261117 1552
# --8<-- fin-encabezado-grupo

"""Diagrama del flujo del coordinador para el pie del correo.

`mermaid_coordinador()` devuelve el Mermaid (texto, siempre disponible). `png_coordinador()` intenta
renderizarlo a PNG (cacheado en logs/) con langchain_core; si no se puede (sin red o sin venv), devuelve
None y el correo usa el Mermaid como texto de respaldo.
"""
from __future__ import annotations

import os

_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.environ.get("GRAFO_PNG", os.path.join(_RAIZ, "logs", "grafo_coordinador.png"))

# Flujo real del supervisor (src/coordinador/graph.py): guardia_entrada -> enrutar -> consultar|sin_agente -> guardia_salida
MERMAID = """graph TD
  START([inicio]) --> GE[guardia_entrada]
  GE -->|ok| EN[enrutar]
  GE -->|bloqueado| GS[guardia_salida]
  EN -->|consultar| CO[consultar]
  EN -->|sin_agente| SA[sin_agente]
  CO --> GS
  SA --> GS
  GS --> FIN([fin])"""


def mermaid_coordinador() -> str:
    """Objetivo: el diagrama Mermaid del coordinador (texto)."""
    return MERMAID


def png_coordinador() -> str | None:
    """Objetivo: ruta a un PNG del grafo (cacheado); None si no se pudo renderizar."""
    if os.path.exists(CACHE) and os.path.getsize(CACHE) > 0:
        return CACHE
    try:
        from langchain_core.runnables.graph import MermaidDrawMethod  # noqa: PLC0415
        from langchain_core.runnables.graph_mermaid import draw_mermaid_png  # noqa: PLC0415
        png = draw_mermaid_png(MERMAID, draw_method=MermaidDrawMethod.API)
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        with open(CACHE, "wb") as f:
            f.write(png)
        return CACHE
    except Exception:  # noqa: BLE001
        return None
