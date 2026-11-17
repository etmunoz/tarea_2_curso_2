<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_014.md`  
> **Objetivo:** 014 · Respuesta — documento de evidencias creado (tablas §10 + guía de capturas)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1928 · **Última modificación:** 20261117 1928
<!--/encabezado-grupo-->

# 014 · Respuesta — Evidencias

**Prompt:** [`../prompts_ejecutados/prompt_014.md`](../prompts_ejecutados/prompt_014.md)

> ⚠️ **Método:** publicado en la VPS (web6), en `evidencias/EVIDENCIAS.md`.

---

## 1. Qué se hizo

Se creó **`evidencias/EVIDENCIAS.md`** (86 líneas) con:

- **Entorno y reproducción:** VPS `server28` (web6), URLs públicas, cómo levantar en local (README) y la
  suite `pytest tests/test_tarea2.py` (8 passed).
- **Tabla de casos §10** (10 casos): Entorno/fecha, Solicitud, Resultado esperado, Resultado obtenido,
  Observaciones — cubriendo seguridad (200/401), Impl 1/A2A (meteorología real), ruteo al administrador,
  Impl 2 (chat HTTPS + correo), Impl 3 (voz), monitor, force-HTTPS y reproducibilidad.
- **Evidencia técnica** con las **salidas reales** capturadas en la sesión (curl 200/401, consultas
  reales con su ruta, correo `{'ok': True}`, publicación `http→301→https`, datos del panel del monitor).
- **Guía de capturas:** qué screenshots tomar (chat, voz audio/video, correo, 200/401 en el monitor,
  panel, candado HTTPS) y dónde guardarlos (`evidencias/`).

## 2. Qué queda del lado del usuario

- Tomar las **capturas/au­dio/video** indicados en la guía y guardarlos en `evidencias/`.
- (Opcional) Armar el **documento de entrega** final (`entrega/`) + `REPOS.txt` y empaquetar.

## 3. Estado

- ✅ Sistema en producción y verificado; **evidencias documentadas** con datos reales.
- ✅ Bitácora de prompts/salidas **000–014** completa; nada sin documentar.
