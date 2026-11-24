<!--encabezado-grupo-->
> **Archivo:** `evidencias/voz/README.md`
> **Objetivo:** Evidencia de la interacción por VOZ con los agentes (video con audio)
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
<!--/encabezado-grupo-->

# Interacción por voz con los agentes — **LOCAL**, 2026-11-23

Video con audio de la **integración avanzada por voz** (Etapa A): se **habla** la consulta
(STT, Web Speech API `es-CL`), el supervisor rutea al agente y la respuesta **se lee en voz alta**
(TTS). Cumple lo que exige el enunciado (pág. 3): *«una imagen de la interfaz no prueba por sí sola
que se escuchó la respuesta»* — por eso es video con audio, no una captura.

**Archivo:** [`evidencia_agente_por_voz.mov`](evidencia_agente_por_voz.mov)

| Dato | Registro |
|---|---|
| **Entorno y fecha** | **LOCAL** (Mac), 2026-11-23. Chat `http://127.0.0.1:8797/` (login por sesión), voz integrada (🎤 dictar / 🔈 leer en voz). |
| **Solicitud** | Dos consultas **dictadas por voz**: (1) el **clima** de una ciudad y (2) los **cinco principios del Reiki**. |
| **Resultado esperado** | Que la voz se transcriba (STT), el supervisor rutee al agente correcto y la respuesta se **escuche** leída (TTS). |
| **Resultado obtenido** | El sistema transcribe el dictado, rutea por A2A (`guardia_entrada → supervisor → agente_local → guardia_salida`), responde con el agente correspondiente (clima → `meteo_mcp`/`meteorologia`; Reiki → `agente_reiki`, el Gokai) y **lee la respuesta en voz alta**. Se escucha en el audio del video. |
| **Observaciones** | Ejecución **LOCAL** (no producción). El clima mundial en local usa el respaldo Open-Meteo de `meteo_mcp`. El **envío por correo** no opera en el Mac (sin SMTP local); su funcionamiento real está evidenciado en el VPS (casos 11/11b, `evidencias/voz_correo/`). |

> Nota: el archivo `.mov` pesa ~81 MB. Está versionado en el repo y se incluye en el ZIP de entrega.
