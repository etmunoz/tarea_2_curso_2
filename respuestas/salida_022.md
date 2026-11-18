<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_022.md`  
> **Objetivo:** 022 · Respuesta — código de la app traído al repo (local + GitHub), sin secretos  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2207 · **Última modificación:** 20261117 2207
<!--/encabezado-grupo-->

# 022 · Respuesta — Código al repo

**Prompt:** [`../prompts_ejecutados/prompt_022.md`](../prompts_ejecutados/prompt_022.md)

---

## 1. Qué se hizo

Se sincronizó el código de la VPS (`etmkuseretmk2@etmk.cl:~/tarea_2_curso_2/`) al repo con `rsync`,
**sin `--delete`** (conserva la bitácora local) y excluyendo secretos/junk. **120 archivos** agregados;
**verificado: nada sensible** en el commit (ni `.env`, ni `*.sqlite`, ni `logs/`).

### Qué quedó en el repo ahora
```
src/            8 agentes + agente_administrador, coordinador/, api/ (FastAPI+API_KEY),
                canales/ (web BFF, voz, correo, monitor), memoria/ (SQLite),
                config/ (usuarios, ajustes, bootstrap, estado), fichas.py
deploy/         systemd/t2c2-*.service, t2c2.env.example, README-T2.md, CHECKLIST-ACTIVACION.md
tools/ tests/ data/ evidencias/
langgraph.json · pyproject.toml · requirements.txt · uv.lock · .python-version · .env.example · README.md
prompts_ejecutados/ · respuestas/ · CONVENCIONES.md   (bitácora, ya existentes)
```

### Qué quedó FUERA (por seguridad / no aplica)
- Secretos y datos: `.env` (está en `/etc/t2c2.env`), `*.sqlite`, `logs/`, `~/usuarios_setup.txt`.
- Runtime/caché: `.langgraph_api/`, `.pytest_cache/`, `.venv/`, `__pycache__/`.
- Restos del T1: `.opencode/`, `scripts/` (lanzadores mac/win del T1, no usados en T2).

## 2. Estado

- ✅ **Código en el repo** (local + GitHub, privado) y **también corriendo en la VPS**. Commit del
  código + este registro, pusheados a `main`.
- Los compañeros (Fabio, Gustavo) y los profes pueden `git clone` y ver todo el código.
- Bitácora **000–022** completa.

## 3. Nota

El `.gitignore` del repo cubre los secretos (`.env`, `*.sqlite`, `logs/`, `.venv`, `__pycache__`,
`.langgraph_api`), así que futuros `git add` no arrastran claves ni datos.
