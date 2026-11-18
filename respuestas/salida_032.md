<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_032.md`  
> **Objetivo:** 032 · Respuesta — Viajes: asistente de destino real (sin API key)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1245 · **Última modificación:** 20261118 1245
<!--/encabezado-grupo-->

# 032 · Respuesta — Viajes real

**Prompt:** [`../prompts_ejecutados/prompt_032.md`](../prompts_ejecutados/prompt_032.md)

---

## 1. Qué se hizo

- 5 herramientas REALES sin API key: `info_destino`, `tipo_cambio`, `convertir_moneda`,
  `clima_destino`, `resumen_destino`. 3 DEMO etiquetadas (`fuente="demo"`).
- Fuentes: Open-Meteo Geocoding + clima, open.er-api.com (cambio, soporta CLP), Wikipedia REST,
  y tabla de referencia incluida para capital/moneda/idiomas (restcountries quedó deprecado).
- Prompt + ficha actualizados; **fix**: `buscar_actividades` ahora está en `HERRAMIENTAS`.
- Tests nuevos: **5 passed**.

## 2. Verificación (clientes/tools en vivo, VPS)

- `info_destino("Cusco")` → Cuzco, Perú, zona horaria America/Lima, pobl. 428.450 (en vivo) +
  capital Lima, moneda **PEN**, idiomas [español, quechua, aimara].
- `clp_por_unidad("USD")` ≈ **998,6 CLP**. `convertir(50000, CLP, PEN)` ≈ **171,05 PEN**.
- `resumen("Cusco")` → extracto real de Wikipedia.

## 3. Pendiente / en vivo

- `sudo systemctl restart t2c2-langgraph` (tools nuevas). Ficha ya aplicada.
- Verificación por el gateway (consulta de destino ruteada al Agente de Viajes) → evidencias.

## 4. Estado

- ✅ Código + prompt + ficha + tests; desplegado. Bitácora **032**.
