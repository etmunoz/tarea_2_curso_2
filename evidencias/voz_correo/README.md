<!--encabezado-grupo-->
> **Archivo:** `evidencias/voz_correo/README.md`  
> **Objetivo:** Evidencia del recorrido voz → chat → respuesta hablada → correo (caso 11)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261123 1810 · **Última modificación:** 20261123 1810
<!--/encabezado-grupo-->

# Caso 11 · Hablo con el chat, me responde en voz y recibo la respuesta por correo

La evidencia tiene dos partes que se complementan:

| Parte | Qué demuestra | Cómo se obtiene | Estado |
|---|---|---|---|
| **A. Prueba automática E2E** | Acceso rechazado/permitido, ruteo del supervisor al agente, respuesta real, despacho SMTP | `tools/prueba_voz_correo.py` (mismo camino HTTP que usa el navegador) | ✅ **Ejecutada** 2026-11-23 19:04 |
| **B. Grabación de voz** | Que la pregunta se **dictó** (STT) y la respuesta **se escuchó** (TTS) en el navegador, y el envío con ✉️ | Video con audio (protocolo abajo) | ⏳ **Pendiente**: la graba una persona |

Lo dice el enunciado (p. 3): *«Una imagen de la interfaz no prueba por sí sola que se escuchó la
respuesta»*. Por eso la parte A no reemplaza a la B. La parte A no simula la voz: envía el texto ya
transcrito.

---

## A. Prueba automática E2E (ejecutada)

```bash
T2_CLAVE='***' python3 tools/prueba_voz_correo.py --usuario fabio \
  --pregunta "¿Cómo está el clima hoy en Talca?" --para fabio@gnome.cl --enviar
```

Sin `--enviar` no se manda correo, así no hay envíos por accidente. La clave se lee del entorno (o se pide
por teclado) y nunca queda en el repo ni en el JSON.

| Dato | Registro |
|---|---|
| **Entorno y fecha** | **REMOTO**: despliegue VPS `https://tarea2curso2.etmk.cl` (no LOCAL). 2026-11-23 19:04 (America/Santiago) |
| **Solicitud** | «¿Cómo está el clima hoy en Talca?», usuario `fabio`; despacho a `fabio@gnome.cl` |
| **Resultado esperado** | 401 sin sesión · 401 con clave errónea · 302 con clave correcta · supervisor → **Agente de Meteorología** con datos reales · correo `ok:true` |
| **Resultado obtenido** | Los 6 pasos OK ([`resultado_20261123_190449.json`](resultado_20261123_190449.json)). Ruta `guardia_entrada → supervisor → agente_local → guardia_salida`. Agente: **Agente de Meteorología** (5,4 s). Respuesta: 22,6 °C, mín 11,6 °C, máx 24,6 °C, llovizna débil, 0,3 mm. Correo aceptado por SMTP (`ok:true`) |
| **Observaciones** | `fabio@gnome.cl` no estaba en la allowlist y el script lo registró con `/api/registrar-correo`. Falta la captura del correo recibido en la bandeja (ver abajo) |

### A.2 · Caso 11b: pregunta bioinformática (proteína p53)

```bash
T2_CLAVE='***' python3 tools/prueba_voz_correo.py --usuario fabio \
  --pregunta "¿Qué función cumple la proteína p53 en humanos?" --para fabio@gnome.cl --enviar
```

| Dato | Registro |
|---|---|
| **Entorno y fecha** | **REMOTO**: despliegue VPS `https://tarea2curso2.etmk.cl` (no LOCAL). 2026-11-23 19:26 (America/Santiago) |
| **Solicitud** | «¿Qué función cumple la proteína p53 en humanos?», usuario `fabio`; despacho a `fabio@gnome.cl` |
| **Resultado esperado** | 401 · 401 · 302 · supervisor → **Agente de Bioinformática** con un dato real de UniProt · correo `ok:true` |
| **Resultado obtenido** | Los 5 pasos OK ([`resultado_20261123_192641.json`](resultado_20261123_192641.json)). Ruta `guardia_entrada → supervisor → agente_local → guardia_salida`. Agente: **Agente de Bioinformática** (7,5 s). La respuesta cita UniProt **P04637** (*Cellular tumor antigen p53*): factor de transcripción y supresor tumoral; detiene el ciclo celular, repara el ADN o induce apoptosis, y enlaza a uniprot.org. Correo aceptado por SMTP (`ok:true`) |
| **Observaciones** | El accession P04637 corresponde de verdad a la p53 humana, así que el dato viene de la herramienta y no es una invención del modelo. Esta vez no hubo paso de registro porque `fabio@gnome.cl` ya estaba en la allowlist desde el caso 11 |

---

## B. Protocolo de grabación (voz real)

**Requisitos:** Chrome o Edge (Firefox no trae `SpeechRecognition`), micrófono y parlantes activos.
Si se escucha por audífonos, el micrófono del celular no capta la respuesta; en ese caso grabar el
audio del sistema (opción 2).

1. Entrar a `https://tarea2curso2.etmk.cl/` con un usuario de prueba. La clave no debe aparecer en el
   video: iniciar sesión **antes** de empezar a grabar.
2. Empezar a grabar:
   - **Opción 1 (la más simple):** filmar la pantalla con el celular, que capta la voz y el parlante.
   - **Opción 2 (Linux/GNOME):** video con `Ctrl+Alt+Shift+R` (graba sin audio) y, en paralelo, el audio:
     ```bash
     pw-record mic.wav &                                         # tu voz
     pw-record -P '{ stream.capture.sink=true }' salida.wav &    # lo que dice el navegador
     # al terminar: kill %1 %2 y luego mezclar:
     ffmpeg -i ~/Videos/Screencasts/*.webm -i mic.wav -i salida.wav \
       -filter_complex "[1:a][2:a]amix=inputs=2[a]" -map 0:v -map "[a]" -c:v copy -c:a libopus voz_correo.webm
     ```
3. Mostrar la hora del sistema y decir en voz alta: *«Evidencia caso 11, fecha …»*.
4. Activar 🔈 (leer respuestas en voz), pulsar 🎤 y **decir**: *«¿Cómo está el clima hoy en Talca?»*.
5. Esperar la respuesta: tiene que **oírse** y verse en pantalla. Abrir **🧭 Ver ruteo** (se ve el agente elegido).
6. Pulsar **✉️ Enviar por correo** → *Para:* `fabio@gnome.cl` → **Enviar** → aparece «✅ Enviado».
7. Abrir la bandeja de `fabio@gnome.cl` y mostrar el correo: consulta, respuesta, ruta, agente y grafo.
8. **Caso 11b:** repetir los pasos 4 a 7 diciendo *«¿Qué función cumple la proteína p53 en humanos?»*.
   El ruteo tiene que mostrar el **Agente de Bioinformática**.
9. Detener la grabación y guardarla en esta carpeta como `voz_correo.webm` (o `.mp4`). Agregar
   `correo_recibido.png` y `correo_recibido_p53.png` con los correos, con los datos personales que no
   sean de prueba ocultos.

Ficha para completar después de grabar:

| Dato | Registro |
|---|---|
| **Entorno y fecha** | REMOTO (VPS) o LOCAL, según dónde se grabó · fecha y hora |
| **Solicitud** | Pregunta dictada por voz |
| **Resultado esperado** | Transcripción correcta → Agente de Meteorología → respuesta leída en voz → correo recibido |
| **Resultado obtenido** | *(completar: lo que se oyó, agente elegido, hora de llegada del correo)* |
| **Observaciones** | *(errores de transcripción, latencia, voz usada por el navegador)* |

## Límites conocidos

- STT y TTS son del **navegador** (Web Speech API). En Chrome, el dictado pasa por los servidores de
  Google y la voz que lee depende del sistema operativo.
- El correo muestra el Markdown de la respuesta sin convertir (por ejemplo `**Temperatura actual:**`),
  porque `correo.componer` solo escapa el HTML.
