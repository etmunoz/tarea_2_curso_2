<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_062.md`  
> **Objetivo:** Resultado de corregir el historial climático relativo en meteo_mcp.  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261123 0000 · **Última modificación:** 20261123 0000
<!--/encabezado-grupo-->

# Resultado del prompt 062

## Diagnóstico

El modelo interpretaba “hace 2 días” como una fecha antigua (`2025-02-20`), que la cuenta de
Meteosource no permite. También reenviaba latitud/longitud junto con `place_id`.

## Correcciones

- Se agregó la fecha actual de `America/Santiago` al prompt del agente.
- Las expresiones relativas usan esa fecha como referencia.
- Las tools envían sólo `place_id` cuando está disponible.

## Validación real

La consulta:

```text
Como estuvo el tiempo hace 2 dias en Santiago ?
```

ahora devuelve datos del **21 de noviembre de 2026** y recorre:

```text
guardia_de_entrada → agente → search_places → get_weather_history
```

Pruebas:

- `tests/test_meteo_mcp.py`: 13 pasaron.
- `tests/test_tarea2.py`: 12 pasaron.
- `pip check`: sin dependencias rotas.
