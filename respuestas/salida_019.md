<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_019.md`  
> **Objetivo:** 019 · Respuesta — render Markdown en el chat (negritas, listas, títulos, código)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2102 · **Última modificación:** 20261117 2102
<!--/encabezado-grupo-->

# 019 · Respuesta — Formateo Markdown

**Prompt:** [`../prompts_ejecutados/prompt_019.md`](../prompts_ejecutados/prompt_019.md)

> ⚠️ **Método:** publicado en la VPS (web6). Se aplica al **reiniciar `t2c2-web`**.

---

## 1. Qué se hizo

En `src/canales/web.py` (PAGINA, frontend) se agregó un **renderizador Markdown** ligero (sin librerías
externas), y las burbujas del bot ahora muestran **HTML formateado** en vez de texto plano:

- `mdToHtml(texto)` + `_mdInline`: convierte **`**negrita**`**, *`*itálica*`*, `` `código` ``,
  **listas** con `* `/`- `/`•` y **numeradas** (`1. `), **títulos** (`#`..`####`), párrafos y saltos de
  línea. Escapa HTML primero (seguridad).
- CSS para `.bub p/ul/ol/li/strong/em/código/hN` acorde al diseño.
- Se aplica solo a la **respuesta del agente**; el mensaje del usuario queda como texto.

`web.py` **compila**.

## 2. Resultado esperado

La respuesta "¿qué recetas tienes?" (que antes mostraba `* **Empanadas de pino**…` en crudo) ahora se ve
como una **lista con negritas**, limpia y legible.

## 3. Estado

- ✅ Código publicado en web6; compila.
- ⏳ Pendiente: reinicio de `t2c2-web` (sudo) + ver el chat con el formato aplicado.
