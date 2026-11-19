<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_036.md`  
> **Objetivo:** 036 · Fallo 4 robusto + memoria de corto plazo DURABLE del seguimiento  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1015 · **Última modificación:** 20261119 1015
<!--/encabezado-grupo-->

# 036 · Seguimiento determinista + memoria durable

**Pedido del usuario (verbatim):**

> «Ojo con la persistencia de la memoria de corto plazo eso es clave»
> «consulta, y subir de versión de langgraph?»
> «recuerda ir dejando todo esto en prompts, salidas y evidencias.»

**Contexto:** al verificar el fallo 4 en vivo, «¿y en Santiago?» seguía yendo a Meteorología aunque el
historial sí llegaba al supervisor (el LLM priorizaba la palabra «Santiago»). Además, el coordinador usa
`InMemorySaver`, que **pierde la memoria de corto plazo al reiniciar**.

**Alcance:**
1. **Fallo 4 determinista** (`src/coordinador/graph.py`): ante una pregunta de seguimiento corta
   (≤6 palabras, patrón «¿y …»), `enrutar` reusa el agente del turno anterior en vez de re-rutear por
   palabras sueltas.
2. **Memoria de corto plazo DURABLE:** el agente del turno anterior se lee del store `memoria` SQLite
   (`memoria.ultimo_agente(hilo)`), que **sobrevive reinicios**, y el gateway lo pasa al estado del grafo
   (`agente_previo`). Fallback: inferirlo de los mensajes del hilo en memoria.
   - `src/memoria/bd.py`: `ultimo_agente(sesion)`.
   - `src/api/app.py`: lee `ultimo_agente(hilo)` y lo pasa en `invoke({... "agente_previo": ...})`.
   - `src/coordinador/graph.py`: `Estado.agente_previo`; `enrutar` lo usa (durable) con fallback.
3. **Tests**: `test_ultimo_agente_memoria_durable`.

**Decisión sobre langgraph (consulta del usuario):** NO subir langgraph solo por un checkpointer
persistente. `langgraph-checkpoint-sqlite` es incompatible con nuestro `langgraph` 1.x (pinnea checkpoint
2.x vs 4.3.1); un `uv pip install` degradó `langgraph-checkpoint` y se **revirtió de inmediato** a 4.3.1.
Subir a langgraph 2.x tocaría todo el runtime A2A → se deja como **backlog** (`docs/MEJORAS_FUTURAS.md`).
La vía elegida (store SQLite propio) da la durabilidad sin tocar dependencias.

**Restricción:** sin cambiar la versión de langgraph; sin romper el runtime (revert verificado:
`/salud` 200, import del coordinador OK con la key).
