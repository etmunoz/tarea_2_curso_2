<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_063.md`  
> **Objetivo:** 063 · Respuesta — meteo_mcp integrado con "Clima resiliente en dos niveles"  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261123 1200 · **Última modificación:** 20261123 1200
<!--/encabezado-grupo-->

# 063 · Respuesta — Clima resiliente (meteo_mcp)

**Prompt:** [`../prompts_ejecutados/prompt_063.md`](../prompts_ejecutados/prompt_063.md)

---

## 1. Dependencia `mcp==2.3.0` — 🟢 verificada

- **dry-run** contra el venv de producción: agrega solo `mcp`, `mcp-types`, `python-multipart`;
  **0 downgrades** (nada que ver con el incidente del `langgraph-checkpoint`).
- `httpx2` (usado por el adaptador) está siempre presente (transitiva de `google-genai`/`langsmith`).
- Instalada en el VPS; `from mcp.client.streamable_http import streamable_http_client` **existe**; el
  grafo `meteo_mcp` **importa limpio** y exporta `graph` (CompiledStateGraph) — seguro para `langgraph.json`.

## 2. Merge del PR #1

`feature/gustavo-changes` → `main` (`72e6ba1`), fast-forward, sin conflictos. Trae `agente_meteo_mcp/`,
`integraciones/`, tests, ficha, `langgraph.json`+catálogo y bitácora 044–062.

## 3. "Clima resiliente en dos niveles" (implementado)

- **Fallback** `pronostico_respaldo` en `meteo_mcp` (Open-Meteo keyless, mundial) + regla de prompt: si
  Meteosource no está disponible, responde igual avisando que es fuente de respaldo.
- **Fichas**: `meteo_mcp` = clima mundial por defecto + respaldo; `meteorologia` = verificación
  (pronóstico vs observado) + Chile keyless; `viajes` = **sin clima**, deriva a meteo_mcp.
- `viajes`: se quitó `clima_destino` de `HERRAMIENTAS` y del prompt (deriva).
- `.env.example` deduplicado; `mcp.meteosource.com` agregado al **egress**; `ARQUITECTURA.md` al día.

## 4. Verificación

- **Tests:** VPS `pytest tests/test_meteo_mcp.py tests/test_mcp_langchain.py tests/test_descubre_mcp.py
  tests/test_agente_viajes.py` → **30 passed** (incluye el fallback). Local (sin mcp) → **164 passed**.
- **En vivo (tras reiniciar + key):** pendiente — ver §5.

## 5. Pendiente de activación

- La **API key de Meteosource** va en `/etc/t2c2.env` del VPS (la carga Ezequiel/administrator, oculta).
- `sudo systemctl restart t2c2-langgraph` → verificar: (a) `meteo_mcp` responde clima mundial con
  Meteosource; (b) **sin key, cae a Open-Meteo** (respaldo); (c) el supervisor rutea el clima a meteo_mcp
  y `viajes` deriva.

## 6. Estado

- ✅ Dependencia OK, merge hecho, clima resiliente implementado, tests verdes, docs al día. Bitácora **063**.
