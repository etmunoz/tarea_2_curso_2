<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_069.md`
> **Objetivo:** 069 · Resultado de la prueba voz → chat → correo
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
> **Creación:** 20261123 1815 · **Última modificación:** 20261123 1815
<!--/encabezado-grupo-->

# 069 · Resultado

- Nuevo `tools/prueba_voz_correo.py` (solo stdlib): acceso rechazado (401 sin sesión, 401 con clave
  errónea), login 302, `POST /api/consulta`, registro en la allowlist y `POST /api/enviar`. Sin `--enviar` no despacha.
- Ejecución real en el VPS 2026-11-23 19:04: **6/6 OK**, Agente de Meteorología (Talca), correo
  `ok:true` a fabio@gnome.cl → `evidencias/voz_correo/resultado_20261123_190449.json`.
- Protocolo de grabación de la voz (STT/TTS del navegador) en `evidencias/voz_correo/README.md`, todavía pendiente de grabar.
- Contraste código ↔ web: el sitio coincide con `src/canales/web.py` (login por sesión, BFF, 🎤/🔈/✉️).
  Observaciones: `/api/correo` muestra la allowlist completa a cualquier usuario; cualquier usuario puede
  agregar destinatarios con `/api/registrar-correo`; el docstring de `web.py` todavía dice "Basic Auth";
  el correo deja el Markdown sin convertir.
