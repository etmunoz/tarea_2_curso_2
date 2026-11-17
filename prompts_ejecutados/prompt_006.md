<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_006.md`  
> **Objetivo:** 006 · Implementación 3 · Etapa A — avatar conversacional por VOZ en el sitio (Web Speech API sobre el BFF)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1608 · **Última modificación:** 20261117 1608
<!--/encabezado-grupo-->

# 006 · Implementación 3 · Etapa A — Voz (Web Speech API)

**Pedido del usuario (verbatim):**

> «dale con el registro 006»

(Continuación del plan: Implementación 3, **Etapa A (base obligatoria)** del `prompt_000.md` §3.)

**Alcance:**
- **Conversación por VOZ en el propio sitio**: el usuario habla; el navegador transcribe (STT, Web
  Speech API `SpeechRecognition`, `es-CL`); el texto va a **FastAPI por el BFF** (API_KEY server-side);
  los agentes responden; el sitio **lee la respuesta en voz** (TTS, `speechSynthesis`).
- El usuario **no teclea**: lo transcribe el STT, pero la **transcripción es editable/confirmable**
  antes de enviar.
- UI con **botón de micrófono**, indicador animado y **estados** (escuchando / pensando / hablando);
  respuesta también en texto. **Fallback** a teclado si el navegador no soporta STT.
- Todo sobre el **mismo gateway** (`/api/consulta` del BFF); **gratis, sin cuentas ni API keys**.

**Etapas B (avatar 2D) y C (avatar realista):** se dejan **consignadas** y condicionales/opcionales (no
se construyen en este registro).

**Criterio de verificación:** servir `/voz` y comprobar (headless) que trae las piezas correctas
(STT/TTS, es-CL, estados, transcripción editable, reenvío por BFF). La prueba de **voz real** se hace en
Chrome/Edge con micrófono (evidencia audio/video) y requiere `GOOGLE_API_KEY` para la respuesta de los
agentes.

**Restricción:** publicar directo en la VPS (web6); BFF solo transitorio para la prueba; sin tocar otros
proyectos.
