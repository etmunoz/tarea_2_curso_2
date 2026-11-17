<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_007.md`  
> **Objetivo:** 007 · Respuesta — units systemd t2c2-* + EnvironmentFile + guía de publicación (listos para administrator)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1624 · **Última modificación:** 20261117 1624
<!--/encabezado-grupo-->

# 007 · Respuesta — Servicios systemd t2c2-* + guía de publicación

**Prompt:** [`../prompts_ejecutados/prompt_007.md`](../prompts_ejecutados/prompt_007.md)

> ⚠️ **Método:** publicado **directo en la VPS** (web6, `~/tarea_2_curso_2/deploy/`). Este `.md` es la
> bitácora. Los archivos quedan **listos**; la activación la hace el usuario con `administrator` (sudo).

---

## 1. Qué se hizo

Se limpió el `deploy/` (traía units `agente-*` del T1) y se crearon los artefactos de despliegue de T2:

| Archivo | Rol |
|---|---|
| `deploy/systemd/t2c2-langgraph.service` | `langgraph dev` con los 8 agentes locales, `127.0.0.1:2025`. |
| `deploy/systemd/t2c2-fichas.service` | Vigilante `configurar_fichas.py --vigilar` (re-aplica agent cards; espera a `:2025/ok`). |
| `deploy/systemd/t2c2-api.service` | Gateway FastAPI (`uvicorn src.api.app:app`), `127.0.0.1:8796`. |
| `deploy/systemd/t2c2-web.service` | Frontend BFF (`src/canales/web.py`), `127.0.0.1:8797`. |
| `deploy/t2c2.env.example` | Plantilla de `/etc/t2c2.env` (secretos ficticios). |
| `deploy/README-T2.md` | Guía de instalación, arranque, verificación y **publicación con proxy**. |

**Características de los units:** `User=web6 Group=client1` (aislado de web1/web5), `HOME`/`PATH`
absolutos de web6, `WorkingDirectory` del repo, `ExecStart` con la **ruta absoluta de `uv`**,
`EnvironmentFile=/etc/t2c2.env`, `Restart=always`, orden de dependencias (api/fichas/web tras langgraph).

## 2. Validación

`systemd-analyze verify` de los 4 units: **sin errores de sintaxis** (solo avisos benignos por el
`EnvironmentFile` aún inexistente y `[Install]`, esperables fuera de instalación).

## 3. Cómo se activa (resumen; detalle en `deploy/README-T2.md`)

Como `administrator` (sudo):
1. `cp deploy/t2c2.env.example /etc/t2c2.env`, completar secretos, `chown root:web6` + `chmod 640`.
2. `cp deploy/systemd/t2c2-*.service /etc/systemd/system/` + `systemctl daemon-reload`.
3. `systemctl enable --now` en orden: `t2c2-langgraph` → `t2c2-fichas` → `t2c2-api` → `t2c2-web`.
4. Verificar: `/salud` 200; `/agentes` 401 sin clave / 200 con `X-API-Key`.

**Publicación (ISPConfig, con proxy, SIN DNS):** Website para `tarea2curso2.etmk.cl` → Redirect proxy a
`http://127.0.0.1:8797/` → SSL + Let's Encrypt → **force-HTTPS antes del proxy** (bloque RewriteCond).
Los agentes (:2025) y el gateway (:8796) **no** se publican.

## 4. Estado y pendientes

- ✅ Archivos de despliegue listos en `deploy/`. **No se instaló/activó nada** (sin sudo).
- ⏸️ **Activación** (sudo): la hace el usuario con `administrator`, cuando estén los secretos.
- Pendientes de secretos del usuario: **`GOOGLE_API_KEY`**, **`API_KEY`**, **`WEB_USER/WEB_PASS`**,
  **`SMTP_*`**; y **swap** (sudo) antes de dejar todo permanente.
- **`t2c2-monitor` (:8798)**: pendiente de construir el **backoffice repropuesto** (fail2ban + accesos
  FastAPI + despachos + historial) — próximo registro.

## 5. Próximos pasos sugeridos

1. **Monitor repropuesto** (`t2c2-monitor`, :8798) + su unit.
2. Cuando el usuario ponga los secretos + swap: **activar los servicios** y hacer la **prueba
   end-to-end** (texto, voz y correo) con evidencias para la rúbrica.
