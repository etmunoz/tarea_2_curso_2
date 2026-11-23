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
- **langgraph** con `langgraph.local.json` (8 agentes; `meteo_mcp` excluido en Mac por el fallo de
  `cryptography`/`libssl`; en el VPS siguen los 9). FastAPI, web y monitor levantados con el `.env` cargado.

## 2. Evidencia del funcionamiento de TODOS los agentes — [`../evidencias/agentes_local.md`](../evidencias/agentes_local.md)

Una consulta real por agente, por el gateway local, con fuentes reales (Gemini, Redis remoto, Open-Meteo,
UniProt, tipo de cambio, Wikipedia). **8/8 ruteados correctamente:**

| Agente | Solicitud (resumen) | Elegido |
|---|---|---|
| meteorologia | clima hoy en Valdivia | ✅ `agente_meteorologia` |
| reiki (RAG) | ¿qué es el Reiki y beneficios? | ✅ `agente_reiki` |
| bioinformatica | gen TP53 en UniProt | ✅ `agente_bioinformatica` |
| mlbioinformatica | pipeline ML punta a punta (sin fuga por homología) | ✅ `agente_mlbioinformatica` |
| machinelearning | técnica para desbalance de clases | ✅ `agente_machinelearning` |
| cocinachilena | pastel de choclo con costo | ✅ `agente_cocinachilena` |
| viajes | Lima: destino + tipo de cambio | ✅ `agente_viajes` |
| administrador | ¿qué agentes hay? | ✅ `agente_administrador` |

Todas con ruta `guardia_entrada → supervisor → agente_local → guardia_salida` (la respuesta del agente
llega como **dato** etiquetado `[agente_...]`). El 9º agente, `meteo_mcp`, está probado en el VPS
(Anexos 14/17).

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

## 5. Estado

- ✅ Montaje local reproducible, **8/8 agentes funcionando en LOCAL** con fuentes reales, control de
  acceso y memoria durable (Postgres local) evidenciados como archivos en el repo. Bitácora **067**,
  Anexo **18**.
