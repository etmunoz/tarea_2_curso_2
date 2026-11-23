<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_055.md`  
> **Objetivo:** Resultado de la corrección del modo --saltos.  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261122 0000 · **Última modificación:** 20261122 0000
<!--/encabezado-grupo-->

# Resultado del prompt 055

## Diagnóstico

`graph.astream(..., stream_mode="updates")` entrega los mensajes dentro de cada nodo. El código
buscaba `messages` en el nivel raíz y por eso no encontraba la respuesta final.

## Corrección

`saltos()` ahora conserva el último mensaje recibido dentro de las actualizaciones y lo devuelve
después de mostrar el recorrido.

## Validaciones

- `tests/test_meteo_mcp.py`: 8 pasaron.
- `tests/test_tarea2.py`: 12 pasaron.
- `pip check`: sin dependencias rotas.
