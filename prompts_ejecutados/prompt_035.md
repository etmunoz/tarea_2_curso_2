<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_035.md`  
> **Objetivo:** 035 · Resolver los fallos pendientes 2, 4 y 7 (tras mergear la rama de Fabio)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 0920 · **Última modificación:** 20261119 0920
<!--/encabezado-grupo-->

# 035 · Fallos 2, 4 y 7 resueltos

**Pedido del usuario (verbatim):**

> «ok. avanza con el merge y luego seguimos de inmediato con las mejoras que se tienen que abordar»

**Contexto:** merge de `fix/fallos-pruebas-sitio` hecho (fallos 1/3/5/6). Quedaban 3 propuestas
pendientes en `fallos.md` (2, 4, 7); se implementan aquí.

**Alcance:**
1. **Fallo 2 · Guardia de entrada** (`src/coordinador/guardrails.py`): se evalúa el texto y su versión
   **de-leet** (`maketrans("013457","oieast")`); `_RE_INYECCION` suma patrones en inglés
   (`ignore|disregard|forget … previous|prior instructions|rules|prompts`) y de exfiltración de
   secretos/variables de entorno. `es_instruccion_remota` también usa el chequeo de-leet.
2. **Fallo 4 · Seguimiento** (`src/coordinador/graph.py` + `prompts.py`): `enrutar` pasa los últimos
   turnos en `<historial>…</historial>` (como dato) y `SYSTEM_SUPERVISOR` mantiene el agente del turno
   anterior ante preguntas cortas de seguimiento.
3. **Fallo 7 · Lugares ficticios** (`src/agente_viajes/prompts.py`): el agente confirma cuando el lugar
   encontrado no calza con lo pedido.
4. **Tests** (`tests/test_guardrails.py`): leetspeak/inglés bloqueados y texto normal con dígitos no.
5. **`fallos.md`**: 2/4/7 marcados como resueltos.

**Restricción:** el de-leet no debe generar falsos positivos en texto normal con números (verificado con
test). Fallos 4 y 7 se verifican en vivo (dependen del LLM).
