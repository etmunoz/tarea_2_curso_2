<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_067.md`
> **Objetivo:** 067 · Respuesta — evidencia LOCAL del funcionamiento de todos los agentes
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
> **Creación:** 20261123 1830 · **Última modificación:** 20261123 1915
<!--/encabezado-grupo-->

# 067 · Respuesta — montaje LOCAL y evidencia de los agentes

**Prompt:** [`../prompts_ejecutados/prompt_067.md`](../prompts_ejecutados/prompt_067.md)

---

## 1. Montaje local (hecho)

- **Claves al `.env` local sin pasar por el chat:** `GOOGLE_API_KEY` (de `/etc/t2c2.env`) y el `REDIS_URL`
  **real** (del almacén de config `logs/config.sqlite`; el de `/etc` era placeholder). Verificado:
  **Gemini OK**, **Redis remoto OK** (dbsize=53). Valores nunca impresos.
- **PostgreSQL 16 local** (Homebrew, nativo, sin Docker). Rol/base `t2c2`; `PG_DSN` en `.env` →
  coordinador con **PostgresSaver** en local.
- **langgraph con los 9 agentes.** `meteo_mcp` fallaba al cargar en el Mac (`cryptography` buscaba
  `libssl.4.dylib`); se **reinstaló `cryptography`** (wheel con openssl incorporado) y pasó a importar.
  Se aplicaron las **fichas** (`tools/configurar_fichas.py`) a las agent cards locales — sin ellas el
  supervisor no distinguía `meteo_mcp` (mundial) de `meteorologia` (Chile). FastAPI, web y monitor con
  el `.env` cargado; vigilante de fichas corriendo.

## 2. Evidencia del funcionamiento de TODOS los agentes — [`../evidencias/agentes_local.md`](../evidencias/agentes_local.md)

Una consulta real por agente, por el gateway local, con fuentes reales (Gemini, Redis remoto, Open-Meteo,
UniProt, tipo de cambio, Wikipedia, MCP Meteosource). **9/9 ruteados correctamente:**

| Agente | Solicitud (resumen) | Elegido |
|---|---|---|
| meteorologia | verificar pronóstico vs observado en Santiago | ✅ Agente de Meteorología |
| **meteo_mcp** | **¿qué clima hace en Madrid hoy?** | ✅ **meteo_mcp** (respaldo Open-Meteo) |
| reiki (RAG) | ¿qué es el Reiki y beneficios? | ✅ Agente de Reiki |
| bioinformatica | gen TP53 en UniProt | ✅ Agente de Bioinformática |
| mlbioinformatica | pipeline ML punta a punta (sin fuga por homología) | ✅ Agente de ML en Bioinformática |
| machinelearning | técnica para desbalance de clases | ✅ Agente de Machine Learning |
| cocinachilena | pastel de choclo con costo | ✅ Agente de Cocina Chilena |
| viajes | Lima: destino + tipo de cambio | ✅ Agente de Viajes |
| administrador | ¿qué agentes hay? | ✅ Agente Administrador |

Todas con ruta `guardia_entrada → supervisor → agente_local → guardia_salida` (la respuesta del agente
llega como **dato** etiquetado `[Nombre]`). **Reparto del clima verificado:** Chile→`meteorologia`,
mundo→`meteo_mcp` (igual que en el VPS).

## 3. Seguridad y memoria — [`../evidencias/backend_local.md`](../evidencias/backend_local.md)

- **Control de acceso (LOCAL):** `/salud`=200; `/agentes` **sin** API_KEY → **401**; **con** API_KEY → **200**
  (sin exponer la clave).
- **Recorrido completo:** `POST /consulta` → `agente_meteorologia` con datos reales (14,1 °C), ruta A2A.
- **UI web (LOCAL):** la misma consulta en `127.0.0.1:8797` muestra la respuesta etiquetada y el panel
  "Ruteo del coordinador" con la ruta — **verificado**; la captura de pantalla la aporta el equipo.
- **PostgresSaver LOCAL:** `[coordinador] checkpointer: postgres`; tabla `checkpoints` con filas > 0
  (persiste). Regla de fallback a `InMemorySaver` verificada antes de instalar la dependencia local.

## 4. Lo que aporta el equipo (como acordamos)

- Captura de la **UI del chat** logueada (pregunta + respuesta + ruteo) — el stack queda levantado para ello.
- **Correo recibido** (bandeja Gmail) y **muestra de voz** (audio/video de `/voz`).
- Rotular la evidencia del **VPS** como el **+1** (entorno remoto).

## 5. Paridad con el VPS (verificada)

El síntoma inicial —"Madrid" respondido por `agente_meteorologia` en vez de `meteo_mcp`— era **solo del
montaje local** (meteo_mcp excluido + fichas sin aplicar), **no un defecto de producción**. Verificado
en vivo en el VPS: catálogo de **9 agentes**; "¿qué clima hace en Madrid hoy?" → **meteo_mcp**
(Meteosource real, 14.2 °C); "clima hoy en Valdivia" → **Agente de Meteorología** (Chile). El reparto
Chile/mundo funciona bien en el VPS: **nada que reparar allí**.

## 6. Estado

- ✅ Montaje local reproducible, **9/9 agentes funcionando en LOCAL** (incluido `meteo_mcp`) con fuentes
  reales, control de acceso y memoria durable (Postgres local) evidenciados como archivos en el repo.
  Paridad con el VPS verificada. Bitácora **067**, Anexo **18**.
