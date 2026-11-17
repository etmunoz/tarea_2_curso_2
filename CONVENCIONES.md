<!--encabezado-grupo-->
> **Archivo:** `CONVENCIONES.md`  
> **Objetivo:** Convenciones de desarrollo de la Tarea 2 (encabezado de archivos + registro de prompts + commits)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1430 · **Última modificación:** 20261117 1430
<!--/encabezado-grupo-->

# Convenciones de desarrollo — Tarea 2

Heredadas del Taller 1 (`tarea_1_curso_2`) y adaptadas. **Todo en español (Chile)**; horarios en
`America/Santiago`.

## 1. Encabezado de archivos (obligatorio)

Todo archivo que generemos y que admita comentarios (`.py`, `.md`, `.html`, `.sh`, `.ps1`, `.toml`,
`.txt`, `.env.example`, `.gitignore`, `.ipynb`) lleva al inicio un encabezado con estos campos:

- **Archivo:** ruta del archivo en el repo.
- **Objetivo:** para qué sirve el archivo (una línea).
- **Grupo del curso:** `Fabio Durán - Gustavo Reyes - Ezequiel Muñoz`.
- **Creación:** fecha de creación en formato `yyyymmdd HHMM` (hora de Santiago).
- **Última modificación:** fecha de última modificación en formato `yyyymmdd HHMM` (hora de Santiago).

### Formato según el tipo de archivo

En archivos con comentarios de almohadilla (`.py`, `.toml`, `.txt`, `.sh`, `.ps1`, `.env.example`,
`.gitignore`):

```text
# --8<-- encabezado-grupo
# Archivo: <ruta>
# Objetivo: <una línea>
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: <yyyymmdd HHMM>
# Última modificación: <yyyymmdd HHMM>
# --8<-- fin-encabezado-grupo
```

En archivos Markdown/HTML (`.md`, `.html`) el encabezado es **visible** al renderizar: un blockquote
entre centinelas HTML invisibles `<!--encabezado-grupo-->` … `<!--/encabezado-grupo-->`:

```text
<!--encabezado-grupo-->
> **Archivo:** `<ruta>`  
> **Objetivo:** <una línea>  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** <yyyymmdd HHMM> · **Última modificación:** <yyyymmdd HHMM>
<!--/encabezado-grupo-->
```

En notebooks (`.ipynb`) ese mismo bloque va como primera celda Markdown. En archivos con frontmatter
YAML va DENTRO del frontmatter como comentarios `#`.

### Qué queda fuera

Los formatos que **no** admiten comentarios: `*.json` (`langgraph.json`, etc.), `uv.lock`
(autogenerado) y `.python-version` (solo la versión).

### Cómo se aplica

El encabezado se inserta y actualiza con `tools/aplicar_encabezados.py` (se portará del T1), que es
**idempotente**: conserva la fecha de **Creación** y solo refresca la de **Última modificación**.

```bash
uv run python tools/aplicar_encabezados.py           # aplica/actualiza en todo el repo
uv run python tools/aplicar_encabezados.py --check    # falla si algún archivo no tiene encabezado
```

## 2. Registro de prompts y salidas (obligatorio)

Cada prompt que ejecutamos se archiva, junto con su salida completa, con **numeración correlativa**:

- Prompt → `prompts_ejecutados/prompt_NNN.md`
- Salida → `respuestas/salida_NNN.md`

Reglas:

- **Mismo número** `NNN` para el prompt y su salida. La numeración **empieza en `000`** en este repo;
  `000` corresponde al **prompt inicial de arranque** (`prompt_000.md`) y su salida (`salida_000.md`).
- Ambos llevan el **encabezado de grupo** (bloque `<!--encabezado-grupo-->`).
- La **salida** guarda: enlace al prompt, **archivos tocados**, salida/resultado real, **estado** y
  **pendientes**. Debe ser **completa y fiel** (lo probado, lo pendiente y lo simulado, por separado).
- Si un prompt genera un PDF para compartir, se guarda junto al `.md` como `prompt_NNN.pdf`.

## 3. Commits y ramas

- **Commits en español**, mensaje claro (qué y por qué), terminando con la línea:
  `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **Push tras cada paso.** Rama principal: `main`.
- No se commitean secretos ni datos: `.env`, `.venv`, `logs/`, `*.sqlite`, `node_modules`, cachés y
  `.DS_Store` van en `.gitignore`.

## 4. Idioma, zona horaria y formato

- **Todo en español** (español de Chile): código visible, UI, mensajes de API/error, correos, docs y
  evidencias.
- **Zona horaria `America/Santiago`** en todo lo visible al usuario (el VPS corre en UTC → convertir al
  mostrar; los logs internos pueden ir en UTC pero rotulándolo).
- **Salidas bien formateadas** (Markdown/HTML con títulos, listas, tablas, énfasis y unidades CLP/°C),
  **sin alterar** cifras/unidades/condiciones (fidelidad).
