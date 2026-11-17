<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_006.md`  
> **Objetivo:** 006 · Respuesta — Implementación 3 Etapa A (voz) construida y verificada (headless) sobre el BFF  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1608 · **Última modificación:** 20261117 1608
<!--/encabezado-grupo-->

# 006 · Respuesta — Implementación 3 · Etapa A (voz)

**Prompt:** [`../prompts_ejecutados/prompt_006.md`](../prompts_ejecutados/prompt_006.md)

> ⚠️ **Método:** publicado **directo en la VPS** (web6, `~/tarea_2_curso_2`). Este `.md` es la bitácora.

---

## 1. Qué se hizo

Se añadió al BFF (`src/canales/web.py`) una **segunda vista `/voz`** para la conversación por voz
(Etapa A). El servidor **no cambió su lógica**: la voz ocurre **en el navegador** (Web Speech API) y la
consulta viaja por el **mismo** `/api/consulta` (que reenvía a FastAPI con la API_KEY server-side). Se
agregó también un enlace a `/voz` desde el chat de texto.

### Flujo de la Etapa A
1. Botón de **micrófono** → **STT** (`SpeechRecognition`, `lang='es-CL'`, resultados en vivo).
2. La **transcripción** aparece en un campo **editable** (el usuario puede corregir antes de enviar).
3. Al enviar → `POST /api/consulta` (BFF → FastAPI con `X-API-Key` server-side) → respuesta.
4. **TTS** (`speechSynthesis`, voz en español) **lee la respuesta**; también se muestra en texto con la
   ruta/agente.
5. **Estados** visibles: `listo` / `escuchando…` / `pensando…` / `hablando…` / error.
6. **Fallback**: si el navegador no soporta `SpeechRecognition`, se deshabilita el micrófono con aviso y
   queda el teclado; el TTS igual lee la respuesta. Casilla para **silenciar** la lectura.

**Costo:** gratis, sin cuentas ni API keys (Web Speech API es del navegador).

## 2. Verificación (headless, en la VPS)

`/voz` servido por el BFF (con login):
```
GET /voz SIN login -> 401
GET /voz CON login -> 200
Piezas presentes en /voz:
  SpeechRecognition (STT) · speechSynthesis (TTS) · es-CL ·
  estados: escuchando… / pensando… / hablando… · Transcripción (editable) · api/consulta (vía BFF)
```
`py_compile` de `web.py`: **OK**. BFF levantado **solo para la prueba** y apagado.

> La prueba de **voz real** (hablar → transcribir → responder → leer) se hace en **Chrome/Edge** con
> micrófono: es la evidencia **audio/video** de la rúbrica. Requiere además `GOOGLE_API_KEY` para que los
> agentes respondan. No es verificable headless en el servidor (no hay navegador ni micrófono).

## 3. Etapas B y C (consignadas, no construidas)

- **Etapa B — Avatar 2D (condicional a que A funcione):** sobre la misma tubería, añadir solo la capa
  visual (avatar 2D animado mientras suena el TTS). Se abordará si A queda estable en el navegador.
- **Etapa C — Avatar realista con lip-sync (opcional, de pago):** HeyGen/D-ID/Simli vía SDK/WebRTC;
  key server-side y control de costos. No comprometida.

## 4. Caveats documentados (Etapa A)

- Soporte de `SpeechRecognition` principalmente en **Chrome/Edge**; en otros navegadores se usa el
  fallback de teclado (el TTS sí es más universal).
- El STT de Chrome usa un servicio en la nube → requiere **internet** y **permiso de micrófono**.
- Hay algo de **latencia** (STT + respuesta de los agentes + TTS).

## 5. Estado y pendientes

- ✅ Publicado directo en web6; servicios solo transitorios para la prueba; otros proyectos intactos.
- Pendiente para la demo end-to-end: **`GOOGLE_API_KEY`** (respuesta de agentes) y la **prueba en
  navegador** con micrófono (evidencia audio/video).

## 6. Próximos pasos sugeridos

1. **Units systemd `t2c2-*`** (langgraph :2025, api :8796, web :8797, monitor :8798) + guía de
   publicación con proxy, listos para activar con `administrator`.
2. **Prueba end-to-end** (texto y voz) cuando estén `GOOGLE_API_KEY` + swap; **envío real de correo** con
   las credenciales SMTP.
3. **Etapa B (avatar 2D)** si A queda estable en el navegador.
