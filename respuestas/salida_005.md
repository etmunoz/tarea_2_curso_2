<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_005.md`  
> **Objetivo:** 005 · Respuesta — Implementación 2 (web BFF + correo) construida y probada en vivo; evidencia de acceso 200/401  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1553 · **Última modificación:** 20261117 1553
<!--/encabezado-grupo-->

# 005 · Respuesta — Implementación 2: web de chat (BFF) + correo

**Prompt:** [`../prompts_ejecutados/prompt_005.md`](../prompts_ejecutados/prompt_005.md)

> ⚠️ **Método:** publicado **directo en la VPS** (web6, `~/tarea_2_curso_2`). Este `.md` es la bitácora.

---

## 1. Dependencias + `uv sync`

Se agregaron `fastapi>=0.110` y `uvicorn>=0.29` a `pyproject.toml` (el T1 usaba `http.server`) y se
corrió `uv sync`: fastapi 0.163.2, uvicorn 0.54.0, langgraph 1.2.20, langchain 1.4.9 (`.venv` 314 MB).

## 2. Evidencia de rúbrica — acceso al gateway (200/401), REAL

Gateway levantado (`uvicorn src.api.app:app` en `127.0.0.1:8796`, sin Gemini) con `API_KEY` de prueba:

```
/salud (abierto)            -> 200
/agentes SIN API_KEY        -> 401
/agentes API_KEY INVALIDA   -> 401
/agentes API_KEY VALIDA     -> 200   (8 agentes: machinelearning, mlbioinformatica, bioinformatica,
                                       reiki, cocinachilena, meteorologia, viajes, administrador)
```

→ **Acceso PERMITIDO y RECHAZADO demostrado** sin exponer la clave.

## 3. `src/canales` — Implementación 2

| Archivo | Rol |
|---|---|
| `web.py` | **Frontend web de chat (BFF)**, stdlib `http.server`. Login **Basic Auth** propio; reenvía a FastAPI agregando `X-API-Key` **server-side**. Rutas: `/` (UI de chat), `/api/consulta`, `/api/agentes`, `/api/salud`. |
| `correo.py` | **Despacho por correo** (SMTP 587 + STARTTLS). `componer()` → HTML + texto; `enviar()` → **solo a la allowlist** (`src/memoria`), registra el despacho, sin credenciales queda deshabilitado. Pie del correo: **ruta de los agentes** + **gráfico del grafo** (PNG por CID, Mermaid de respaldo). |
| `grafo_imagen.py` | `mermaid_coordinador()` (texto) y `png_coordinador()` (PNG cacheado vía `langchain_core` → mermaid.ink; None si no se puede). |

### Evidencia BFF (login + inyección de API_KEY)
```
GET /            SIN login   -> 401
GET /            CON login   -> 200   (sirve la UI de chat)
GET /api/agentes CON login   -> 200   (8 agentes vía BFF)
```
→ El navegador usa **solo su login**; **nunca** envía la API_KEY: la pone el BFF en el servidor.

### Evidencia correo (composición + allowlist, sin enviar)
```
a no registrado  -> {'ok': False, 'error': 'destinatario no está en la allowlist...'}
a registrado     -> {'ok': False, 'error': 'correo no configurado (faltan credenciales SMTP...)'}
HTML tiene Ruta: True | tiene Grafo: True | bytes: 1603
despachos: [dest@etmk.cl -> no_configurado ; nadie@x.com -> rechazado_allowlist]
```
→ **Nunca envía fuera de la allowlist**; registra cada intento; el HTML trae ruta y gráfico.

### Evidencia gráfico del grafo
```
PNG: .../logs/grafo_coordinador.png | existe: True | bytes: 23515
```
→ **PNG real** del flujo del coordinador (`guardia_entrada → enrutar → consultar|sin_agente →
guardia_salida`) renderizado por mermaid.ink y cacheado.

## 4. Estado y cuidados

- ✅ Publicado directo en web6. FastAPI y BFF se levantaron **solo para la prueba** y se **apagaron**;
  no queda nada corriendo. Otros proyectos intactos.
- ✅ `py_compile` de `src/canales/*` OK; pruebas stdlib en vivo OK; gateway real 200/401.

## 5. Pendientes

- **`/consulta` end-to-end** (web → FastAPI → coordinador → agentes): requiere **`GOOGLE_API_KEY`** y
  `langgraph` corriendo en `:2025`.
- **Envío real de correo**: requiere las **credenciales SMTP** del buzón `tarea2curso2@etmk.cl` (en el
  `.env`/EnvironmentFile del servicio).
- **Swap** (sudo) antes de dejar servicios permanentes; **units systemd `t2c2-*`** + publicación por
  subdominio con proxy (pendiente, requiere `administrator`).

## 6. Próximos pasos sugeridos

1. **Impl 3 — Etapa A (voz)**: Web Speech API (STT→FastAPI→TTS) sobre el BFF.
2. **Units systemd `t2c2-*`** (langgraph :2025, api :8796, web :8797, monitor :8798) + guía de
   publicación con proxy, listos para que el usuario los active con `administrator`.
3. **Prueba end-to-end** cuando estén `GOOGLE_API_KEY`, SMTP y swap.
