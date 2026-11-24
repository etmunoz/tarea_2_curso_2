<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_072.md`
> **Objetivo:** 072 · Día de la semana en el dato y tests herméticos
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
> **Creación:** 20261124 1700 · **Última modificación:** 20261124 1700
<!--/encabezado-grupo-->

# 072 · Resultado

- **Fallo 1:** `openmeteo.dia_semana` y el campo `dia` en cada día del pronóstico (`pronostico_hoy`,
  `pronostico_semana` y el respaldo de `meteo_mcp`). El prompt de Meteorología exige usar `dia` sin
  recalcularlo. Test `test_dia_semana_lo_calcula_la_herramienta`.
- **Fallo 2:** se eliminó `tests/test_consumidor.py` (el módulo `src.consumidor`, de Taller 1, no está en la
  entrega). Los tests del puente A2A (`src.puente_a2a`) se omiten con `skipif` si el módulo falta.
  `test_consultar_hace_fallback_local` usa una clave ficticia: no llama a Gemini.
- `pytest` sin `GOOGLE_API_KEY`: **172 passed, 17 skipped** (sin contar 3 módulos MCP, que requieren
  `mcp==2.3.0` instalado con `uv sync`).
