<!--encabezado-grupo-->
> **Archivo:** `evidencias/mcp-adaptador.md`  
> **Objetivo:** Evidencia de validación offline del adaptador MCP propio.  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261122 0000 · **Última modificación:** 20261122 0000
<!--/encabezado-grupo-->

# Evidencia: adaptador MCP propio

Fecha: 2026-11-22

## Validaciones realizadas

```text
python -m pip check
No broken requirements found.

python -m pytest tests/test_mcp_langchain.py -q
7 passed

python -m pytest tests/test_tarea2.py -q
12 passed
```

Las pruebas usan un servidor MCP simulado, sin red, y cubren descubrimiento, conversión a
`StructuredTool`, ejecución, errores, inicialización única y cierre del transporte/sesión.
