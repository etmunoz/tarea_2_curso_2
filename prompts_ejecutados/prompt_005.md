<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_005.md`  
> **Objetivo:** 005 · Implementación 2 — canal web de chat (BFF→FastAPI) + despacho por correo (HTML con ruta y gráfico del grafo)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1553 · **Última modificación:** 20261117 1553
<!--/encabezado-grupo-->

# 005 · Implementación 2 — web de chat (BFF) + correo

**Pedido del usuario (verbatim):**

> «dale con el registro 005»

(Continuación del plan: Implementación 2 del `prompt_000.md`.)

**Alcance:**
1. **Frontend web de chat como BFF** (`src/canales/web.py`): el navegador habla solo con este servidor
   (login propio), que **reenvía a FastAPI agregando la `API_KEY` server-side** → el browser nunca ve la
   clave (requisito §2).
2. **Despacho por correo** (`src/canales/correo.py`): HTML bien formateado + texto plano; **solo a
   destinatarios de la allowlist** (`src/memoria`); al pie, **(1) la ruta de los agentes** y **(2) el
   gráfico del grafo de LangGraph** (PNG embebido por CID, con Mermaid de respaldo). Nunca auto-envío.
3. Para poder **probar el gateway de verdad**: agregar `fastapi`/`uvicorn`, `uv sync`, y **demostrar el
   acceso 200/401** (evidencia de rúbrica; `/salud` y `/agentes` no requieren Gemini).

**Criterio de verificación:** probar en vivo todo lo que no necesita secretos (gateway 200/401, BFF con
login + inyección de API_KEY, composición de correo + allowlist, render del PNG del grafo). El envío
real de correo (SMTP) y `/consulta` end-to-end (Gemini) quedan pendientes de secretos.

**Restricción:** publicar directo en la VPS (web6); servicios solo de forma transitoria para la prueba
(apagados al terminar); sin tocar otros proyectos.
