<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_016.md`  
> **Objetivo:** 016 · Traer las funcionalidades del chat del Taller 1 que faltaban (ruteo por turno, ver ruteo, enviar por correo)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1944 · **Última modificación:** 20261117 1944
<!--/encabezado-grupo-->

# 016 · Funcionalidades del chat (ruteo por turno + correo)

**Pedido del usuario (verbatim):**

> «nuevamente el mismo error que en la tarea 1, la ventana de la derecha va acumulando la ruta de toda
> la conversación. Revisa que es sólo de una, que se puede volver a ver, que se puede enviar por correo,
> todo eso estaba en la tarea 1, parece que te olvidaste de traer esas funcionalidades»
> «recuerda dejando todo en los prompts y las salidas, y las evidencias.»

**Alcance:**
1. **Ruteo por turno:** el panel de la derecha acumulaba la ruta de toda la conversación, porque el
   estado de LangGraph (checkpointer por `thread_id` + `ruta` con `operator.add`) **suma** los pasos
   turno a turno. Arreglo en el gateway: `POST /consulta` calcula la **ruta previa** (`get_state`) y
   devuelve **solo los pasos del turno actual** (`ruta[prev:]`).
2. **Ver ruteo:** el botón "🧭 Ver ruteo" de cada respuesta re-muestra el ruteo de ese turno (ya
   quedará correcto con #1).
3. **Enviar por correo:** se re-incorpora la función del T1 — modal de correo + botón "✉️ Enviar por
   correo" en cada respuesta, con endpoints nuevos en el gateway (`GET /destinatarios`, `GET /correo`,
   `POST /enviar`) y sus proxies en el BFF (`/api/destinatarios`, `/api/correo`, `/api/enviar`). El
   correo sale por el gateway (allowlist + ruta + gráfico del grafo).

**Restricción:** el reinicio de servicios lo hace el usuario (sudo); web6 no puede.
