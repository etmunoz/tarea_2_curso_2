<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_009.md`  
> **Objetivo:** 009 · Respuesta — README de reproducibilidad + suite de pruebas T2 (8/8 en verde)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1811 · **Última modificación:** 20261117 1811
<!--/encabezado-grupo-->

# 009 · Respuesta — README + pruebas T2

**Prompt:** [`../prompts_ejecutados/prompt_009.md`](../prompts_ejecutados/prompt_009.md)

> ⚠️ **Método:** publicado **directo en la VPS** (web6). Este `.md` es la bitácora.

---

## 1. `README.md` del repo

Se reescribió el `README.md` (antes era el copiado del T1) con: descripción, **las 3
implementaciones**, diagrama de arquitectura, los **8 agentes**, memoria/monitor/RAG, **requisitos**
(Python 3.13 + uv + `.env`), **instalar / levantar / probar / detener** (local y referencia a los
servicios systemd), **seguridad** (API_KEY server-side, agentes solo 127.0.0.1, allowlist, guardrails,
secretos fuera del repo) y **límites**. 97 líneas.

## 2. `tests/test_tarea2.py` — suite sin secretos

Pruebas deterministas, **sin `GOOGLE_API_KEY` ni red**:

| Prueba | Qué valida |
|---|---|
| `test_api_key_clave_valida` | `clave_valida`: match, no-match, vacíos → nunca abre con clave vacía. |
| `test_memoria` | allowlist (alta/normalización/baja), despachos, historial, accesos + `resumen_accesos`. |
| `test_ciudades` | normalización sin tildes, coords conocidas/desconocidas, listado. |
| `test_wmo_condicion` | mapeo de códigos WMO → texto español (0, 95, None). |
| `test_bd_clima` | guardar/leer pronóstico y observado en SQLite. |
| `test_fichas_ocho_agentes` | `FICHAS` tiene 8 agentes con nombre y descripción. |
| `test_administrador_tools` | `listar_agentes` excluye al propio admin (7), `describir_agente` conocido/inexistente. |
| `test_correo` | `componer` trae ruta + grafo; `enviar` rechaza fuera de allowlist y sin SMTP. |

### Resultado
```
uv run --with pytest pytest tests/test_tarea2.py -q
........                                                                 [100%]
8 passed in 1.17s
```
→ **8/8 en verde.**

## 3. Estado y cuidados

- ✅ Publicado en web6; otros proyectos intactos; sin servicios dejados corriendo.
- La suite **no requiere secretos ni red**: el evaluador puede correrla tras `uv sync`.
- Las pruebas end-to-end con Gemini/SMTP siguen pendientes de los secretos del usuario (documentado).

## 4. Dónde quedó el proyecto

Construcción **completa de lo que no depende de secretos/sudo** y, donde fue posible, **probada en
vivo**. Quedan del lado del usuario, para la demo con evidencias:
- **`GOOGLE_API_KEY`** → respuestas reales de los agentes (texto y voz).
- **Credenciales SMTP** → envío real de correo.
- **swap** + **activar los servicios** (`deploy/README-T2.md`) + **publicar** los subdominios con proxy.

## 5. Próximos pasos sugeridos

1. (Usuario) Secretos en `/etc/t2c2.env` + swap + activar servicios.
2. **Prueba end-to-end** con captura de evidencias (tablas del §10 del prompt_000) para la entrega.
3. Opcional: **RAG → Redis cloud** cuando llegue la URL; **Etapa B** (avatar 2D).
