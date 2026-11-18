<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_024.md`  
> **Objetivo:** 024 · Respuesta — RAG de Reiki migrado a Redis cloud (RediSearch), verificado en producción  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2250 · **Última modificación:** 20261117 2250
<!--/encabezado-grupo-->

# 024 · Respuesta — RAG de Reiki en Redis cloud

**Prompt:** [`../prompts_ejecutados/prompt_024.md`](../prompts_ejecutados/prompt_024.md)

---

## 1. Qué se hizo

1. **`src/agente_reiki/rag.py`** — resolución de configuración desde el almacén:
   - `_config_store()` lee `config.sqlite` (que `web6` escribe **sin sudo**).
   - `_es_placeholder()` ignora el `REDIS_URL` de ejemplo del EnvironmentFile
     (`redis://usuario:password@host:puerto/0`).
   - `REDIS_URL` = almacén → entorno (si no es placeholder) → `localhost`.
   - `BACKEND` = **redis** si hay una `REDIS_URL` real (o si `RAG_BACKEND=redis`); si no, local.
   - `REDIS_INDEX` = almacén → entorno → **`t2c2_duran_reyes_munoz_reiki`** (namespaceado al grupo).
2. **`src/config/ajustes.py`** — `PERMITIDAS` ahora incluye `REDIS_URL`, `RAG_BACKEND`, `REDIS_INDEX`.
3. **`deploy/set_redis_url.sh`** — guarda la `REDIS_URL` leyéndola **oculta** (sin eco, sin history, sin
   pasar por el chat). Se corre como `web6`:
   `sudo -u web6 bash …/tarea_2_curso_2/deploy/set_redis_url.sh`.
4. **Deploy** local → VPS (`deploy/deploy_local_a_vps.sh`) y **construcción del índice** en Redis.

## 2. Verificación (producción)

- **Conectividad:** `PING = True`. **RediSearch presente:** `FT._LIST` responde y `FT.INFO` existe
  (el `MODULE LIST` venía vacío por estar restringido en el Redis gestionado — no es indicador).
- **Índice construido:** `t2c2_duran_reyes_munoz_reiki`, **9 fragmentos**; `buscar()` devuelve
  `nivel-1-shoden.md`, `nivel-2-okuden.md`.
- **Backend en vivo:** tras `sudo systemctl restart t2c2-langgraph`, se **movió el artefacto local**
  (`logs/reiki_rag.json` → `.bak`) y la consulta ruteada al Agente de Reiki **igual respondió** con
  contenido correcto (Mikao Usui, Gokai, posiciones de manos) y
  `ruta: guardia_entrada → supervisor → agente_local → guardia_salida`. Al no existir el backend local,
  la respuesta **solo pudo venir de Redis** → migración confirmada.

## 3. Seguridad

- La `REDIS_URL` (con usuario/clave) **no aparece** en el repo, ni en el chat, ni en logs: vive solo en
  `config.sqlite` (gitignored, excluido del deploy). El script la lee con `read -rs` (oculta) y la pasa a
  Python por `stdin` (no por argv, no visible en `ps`).
- `GOOGLE_API_KEY` sigue solo en `/etc/t2c2.env`; para construir el índice se cargó en memoria desde ese
  archivo (legible por `web6`) **sin imprimirla**.

## 4. Estado

- ✅ RAG de Reiki sirviendo desde **Redis cloud** (RediSearch), verificado en producción.
- ✅ Config por almacén (sin sudo, sin `/etc`); índice namespaceado al grupo.
- ✅ Bitácora **000–024**; código desplegado y commiteado/pusheado.
