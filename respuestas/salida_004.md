<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_004.md`  
> **Objetivo:** 004 · Respuesta — Gateway FastAPI (API_KEY) + memoria SQLite + coordinador all-local, con pruebas stdlib en vivo  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1544 · **Última modificación:** 20261117 1544
<!--/encabezado-grupo-->

# 004 · Respuesta — Gateway FastAPI + memoria SQLite + coordinador all-local

**Prompt:** [`../prompts_ejecutados/prompt_004.md`](../prompts_ejecutados/prompt_004.md)

> ⚠️ **Método:** publicado **directo en la VPS** (web6, `~/tarea_2_curso_2`). Este `.md` es la bitácora.

---

## 1. `src/api` — Gateway FastAPI protegido por API_KEY (§2)

| Archivo | Rol |
|---|---|
| `claves.py` | `clave_valida(provista, esperada)` — comparación en tiempo constante (`hmac.compare_digest`); **solo stdlib** (testeable sin FastAPI). Vacío/None → `False` (no abre la puerta). |
| `seguridad.py` | Dependencia FastAPI `verificar_api_key` (header **`X-API-Key`** vs env `API_KEY`): inválida/ausente → **401**, sin revelar la clave. |
| `app.py` | App FastAPI. `GET /salud` (abierto), `GET /agentes` (catálogo desde `src/fichas.py`; **protegido**), `POST /consulta` (ruteo+respuesta; **protegido**). Import **diferido** del grafo del coordinador y de `HumanMessage` (requieren `GOOGLE_API_KEY`); registra la conversación en `src/memoria`. |

**Flujo `/consulta`:** valida API_KEY → guarda el mensaje del usuario → invoca el coordinador
(`graph.invoke({"messages":[HumanMessage(...)]}, {"configurable":{"thread_id": sesion}})`) → guarda la
respuesta → devuelve `{sesion, respuesta, elegido, origen, ruta}`.

## 2. `src/memoria` — SQLite de largo plazo (§6, §7)

`bd.py` (stdlib `sqlite3`), ruta por env `MEMORIA_DB` (def. `<repo>/logs/memoria.sqlite`). Tablas:

```sql
conversaciones(id, sesion, rol, contenido, agente, ts)
destinatarios(correo PK, nombre, activo, alta_ts)      -- allowlist autogestionada (§7)
despachos(id, destinatario, asunto, estado, ts)        -- bitácora de correos
```

Funciones: `guardar_mensaje`/`historial`; `registrar_destinatario` (idempotente)/`baja_destinatario`/
`listar_destinatarios`/`es_destinatario_permitido`; `registrar_despacho`/`despachos`. Correos
normalizados (minúsculas, sin espacios). Horas en `America/Santiago`.

## 3. Coordinador ALL-LOCAL — `.env.example`

Se creó `.env.example` (valores ficticios, se versiona la plantilla, nunca el `.env` real) con la
configuración all-local:

- `A2A_BASE=http://127.0.0.1:2025` · `A2A_GRAFOS_LOCALES` = **los 8 grafos** · **sin `URLS_AGENTES`**.
- `MODELO`, `GOOGLE_API_KEY`, `API_KEY` (gateway), `RAG_BACKEND=local` + `REDIS_URL` (placeholder para
  cuando llegue el Redis cloud), `SMTP_*`/`MAIL_FROM` del buzón `tarea2curso2@etmk.cl`.

No se cambió código del coordinador: ya lee `A2A_BASE`/`A2A_GRAFOS_LOCALES`/`URLS_AGENTES`; con esta
config rutea solo a los 8 agentes locales.

## 4. Pruebas REALES en vivo (en la VPS, stdlib, sin secretos)

**Memoria (SQLite):**
```
alta: {'correo': 'test@example.com', 'nombre': 'Tester', 'activo': 1, 'alta_ts': '2026-11-17T15:44:27-03:00'}
permitido (activo): True
despacho id: 1 ; despachos: [{'destinatario':'test@example.com','asunto':'Pronóstico','estado':'enviado',...}]
historial s1: [usuario 'hola', asistente 'hola, soy el administrador' (agente_administrador)]
baja: True ; permitido tras baja: False
```
→ Normalización de correo, allowlist, idempotencia, baja lógica, historial y despachos: **OK**.

**API_KEY (`claves.clave_valida`):**
```
match OK: True ; match bad: False ; sin provista: False ; sin esperada: False
```
→ Solo acepta coincidencia exacta; nunca abre con clave vacía: **OK**.

**Compilación:** `py_compile` de `src/api/*.py` y `src/memoria/*.py`: **OK** (FastAPI no se importa en la
prueba; se valida sintaxis).

## 5. Estado y cuidados

- ✅ Publicado directo en web6. **No se iniciaron servicios**; otros proyectos intactos; DB de prueba en
  `/tmp` y eliminada.
- La parte que **sí** depende de Gemini (`POST /consulta` end-to-end) queda construida y compilando,
  lista para probar cuando haya `GOOGLE_API_KEY`.

## 6. Pendientes

- **`GOOGLE_API_KEY`** en el `.env` de web6 → para `uv sync` + levantar `langgraph` (:2025) + probar
  `/salud`, `/agentes` y `/consulta` end-to-end.
- **Swap** (sudo) antes de dejar servicios corriendo.
- **Redis cloud**: cambiar `RAG_BACKEND=redis` + `REDIS_URL` cuando llegue la URL.

## 7. Próximos pasos sugeridos

1. **Canal web (Impl 2)**: frontend de chat (BFF que habla con FastAPI con la API_KEY server-side) +
   **despacho por correo** (usando `src/memoria` allowlist + formato HTML con ruta y gráfico del grafo).
2. **Impl 3 Etapa A**: voz (Web Speech API) sobre el gateway.
3. **Prueba end-to-end** + `uv sync` cuando estén la `GOOGLE_API_KEY` y el swap.
