<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_064.md`
> **Objetivo:** 064 · Respuesta — PostgresSaver en el coordinador (memoria durable con fallback)
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
> **Creación:** 20261123 1700 · **Última modificación:** 20261123 1715
<!--/encabezado-grupo-->

# 064 · Respuesta — PostgresSaver en el coordinador

**Prompt:** [`../prompts_ejecutados/prompt_064.md`](../prompts_ejecutados/prompt_064.md)

---

## 1. Qué se cambió

- **`src/coordinador/graph.py`** → nuevo `_checkpointer()`:
  - `PG_DSN` definido y Postgres alcanzable → `PostgresSaver` sobre `ConnectionPool(..., timeout=5)` +
    `.setup()` (crea las tablas, idempotente) → etiqueta `postgres`.
  - sin `PG_DSN`, o Postgres caído / credencial inválida → `InMemorySaver` → etiqueta `memoria`
    (**regla del grupo: ante cualquier fallo de Postgres, InMemorySaver**). El `except` evita que el
    gateway se caiga; `timeout=5` hace el fallback rápido.
  - `_construir_grafo()` compila con ese checkpointer y loguea la etiqueta.
- **`requirements.txt`** → `langgraph-checkpoint-postgres>=3.2,<4`.
- **`docs/decisiones/ADR-0001`** → actualizada: de "InMemorySaver + SQLite" a "PostgresSaver opcional
  (con fallback) + SQLite de respaldo del seguimiento".

El `agente_previo` del store SQLite se **mantiene** (defensa en profundidad del seguimiento).

## 2. Base de datos (VPS)

- PostgreSQL 16 ya estaba instalado y corriendo (no lo instaló una sesión con credenciales
  entregadas; se creó ahora el rol/base dedicados).
- Rol `t2c2` + base `t2c2` (owner `t2c2`) creados por el administrador con `sudo -u postgres psql`.
- `PG_DSN=postgresql://t2c2:***@localhost:5432/t2c2` → en `/etc/t2c2.env` (clave rotada por el
  usuario; **nunca** en el chat ni en el repo).

## 3. Verificación (VPS)

- **Dependencia:** `langgraph-checkpoint-postgres` instalada; `import langgraph.checkpoint.postgres,
  psycopg_pool, psycopg` → OK.
- **Round-trip real** contra la base `t2c2`: `.setup()` crea las tablas; `put()` + `get_tuple()`
  → `round-trip OK: True`, `filas en checkpoints: 1`; luego `delete_thread` de la prueba →
  `filas restantes: 0` (base limpia).
- **Selección del checkpointer** (import del coordinador con la key de Gemini):
  - con `PG_DSN` válido → `[coordinador] checkpointer: postgres` ✅
  - sin `PG_DSN` → `[coordinador] checkpointer: memoria` ✅
  - con `PG_DSN` de credencial inválida → `PG_DSN presente pero PostgresSaver no disponible
    (PoolTimeout): uso InMemorySaver.` + `checkpointer: memoria` ✅ (cumple la regla)
- **Tests locales (coordinador):** `tests/test_coordinador.py tests/test_guardrails.py
  tests/test_guardrails_auth_48.py` → **41 passed** (sin regresión; el import sin `PG_DSN` sigue
  usando InMemorySaver).

## 4. Activación en producción — CONFIRMADA

El administrador, en el VPS:
1. **Rotó la clave** del rol `t2c2` a una aleatoria generada en el propio servidor
   (`openssl rand`), sin que pase por el chat (`ALTER ROLE` → `ALTER ROLE`).
2. Escribió `PG_DSN=postgresql://t2c2:***@localhost:5432/t2c2` en `/etc/t2c2.env` (reemplazando la
   línea previa) y reinició `t2c2-api`.

**Verificación en vivo:**
- `curl POST /consulta` al gateway (`:8796`) → **http=200** (fuerza el import diferido del coordinador).
- Log del servicio:
  ```
  Nov 23 12:10:25 server28 uv[1051209]: [coordinador] checkpointer: postgres
  ```
  Es decir, el pool conectó y `setup()` corrió contra la base real `t2c2`. Si Postgres hubiera
  fallado, el log diría `PoolTimeout ... uso InMemorySaver` + `checkpointer: memoria`.
- Las líneas `status=143/n/a` + `Failed with result 'exit-code'` al parar el servicio son el
  `SIGTERM` normal del `restart` de uvicorn (128+15=143), no un error (tras ellas: `Application
  startup complete`).

> Nota operativa: el `print` del checkpointer aparece en la **primera `/consulta`** (el grafo del
> coordinador se importa de forma diferida en `src/api/app.py::_coordinador()`), no al arrancar el
> servicio.

Si en el futuro `PG_DSN` no estuviera o Postgres fallara, `t2c2-api` seguiría operativo con
`InMemorySaver` (sin cambios de comportamiento respecto de antes).

## 5. Estado

- ✅ PostgresSaver implementado con fallback a InMemorySaver, dependencia declarada, base/rol
  dedicados, round-trip verificado, **activado y confirmado en producción** (`checkpointer: postgres`),
  ADR-0001 al día. Bitácora **064**, evidencia **Anexo 15**.
