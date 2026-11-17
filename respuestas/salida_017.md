<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_017.md`  
> **Objetivo:** 017 · Respuesta — historial persistente del chat y voz integrada en la misma página  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1954 · **Última modificación:** 20261117 1954
<!--/encabezado-grupo-->

# 017 · Historial persistente + voz integrada

**Prompt:** [`../prompts_ejecutados/prompt_017.md`](../prompts_ejecutados/prompt_017.md)

> ⚠️ **Método:** publicado en la VPS (web6). Se aplica al **reiniciar `t2c2-web`**.

---

## 1. Historial persistente (ya no se borra al volver)

Se re-incorporó la persistencia de la conversación (como en el T1), en `src/canales/web.py` (PAGINA):

- `historial` por conversación, guardado en `sessionStorage` (`t2_hist_<thread>`) en cada turno.
- **`restaurarHist()`** al cargar la página: re-dibuja las burbujas (usuario/bot) y re-pinta el **último
  ruteo**. "🔄 Nueva conversación" limpia el historial e inicia un hilo nuevo.

## 2. Voz integrada en la MISMA página

En vez de navegar a `/voz`, el micrófono vive **en el chat**:

- **Botón 🎤** en la caja de texto: dicta al input con **STT** (Web Speech API, `es-CL`, resultados en
  vivo); se puede **corregir** antes de enviar. Si el navegador no soporta STT, el botón se oculta.
- **Toggle 🔊/🔈** en la cabecera: cuando está activo, **lee en voz** cada respuesta (TTS). Persistente.
- Se quitó el enlace del chat a `/voz`. La página `/voz` sigue servida (evidencia de la Etapa A), pero
  el flujo principal es el chat integrado — más claro y sin perder el contexto al navegar.

`web.py` **compila**.

## 3. Verificación (tras reiniciar `t2c2-web`)

```bash
sudo systemctl restart t2c2-web
```
→ Se comprobará que la página sirve con el micrófono integrado, el toggle de voz y la restauración del
historial.

## 4. Estado

- ✅ Código publicado en web6; compila. Bitácora **000–017** en el repo.
- ⏳ Pendiente: reinicio de `t2c2-web` (sudo) + prueba en el navegador.
