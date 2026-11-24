<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_073.md`
> **Objetivo:** 073 · Respuesta — merge del PR de Fabio (fix día de la semana) + deploy
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
> **Creación:** 20261124 1720 · **Última modificación:** 20261124 1720
<!--/encabezado-grupo-->

# 073 · Fix del día de la semana (PR de Fabio) — revisado, mergeado y desplegado

**Prompt:** [`../prompts_ejecutados/prompt_073.md`](../prompts_ejecutados/prompt_073.md)

> ⚠️ **ESTE ARREGLO ES POSTERIOR A LA ENTREGA.** La entrega ya estaba **congelada** (ZIP descargado del
> repo + rama `main` **bloqueada**). Este fix (día de la semana) se revisó, mergeó y desplegó **después**
> de la entrega, y se deja registrado aquí solo por **trazabilidad y transparencia**. **No forma parte
> del ZIP entregado.** Tras aplicarlo, `main` se vuelve a bloquear.

---

## 1. El fix (qué estaba mal y cómo se corrigió)

**Problema:** el **nombre del día de la semana** lo deducía el LLM y a veces erraba (intermitente):
p. ej. «Lunes, 24 de noviembre de 2026» cuando el 24-11-2026 es **martes**.

**Corrección (de Fabio):** el día se calcula en **código**, no en el LLM:
- `src/agente_meteorologia/openmeteo.py` → nuevo `dia_semana(fecha)` (`date.fromisoformat(f).weekday()`
  → nombre en español). Se agrega el campo **`dia`** a cada día de `pronostico()` y `observado()`.
- `src/agente_meteorologia/herramientas.py` → `pronostico_hoy` devuelve `dia`.
- `src/agente_meteorologia/prompts.py` → el prompt obliga: *«El día de la semana es el campo `dia`…
  úsalo tal cual y nunca lo calcules tú».*
- `src/agente_meteo_mcp/herramientas.py` → el respaldo Open-Meteo antepone `dia_semana(fecha)` a cada día.

## 2. Revisión del PR

- **Código:** correcto y acotado (cálculo determinista del día + instrucción en el prompt). ✅
- **Tests:** corrí la suite de la rama varias veces → **201 passed, 13 skipped**. El único rojo es
  `test_swarm::test_swarm_incluye_actividades` (importa `src.swarm`, inexistente) — **pre-existente**,
  falla igual en `main` y está detrás de `skipif GOOGLE_API_KEY`; **no es de este PR**. Sin regresiones
  (una falla puntual de `rag_reiki` fue flakiness del `.env` local con Redis real; en reintentos pasa).
- **QA del sitio** (`tools/qa_entrega.py`): 95/96 en vivo + E2E 5/5; el único fail es la falta de CSP
  (no exigida por el enunciado). Hallazgos menores (confirmación «Narnia», ML-Bio, administrador,
  saludo) quedan de **backlog**, no bloquean.

## 3. Merge + deploy

- **Merge** `fix/dia-semana-tests` → `main` (`--no-ff`), sin conflictos. `main` se **desbloqueó** para
  esto y se **vuelve a bloquear** al final.
- **Deploy al VPS** con el código del fix (el DNS del Mac no resolvía `etmk.cl`; se desplegó por IP,
  `69.197.134.192`). Verificado: `dia_semana` presente en `openmeteo.py` del VPS.
- **Reinicio** de `t2c2-langgraph` + `t2c2-fichas` (los agentes) para tomar el fix — lo hace el
  administrador con sudo.

## 4. Verificación en vivo (hecha)

Tras reiniciar `t2c2-langgraph` + `t2c2-fichas` (ambos `active`):
- **Determinista:** `dia_semana` → 2026-11-23 **lunes**, 24 **martes**, 25 **miércoles**, 26 **jueves**. ✓
- **End-to-end (gateway del VPS):** «pronóstico de 7 días en Santiago» → Agente de Meteorología, con
  los nombres de día **ya correctos**: `martes 2026-11-24`, `miércoles 25`, `jueves 26`, `viernes 27`,
  `sábado 28`, `domingo 29` (hoy, 24-11-2026, es martes). El bug intermitente **quedó corregido**.
- `meteo_mcp` usa la misma `openmeteo.dia_semana`, por lo que su respaldo también sale correcto.

## 5. Estado

- ✅ PR revisado (sin regresiones, 201 passed), **mergeado a `main`**, **desplegado al VPS**, reiniciado
  y **verificado en vivo** (día de la semana correcto). `main` se vuelve a **bloquear** para congelar la
  entrega. Bitácora **073**.
