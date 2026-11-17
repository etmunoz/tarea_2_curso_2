<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_004.md`  
> **Objetivo:** 004 · Gateway FastAPI protegido por API_KEY + memoria SQLite + coordinador all-local (.env.example)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1544 · **Última modificación:** 20261117 1544
<!--/encabezado-grupo-->

# 004 · Gateway FastAPI (API_KEY) + memoria SQLite + coordinador all-local

**Pedido del usuario (verbatim):**

> «dale con el registro 004»

(Continuación del plan: tras `agente_meteorologia` REAL (003), el núcleo de la **arquitectura §2** del
`prompt_000.md`.)

**Alcance:**
1. **`src/api` — Gateway FastAPI**, ÚNICO punto de entrada a los agentes, **protegido por `API_KEY`**
   (header `X-API-Key`; sin clave válida → **401**). Endpoints `GET /salud` (abierto), `GET /agentes`
   (catálogo; protegido), `POST /consulta` (ruteo + respuesta; protegido). Import **diferido** del grafo
   del coordinador (requiere `GOOGLE_API_KEY`), para que el proceso arranque sin Gemini.
2. **`src/memoria` — SQLite de largo plazo**: historial de conversación, **destinatarios autogestionados
   (allowlist, §7)** y bitácora de despachos.
3. **Coordinador all-local**: `.env.example` con `A2A_BASE=:2025` y `A2A_GRAFOS_LOCALES` = los 8 grafos,
   **sin `URLS_AGENTES`** (no hay compañeros remotos).

**Criterio de verificación:** probar en vivo lo que no necesita secretos (memoria SQLite y la validación
de `API_KEY`, ambos stdlib); FastAPI compila; la prueba end-to-end de `/consulta` queda pendiente de
`GOOGLE_API_KEY` + `uv sync`. **Dejar traza completa** en `prompt_`/`salida_`.

**Restricción:** publicar directo en la VPS (web6), sin tocar otros proyectos, sin iniciar servicios.
