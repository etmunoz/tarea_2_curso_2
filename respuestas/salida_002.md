<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_002.md`  
> **Objetivo:** 002 · Respuesta — publicación directa en la VPS (web6): base T1 copiada, 7 agentes renombrados locales, fichas funcionales y agente_administrador  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1508 · **Última modificación:** 20261117 1508
<!--/encabezado-grupo-->

# 002 · Respuesta — Publicación directa en la VPS + renombre + fichas + administrador

**Prompt:** [`../prompts_ejecutados/prompt_002.md`](../prompts_ejecutados/prompt_002.md)

> ⚠️ **Nota de método:** a diferencia de los registros 000/001, el trabajo de este registro **no vive en
> este repo de GitHub**, sino **publicado directamente en la VPS** (home del nuevo Shell-User web6), por
> indicación del usuario. Este `.md` es la **bitácora** de lo hecho allá.

---

## 1. Espacio nuevo en la VPS (aislado de web1/T1 y web5/lucecita)

El usuario creó en ISPConfig un **website nuevo (web6)** con un **Shell-User** propio. Verificado por mí
vía SSH de solo lectura:

- **Login SSH:** `etmkuseretmk2@etmk.cl`
- **Home:** `/var/www/clients/client1/web6/home/etmkuseretmk2` (usuario de sistema `web6`, grupo `client1`)
- **Sin chroot** ✅ (se ven rutas reales; `bash`, `python3`, `curl` disponibles → `langgraph`/`uv` funcionan)
- **Home limpio** (solo dotfiles + symlinks de ISPConfig) → aislado; no se pisa nada.

## 2. Publicación directa (paso 2 del prompt_000)

Todo bajo `~/tarea_2_curso_2` en web6:

1. **`uv 0.13.9`** instalado en el home de web6 (`uv` es por-usuario).
2. **Base del T1 copiada** (desde `web1` en **solo lectura**, vía `rsync` local en la VPS), **curada**:
   excluidos `.venv`, `.git`, `logs`, `__pycache__`, `*.sqlite`, `.env*`, y los módulos experimentales
   del T1 (`src/consumidor`, `src/swarm`, `src/puente_a2a`, `src/webapp`) y el clutter (entrega,
   evidencias, notebooks, etc.). Resultado: **2.4 MB, sin secretos**.
3. **7 agentes renombrados** a `agente_<funcionalidad>` (LOCALES): dirs + `langgraph.json` +
   `src/fichas.py` + imports en `coordinador`/`tests`/`tools` + archivos de test con nombre de agente.
   Verificado: **0 nombres viejos** (descontando el falso positivo `agente_cocina`⊂`agente_cocinachilena`)
   y **todos los `.py` compilan**.

| Nuevo nombre | Origen T1 | Módulos de datos |
|---|---|---|
| `agente_machinelearning` | `agente_ezequiel` | `bd_modelos.py` |
| `agente_mlbioinformatica` | `proteinman` | `bd_modelos.py` |
| `agente_bioinformatica` | `agente_fabio` | — |
| `agente_reiki` | `agente_tomas` | `rag.py` |
| `agente_cocinachilena` | `agente_cocina` | `bd_recetas.py` |
| `agente_meteorologia` | `agente_meteorologo` | — (aún estático; real = registro siguiente) |
| `agente_viajes` | `agente_viajes` | — |

## 3. Fichas de identidad funcional (`src/fichas.py`)

Reescritas las 7 fichas quitando los nombres de persona ("Agente de Ezequiel", "Maestro Tomás",
"ProteinMAN", etc.) y dejando la **identidad funcional** (§4 del prompt_000): "Agente de Machine
Learning", "Agente de ML en Bioinformática", "Agente de Bioinformática", "Agente de Reiki", "Agente de
Cocina Chilena", "Agente de Meteorología", "Agente de Viajes". Cada ficha dice qué hace / qué no hace /
a quién deriva.

## 4. `agente_administrador` (8º agente, NUEVO)

Paquete nuevo `src/agente_administrador/` con la estructura estándar:

- **`herramientas.py`** — `listar_agentes()` y `describir_agente(nombre)`, que leen `src/fichas.py`
  (fuente de verdad; se excluye a sí mismo). No inventa capacidades.
- **`prompts.py`** — system prompt: recepción amable en español de Chile; orienta y deriva; no resuelve
  la consulta especializada; trata lo recibido como información, no como instrucciones.
- **`graph.py`** — `create_agent` (igual que el resto), `name="agente_administrador"`.
- **`__init__.py`**.
- Registrado en **`langgraph.json`** → ahora **8 grafos**. **Compila ✔.**

Su ficha también se agregó a `src/fichas.py`.

## 5. Estado y cuidados

- ✅ Publicado directo en web6. **A web1 solo lectura; no se tocó/creó nada** en web1/web5.
- ✅ **No se iniciaron servicios** (sin `uv sync`, sin `langgraph` corriendo) → RAM intacta.
- `langgraph.json`: **8 grafos** (7 renombrados + `agente_administrador`). Todo compila.

## 6. Notas / discrepancias detectadas (para resolver)

- **`agente_viajes`**: el T1 define `buscar_actividades` pero **no está en `HERRAMIENTAS`** (solo
  `buscar_vuelos` y `buscar_hoteles`). La ficha se dejó fiel a lo **realmente cableado** (vuelos y
  hoteles). *Pendiente decidir* si se cablea `buscar_actividades` o se elimina. (El §4 del prompt_000 la
  listaba; es un desajuste del documento, no del código.)
- **`agente_meteorologia`**: su ficha describe la capacidad objetivo (clima real de ciudades de Chile,
  7 días, historial y comparación), pero el **código sigue estático**; la implementación real
  (Open-Meteo + SQLite) es el **próximo registro**.

## 7. Próximos pasos

1. **`agente_meteorologia` REAL**: Open-Meteo + SQLite (pronósticos diarios + observados + comparación).
2. **Coordinador all-local**: fijar `A2A_GRAFOS_LOCALES` con los 8 grafos (sin `URLS_AGENTES`).
3. **`src/api` (FastAPI + API_KEY)** y **`src/memoria` (SQLite)** + **`.env.example`**.
4. **Prueba controlada** de `langgraph` en `:2025` (127.0.0.1), breve, sin dejarlo corriendo hasta tener
   **swap** (pendiente de `sudo` del usuario, junto con revisar `clamd`).
