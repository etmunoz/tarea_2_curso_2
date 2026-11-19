<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_036.md`  
> **Objetivo:** 036 · Respuesta — seguimiento determinista + memoria de corto plazo durable  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1015 · **Última modificación:** 20261119 1015
<!--/encabezado-grupo-->

# 036 · Respuesta — Seguimiento durable

**Prompt:** [`../prompts_ejecutados/prompt_036.md`](../prompts_ejecutados/prompt_036.md)

---

## 1. Qué se hizo

- **Fallo 4 determinista:** `enrutar` mantiene el agente del turno anterior ante seguimientos cortos
  («¿y en Santiago?»), sin depender de que el LLM lo infiera.
- **Memoria de corto plazo DURABLE:** el agente previo se lee de `memoria` SQLite
  (`ultimo_agente(hilo)`) y el gateway lo pasa al estado (`agente_previo`). Sobrevive reinicios, a
  diferencia del `InMemorySaver`. Respaldo: inferirlo de los mensajes del hilo.
- **Tests:** +1 (`test_ultimo_agente_memoria_durable`) → **12 passed** en `test_tarea2.py`.

## 2. Verificación del fallo 4 (en vivo, antes del cambio durable)

- «voy a viajar a Lima, ¿qué moneda?» → **Viajes**; «¿y en Santiago?» → **Viajes** (CLP);
  «¿y el clima allá?» → **Viajes**. El seguimiento ya se mantiene en el agente correcto.

## 3. Decisión documentada: NO `SqliteSaver` / NO subir langgraph

Esta decisión quedó formalizada en un **ADR**:
[`../docs/decisiones/ADR-0001-memoria-corto-plazo.md`](../docs/decisiones/ADR-0001-memoria-corto-plazo.md).
- `SqliteSaver` requiere `langgraph-checkpoint-sqlite`, **incompatible** con langgraph 1.2 (pinnea
  checkpoint 2.x vs nuestra 4.3.1). El intento **degradó** `langgraph-checkpoint`; se **revirtió** a
  4.3.1 y se verificó el runtime sano (`/salud` 200). Evidencia: `evidencias/EVIDENCIAS.md` (Anexo 9).
- **No** se sube langgraph a 2.x (tocaría todo el runtime A2A). Backlog: `docs/MEJORAS_FUTURAS.md` §3.
- **Qué usamos:** `InMemorySaver` (estado intra-proceso) + store `memoria` SQLite (`agente_previo`) para
  el seguimiento durable.

## 4. Verificación de durabilidad (en vivo)

- Turno 1 → **Agente de Viajes**; `ultimo_agente("ezequiel:durab1")` = **"Agente de Viajes"** (leído del
  **SQLite en disco**); «¿y en Santiago?» → **Viajes**. El origen en disco ⇒ sobrevive reinicios.

## 5. Estado

- ✅ Fallo 4 robusto + memoria de corto plazo **durable** y **verificada**; decisión formalizada en
  **ADR-0001**; revert de langgraph verificado. Bitácora **036**.
