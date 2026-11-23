<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_064.md`
> **Objetivo:** 064 · Memoria durable del coordinador con PostgresSaver (opcional, con fallback a InMemorySaver)
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
> **Creación:** 20261123 1700 · **Última modificación:** 20261123 1700
<!--/encabezado-grupo-->

# 064 · PostgresSaver en el coordinador (memoria durable, con fallback)

**Pedido del usuario (verbatim):**

> «el memory saver, no debiésemos cambiarlo por algo similar para otros agentes, para que no pierda
> contexto?» … «tengo el posgresql levantado, lo hicimos en otra sesión tuya» … «genera con eso y
> cambio la clave cuando termines.» … «lo que si, como regla, si falla PostgresSaver debes usar
> InMemorySaver» … «si, todo registrado como prompt, luego su salida y al final evidencias como
> siempre.»

**Contexto:** el **coordinador** (supervisor que corre dentro de `t2c2-api`, NO bajo `langgraph dev`)
se compilaba con `InMemorySaver`: el estado del hilo vivía en RAM y se perdía en cada reinicio del
gateway (ver ADR-0001). El `agente_previo` del seguimiento ya era durable vía store SQLite, pero el
resto del estado no. El VPS ya tiene **PostgreSQL 16** corriendo y un dry-run confirmó que
`langgraph-checkpoint-postgres` 3.2.x es **compatible** con nuestro `langgraph-checkpoint` 4.3.1
(a diferencia del de SQLite, descartado en ADR-0001).

**Decisión de diseño:** usar `PostgresSaver` en el coordinador **cuando hay `PG_DSN`** y Postgres
responde; ante **cualquier** fallo (sin `PG_DSN`, caído, credencial mala) **caer a `InMemorySaver`**
(regla explícita del grupo). El `agente_previo` SQLite se mantiene como respaldo determinista.

**Alcance:**
1. `src/coordinador/graph.py`: `_checkpointer()` elige PostgresSaver / InMemorySaver (pool con
   `timeout=5` para que el fallback sea rápido; `.setup()` crea las tablas idempotentes). El compile
   del grafo usa ese checkpointer y loguea la etiqueta (`postgres` / `memoria`).
2. `requirements.txt`: `langgraph-checkpoint-postgres>=3.2,<4`.
3. VPS: rol `t2c2` + base `t2c2` dedicados; `PG_DSN` en `/etc/t2c2.env` (nunca en el chat/repo).
4. `docs/decisiones/ADR-0001`: actualizada (de "InMemorySaver + SQLite" a "PostgresSaver opcional").
5. Verificación en el VPS: round-trip real contra la base + las tres rutas de selección.

**Restricción de seguridad:** la clave de Postgres no pasa por el chat; se genera/rota en el VPS y se
escribe en `/etc/t2c2.env` con `sudo`. Para la verificación se usó la credencial solo en memoria (sin
persistirla) y el usuario rota la clave al final. PostgreSQL ya estaba instalado (no lo instaló ninguna
sesión con credenciales entregadas): rol y base se crean ahora, dedicados al proyecto.
