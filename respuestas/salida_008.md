<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_008.md`  
> **Objetivo:** 008 · Respuesta — monitor repropuesto (:8798) + logging de accesos, probado en vivo (200/401)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1629 · **Última modificación:** 20261117 1629
<!--/encabezado-grupo-->

# 008 · Respuesta — Monitor/backoffice repropuesto

**Prompt:** [`../prompts_ejecutados/prompt_008.md`](../prompts_ejecutados/prompt_008.md)

> ⚠️ **Método:** publicado **directo en la VPS** (web6). Este `.md` es la bitácora.

---

## 1. Qué se hizo

| Archivo | Cambio |
|---|---|
| `src/memoria/bd.py` | Nueva tabla **`accesos`** + `registrar_acceso`, `accesos`, `resumen_accesos`, y `historial_reciente` (para el monitor). |
| `src/api/app.py` | **Middleware `_log_acceso`**: registra cada llamada al gateway (ruta, método, status, si traía `X-API-Key`) en la memoria. **No guarda la clave.** |
| `src/canales/monitor.py` | **Backoffice** (stdlib `http.server`, login Basic Auth) con: tarjetas de resumen (accesos / permitidos / rechazados / destinatarios), tabla de **accesos** recientes, **despachos**, **allowlist** e **historial**. |
| `deploy/systemd/t2c2-monitor.service` | Unit del monitor (`:8798`, `User=web6`). |
| `deploy/t2c2.env.example` | + `MONITOR_HOST/PORT/USER/PASS`. |

**Repropósito:** el monitor del T1 trazaba el puente A2A (compañeros); en T2 no hay puente, así que se
reorienta a **operación/seguridad**. Los **baneos de fail2ban** se gestionan a nivel de servidor
(requiere administrador) y quedan como hook aparte (documentado en la página).

## 2. Prueba en vivo (FastAPI + monitor, sin Gemini)

Se generaron accesos reales contra el gateway (con y sin `API_KEY`) y el monitor los reflejó:

```
monitor SIN login -> 401
monitor CON login -> 200
Resumen del monitor:  Accesos = 6 · Permitidos = 4 · Rechazados (401) = 2
Tabla de accesos:     4×<td>200</td> · 2×<td>401</td>
```
→ El **middleware** registra cada llamada; el **monitor** muestra el **200/401** real (evidencia de
acceso permitido/rechazado), además de despachos, allowlist e historial.

> **Nota técnica:** el monitor se ejecuta como script; se añadió un bootstrap de `sys.path` para poder
> importar `src.memoria` tanto por `python src/canales/monitor.py` como por el servicio.

`py_compile` de `bd.py` y `monitor.py`: **OK**. `app.py`: sintaxis OK. `systemd-analyze verify` del unit:
sin errores. Servicios **apagados** tras la prueba.

## 3. Estado y pendientes

- ✅ Publicado en web6; otros proyectos intactos; nada quedó corriendo.
- **Activación** (sudo): el unit `t2c2-monitor` se instala/activa igual que los demás (ver
  `deploy/README-T2.md`), y se publica por `monitortarea2curso2.etmk.cl` con proxy a `:8798`.
- **fail2ban** en el monitor: pendiente de exponer una fuente legible sin root (hook de administrador).

## 4. Dónde quedó el proyecto

Las **3 implementaciones** y el soporte están construidos y, donde fue posible, **probados en vivo**:
agentes locales + administrador, meteorología real, **gateway FastAPI con API_KEY (200/401)**, memoria
SQLite, **web chat + voz**, **correo** (compone/allowlist/gráfico), **5 units systemd** (langgraph,
fichas, api, web, monitor) + guía de publicación, y **monitor** de operación.

**Falta solo lo que depende de secretos/sudo del usuario** para la demo end-to-end:
- **`GOOGLE_API_KEY`** → respuestas reales de los agentes (texto y voz).
- **Credenciales SMTP** → envío real de correo.
- **swap** + activar los servicios con `administrator` + publicar los subdominios con proxy.

## 5. Próximos pasos sugeridos

1. (Usuario) Poner secretos en `/etc/t2c2.env` + swap + activar servicios (guía en `deploy/README-T2.md`).
2. **Prueba end-to-end** con evidencias (tablas del §10 del prompt_000) para la rúbrica.
3. Opcional: **RAG → Redis cloud** cuando llegue la URL; **Etapa B** (avatar 2D) si la voz queda estable.
