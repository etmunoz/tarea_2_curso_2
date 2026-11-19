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

## 3. Sobre langgraph (consulta del usuario)

- `SqliteSaver` requiere `langgraph-checkpoint-sqlite`, **incompatible** con langgraph 1.x (pinnea
  checkpoint 2.x vs nuestra 4.3.1). El intento de instalarlo **degradó** `langgraph-checkpoint`; se
  **revirtió** a 4.3.1 y se verificó que el runtime quedó sano (`/salud` 200).
- **No** se sube langgraph (tocaría todo el runtime A2A). Queda como backlog
  (`docs/MEJORAS_FUTURAS.md` §3). La durabilidad se logró con el store propio.

## 4. Pendiente de activación

- `sudo systemctl restart t2c2-api` (coordinador). Verificación: seguimiento que **sobrevive a un
  reinicio** entre turnos (lee el agente del store).

## 5. Estado

- ✅ Fallo 4 robusto + memoria durable; revert de langgraph verificado. Bitácora **036**.
