<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_011.md`  
> **Objetivo:** 011 · Respuesta — config web de secretos + aviso de cuota de Gemini; correo real enviado y recibido  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1852 · **Última modificación:** 20261117 1852
<!--/encabezado-grupo-->

# 011 · Respuesta — Config web de claves + aviso de cuota Gemini

**Prompt:** [`../prompts_ejecutados/prompt_011.md`](../prompts_ejecutados/prompt_011.md)

> ⚠️ **Método:** publicado **directo en la VPS** (web6). Este `.md` es la bitácora.

---

## 1. Verificaciones end-to-end de esta sesión

- **GOOGLE_API_KEY (del T1):** ✅ válida — Gemini respondió "¡Hola!" (`gemini-3.5-flash-lite`).
- **Correo real:** ✅ **enviado y recibido** en etmunoz@gmail.com (`{'ok': True}`) — asunto "Prueba
  Tarea 2 — sistema de agentes", con la **ruta de los agentes** y el **gráfico del grafo del
  coordinador** (PNG) al pie. Llegó al **Inbox**. (La clave SMTP la corrigió el usuario tras un primer
  `535 auth failed`.)

## 2. Ingreso de secretos por web (alternativo al `.env`)

| Archivo | Rol |
|---|---|
| `src/config/ajustes.py` | Almacén SQLite clave/valor (CONFIG_DB); solo claves permitidas (`GOOGLE_API_KEY`, `API_KEY`, `SMTP_PASS`); `set/get/todos/estados` (estados sin exponer valores). |
| `src/config/bootstrap.py` | Al importarse, vuelca los ajustes al entorno **solo si faltan** → el `.env`/EnvironmentFile **tiene prioridad**. |
| `src/canales/monitor.py` | Página **`/config`** (login): formulario para cargar las claves; muestra estado (en .env / por web / no definida). Avisa que al cambiar la clave hay que reiniciar `t2c2-langgraph` y `t2c2-api`. |
| Cableado | `from src.config import bootstrap` insertado en los **8 agentes + coordinador + gateway** (antes de instanciar el modelo). |

**Prueba:** `POST /config` con `google_api_key=…` → guardado en el almacén (`ajustes.get` lo devuelve);
`bootstrap` rellena el entorno si falta y **no pisa** si ya estaba (`.env` gana). 9 grafos cableados,
todo compila.

## 3. Aviso de cuota/tokens de Gemini

| Archivo | Rol |
|---|---|
| `src/config/estado.py` | `es_cuota(texto)` (detecta 429/`RESOURCE_EXHAUSTED`/quota/…); `set_gemini/gemini` guardan el estado con fecha. |
| `src/api/app.py` | `/consulta` envuelve la invocación: si es cuota → marca estado y responde **⚠️ "La clave de Gemini se quedó sin tokens o cuota…"** (se ve en chat y voz); en éxito marca OK. Nuevo `GET /estado`. |
| `src/canales/monitor.py` | **Banner** en el panel y en `/config`: `OK` / `cuota/tokens agotados desde <fecha>`. |

**Prueba:** `es_cuota("429 RESOURCE_EXHAUSTED quota")=True`, `es_cuota("timeout")=False`; el monitor
muestra "Clave Gemini: cuota/tokens agotados…". Compila.

## 4. Estado y pendientes

- ✅ Publicado en web6; servicios solo transitorios para las pruebas; otros proyectos intactos.
- **`/etc/t2c2.env` COMPLETO** (5 claves OK, incl. SMTP corregida). Gemini y correo verificados.
- ⏳ **Servicios aún `inactive`**: falta `systemctl enable --now t2c2-*` (sudo) — recomendado tras crear
  **swap**.
- ⏳ **Publicación con proxy** (ISPConfig) de `tarea2curso2.etmk.cl` (→ :8797) y
  `monitortarea2curso2.etmk.cl` (→ :8798), con Let's Encrypt + force-HTTPS.

## 5. Próximos pasos

1. (Usuario) **Swap** + `systemctl enable --now` de los 5 servicios (guía `deploy/README-T2.md` /
   `deploy/CHECKLIST-ACTIVACION.md`).
2. (Usuario) **Configurar los proxies** de los dos subdominios en ISPConfig.
3. **Prueba end-to-end por la web** (chat, voz, 200/401 en el monitor) con evidencias para la rúbrica.
