<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_052.md`  
> **Objetivo:** Resultado de la eliminación completa del bloque extras: signature.  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261122 0000 · **Última modificación:** 20261122 0000
<!--/encabezado-grupo-->

# Resultado del prompt 052

## Cambios

- La limpieza ahora corta desde `extras: signature:`.
- También elimina el separador anterior `,` o `;`.
- Se mantiene una prueba con el formato real observado en la terminal.

## Validaciones

- `tests/test_meteo_mcp.py`: 5 pasaron.
- `tests/test_tarea2.py`: 12 pasaron.
- `pip check`: sin dependencias rotas.
