<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_063.md`  
> **Objetivo:** 063 · Integrar meteo_mcp (MCP Meteosource) con el patrón "Clima resiliente en dos niveles"  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261123 1200 · **Última modificación:** 20261123 1200
<!--/encabezado-grupo-->

# 063 · Clima resiliente en dos niveles (meteo_mcp)

**Pedido del usuario (verbatim):**

> «revisa el PR de Fabio…» → luego el **PR #1 de Gustavo**: nuevo `agente_meteo_mcp` con un **MCP real de
> Meteosource** (de pago). «me gustó tu propuesta: "Clima resiliente en dos niveles" 🌦️ anótalo para el
> prompt. Y sigamos viendo los temas a resolver… tengo la clave, cómo la agregamos… escribe el prompt
> para este caso, luego su salida y las evidencias correspondientes. Vamos!!!»

**Contexto:** Gustavo agregó `src/agente_meteo_mcp/` (grafo con guardia propia + 3 tools MCP:
`search_places`, `get_forecast`, `get_weather_history`), el adaptador `src/integraciones/mcp_langchain.py`
y la dependencia `mcp==2.3.0`, integrado a `langgraph.json` y al catálogo. Quedaban: validar la
dependencia, resolver el **solape de 3 agentes de clima** y cargar la API key de forma segura.

**Decisión de diseño acordada — "Clima resiliente en dos niveles":**
- **`meteo_mcp` = clima MUNDIAL por defecto** (Meteosource MCP, por hora + histórico), con **respaldo
  keyless Open-Meteo** si el servicio de pago no está disponible (sin key, cuota, caído, egress).
- **`agente_meteorologia` = verificación (pronóstico vs observado) + Chile keyless** (su nicho único).
- **`agente_viajes` deja el clima** y lo deriva a `meteo_mcp`.

**Alcance:**
1. **Dependencia:** verificar que `mcp==2.3.0` instala sin romper el stack (dry-run + imports reales).
2. **Merge** del PR #1 a `main`.
3. **Fallback** en `meteo_mcp`: tool `pronostico_respaldo` (Open-Meteo, reusa `openmeteo.py` +
   `clientes.geocodificar`) + regla en el prompt.
4. **Fichas** de los 3 agentes de clima + `viajes` sin `clima_destino` (deriva).
5. **`.env.example`** deduplicado; **egress** agrega `mcp.meteosource.com`; **ARQUITECTURA** al día.
6. **Tests** del fallback. **Clave** de Meteosource: en `/etc/t2c2.env` del VPS (oculta), nunca en el chat.

**Restricción:** la API key de pago no pasa por el chat ni la ve Claude; se carga directo en el VPS. El
sistema funciona **sin la key** gracias al respaldo Open-Meteo.
