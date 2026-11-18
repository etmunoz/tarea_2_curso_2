<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_032.md`  
> **Objetivo:** 032 · Agente de Viajes como asistente de destino REAL (APIs públicas sin API key)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1245 · **Última modificación:** 20261118 1245
<!--/encabezado-grupo-->

# 032 · Viajes: asistente de destino real

**Pedido del usuario (verbatim):**

> «y qué propondrías para viajes?» → se eligió (a criterio) el alcance completo: **asistente de
> destino real** con APIs públicas sin API key.

**Alcance:**
1. **`src/agente_viajes/clientes.py`** (nuevo): clientes stdlib sin API key.
   - `geocodificar` (Open-Meteo Geocoding, en vivo), `clp_por_unidad`/`convertir` (open.er-api.com,
     cambio real con CLP), `resumen` (Wikipedia REST es).
   - `pais_info`: capital/moneda/idiomas desde una **tabla de referencia incluida** (restcountries
     quedó deprecado); país/zona horaria/coords vienen en vivo del geocoding.
2. **`herramientas.py`**: tools REALES `info_destino`, `tipo_cambio`, `convertir_moneda`,
   `clima_destino` (reusa `agente_meteorologia.openmeteo`), `resumen_destino`. Las tools DEMO
   (`buscar_vuelos`/`buscar_hoteles`/`buscar_actividades`) marcan `fuente="demo"` y se declaran como
   estimación de ejemplo. **Fix:** `buscar_actividades` ahora SÍ está en `HERRAMIENTAS` (antes la ficha
   la mencionaba pero el agente no la exponía).
3. **`prompts.py`** y **`src/fichas.py`**: describen las capacidades reales + la demo etiquetada.
4. **`tests/test_agente_viajes.py`** (nuevo): parseo (geocoding/FX) con JSON de ejemplo + degradación.

**Restricción:** vuelos/hoteles con precio real exigen APIs con key (fuera del diseño keyless); por eso
quedan como DEMO claramente etiquetada. Lo real es destino/moneda/clima/resumen.
