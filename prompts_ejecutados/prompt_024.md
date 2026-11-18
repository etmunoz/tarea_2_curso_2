<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_024.md`  
> **Objetivo:** 024 · Migrar el RAG de Reiki de backend local a Redis cloud (con RediSearch)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2250 · **Última modificación:** 20261117 2250
<!--/encabezado-grupo-->

# 024 · Migración del RAG de Reiki a Redis cloud

**Pedido del usuario (verbatim):**

> «actualicé el server redis»
> «no puedo ponerlo, pidemelo por pantalla y lo cambias tu»
> «guardado OK»

**Contexto:** el RAG de Reiki venía con backend **local** (`InMemoryVectorStore` persistido a
`logs/reiki_rag.json`). El usuario habilitó un **Redis cloud** (compartido del curso, con **RediSearch**)
y pidió migrar el RAG allí. Restricción clave: el usuario **no tiene sudo** para editar
`/etc/t2c2.env` (donde systemd define las variables), así que la `REDIS_URL` debía fijarse **sin tocar
`/etc`** y **sin que la clave quedara escrita en el chat**.

**Alcance:**
1. **`rag.py`**: resolver `REDIS_URL`, `BACKEND` y `REDIS_INDEX` desde el **almacén de config**
   (`config.sqlite`, que `web6` escribe sin sudo) cuando el entorno trae el *placeholder* del
   EnvironmentFile. Si hay una `REDIS_URL` real configurada, el backend pasa a **redis** automáticamente.
2. **`ajustes.py`**: agregar `REDIS_URL`, `RAG_BACKEND`, `REDIS_INDEX` a la allowlist `PERMITIDAS`.
3. **`deploy/set_redis_url.sh`**: script que lee la `REDIS_URL` de forma **oculta** (no se muestra, no
   queda en history ni en el chat) y la guarda en el almacén. Lo corre el usuario como `web6`.
4. **Índice namespaceado al grupo** (`t2c2_duran_reyes_munoz_reiki`) para no colisionar con los demás
   equipos que comparten ese Redis.
5. Construir el índice en Redis y **verificar en producción** (consulta ruteada al Agente de Reiki).

**Restricción de seguridad:** la `REDIS_URL` (con usuario/clave) **nunca** se escribe en el chat ni se
imprime; se entrega por un prompt oculto y se guarda en `config.sqlite` (fuera del repo, gitignored).
