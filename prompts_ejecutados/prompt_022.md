<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_022.md`  
> **Objetivo:** 022 · Dejar el código de la app también en el repo (traerlo desde la VPS, sin secretos)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2207 · **Última modificación:** 20261117 2207
<!--/encabezado-grupo-->

# 022 · Código de la app al repo

**Pedido del usuario (verbatim):**

> «no veo el código de la app»
> «el código lo debemos dejar localmente también»

**Contexto:** por acuerdo inicial, el código se **publicó directo en la VPS** (web6) y el repo de GitHub
solo tenía la bitácora (`prompts_ejecutados/`, `respuestas/`), `CONVENCIONES.md`, `README`, el PDF. Ahora
se decide dejar el **código también en el repo** (local + GitHub) para la entrega y para los compañeros.

**Alcance:** sincronizar el código de la VPS (`~/tarea_2_curso_2/`) al repo, **excluyendo secretos y
basura** (`.env`, `*.sqlite`, `logs/`, `.venv/`, `__pycache__/`, `.langgraph_api/`, cachés y restos del
T1 como `.opencode/`, `.pytest_cache/`, `scripts/` mac/win), y commitear/pushear.

**Restricción:** no versionar ningún secreto (lo cubre `.gitignore`: `.env`, `*.sqlite`, `logs/`, etc.).
