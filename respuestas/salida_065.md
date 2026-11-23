<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_065.md`
> **Objetivo:** 065 · Respuesta — documentación al día para presentar a profesores
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
> **Creación:** 20261123 1730 · **Última modificación:** 20261123 1730
<!--/encabezado-grupo-->

# 065 · Respuesta — documentación coherente y al día

**Prompt:** [`../prompts_ejecutados/prompt_065.md`](../prompts_ejecutados/prompt_065.md)

---

## 1. Inventario de staleness encontrado

| Archivo | Problema | Acción |
|---|---|---|
| `README.md` | "8 agentes" ×2; sin meteo_mcp ni Postgres | 9 agentes, meteo_mcp en texto y diagrama, nota de PostgresSaver, vars en Requisitos |
| `AGENTS.md` | "8 agentes" ×2; checkpointer "InMemorySaver"; estructura sin meteo_mcp/integraciones | 9 agentes, meteo_mcp, checkpointer Postgres/InMemory, estructura + fecha |
| `deploy/README-T2.md` | "8 agentes locales"; sin PG_DSN/MCP en requisitos | 9 agentes; bloque de opcionales (MCP + PG_DSN con pasos) |
| `deploy/CHECKLIST-ACTIVACION.md` | `chown root:web6` (incorrecto); sin MCP/PG_DSN | `root:client1`; ítems opcionales MCP y Postgres |
| `deploy/t2c2.env.example` | `A2A_GRAFOS_LOCALES` sin meteo_mcp; sin MCP/PG_DSN; `root:web6` | +meteo_mcp, +vars MCP, +PG_DSN (comentado), `root:client1` |
| `.env.example` | "8 agentes" en comentario; sin PG_DSN | 9 agentes; bloque PG_DSN opcional |
| `docs/MEJORAS_FUTURAS.md` | ítem 3 (checkpointer) ya **hecho** en 064 | marcado ✅ HECHO; nuevos §5 (hilos de agentes) y §6 (hardening Postgres) |
| `docs/decisiones/ADR-0001` | 2 notas con "8 agentes" | → 9 agentes |
| `docs/ARQUITECTURA.md` | ya actualizado en 064 | verificado (9 agentes + meteo_mcp + Postgres); Mermaid balanceado |

## 2. Consistencia verificada

- **0 rezagos** de "8 agentes/grafos" en todo el repo (salvo donde describe historia, ya corregido).
- Los **3 diagramas Mermaid** (coordinador en README y AGENTS, arquitectura técnica) muestran los **9
  agentes** con `meteo_mcp`; el de arquitectura marca el checkpointer Postgres del coordinador.
  `subgraph`/`end` balanceados (el conteo 8/7 en ARQUITECTURA es la mención en prosa del "Prompt de
  mantención", no un bloque).
- **`chown root:client1`** coherente en los 3 lugares de `deploy/` (antes había `root:web6` en dos).
- `A2A_GRAFOS_LOCALES` con los 9 grafos en ambos `*.env.example` y en producción.

## 3. Estado del sistema que la documentación refleja ahora

9 agentes A2A (incl. **meteo_mcp** con MCP Meteosource + respaldo Open-Meteo), coordinador supervisor
con **PostgresSaver** durable (fallback a InMemorySaver), RAG de Reiki en **Redis cloud**, recepción
personalizada, guardrails anti-ofuscación, gateway FastAPI único acceso, servicios systemd `t2c2-*`.

## 4. Estado

- ✅ README, AGENTS, ARQUITECTURA, ADR-0001, MEJORAS_FUTURAS, deploy (README-T2, CHECKLIST,
  t2c2.env.example) y `.env.example` **coherentes y al día** para la revisión académica. Bitácora
  **065**, evidencia **Anexo 16**.
