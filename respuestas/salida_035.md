<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_035.md`  
> **Objetivo:** 035 · Respuesta — fallos 2, 4 y 7 resueltos  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 0920 · **Última modificación:** 20261119 0945
<!--/encabezado-grupo-->

# 035 · Respuesta — Fallos 2, 4 y 7

**Prompt:** [`../prompts_ejecutados/prompt_035.md`](../prompts_ejecutados/prompt_035.md)

## Contexto — datos de los fallos y de las pruebas

Origen: prueba del sitio desplegado por **Fabio** (2026-11-19, usuario `fabio`): **10 funcionales** +
**16 red-team** vía `POST /api/consulta`. Se detectaron **7 fallos** (ninguno crítico; los ataques
importantes fueron resistidos). Artefactos reproducibles reubicados a
[`../evidencias/fallos.md`](../evidencias/fallos.md) y
[`../evidencias/pruebas-prompts.md`](../evidencias/pruebas-prompts.md).

| # | Sev | Fallo | Resuelto en |
|---|---|---|---|
| 1 | Media | `1e308 CLP` rompía Viajes (`TypeError`) + mostraba error crudo | merge Fabio (034) |
| 2 | Media | Guardia ciega a leetspeak e inglés ampliado | **035** |
| 3 | Baja | Pregunta vacía llegaba al Administrador | merge Fabio (034) |
| 4 | Baja | Perdía contexto en seguimiento | **035** |
| 5 | Baja | Filtraba nombre interno («Agente Fabio»/«ProteinMAN») | merge Fabio (034) |
| 6 | Baja | Faltaban cabeceras de seguridad + versión del server | merge Fabio (034); HSTS → proxy |
| 7 | Baja | Ubicaba lugares ficticios sin avisar | **035** |

---

## 1. Qué se hizo (fallos 2, 4, 7)

| Fallo | Fix | Verificación |
|---|---|---|
| **2** · guardia ciega a leetspeak/inglés | `revisar_entrada` evalúa texto + de-leet; patrones EN ampliados + exfiltración | tests (leetspeak/inglés bloqueados; dígitos normales no) |
| **4** · pierde contexto en seguimiento | `enrutar` envía `<historial>` al supervisor; `SYSTEM_SUPERVISOR` mantiene el agente previo | en vivo |
| **7** · ubica lugares ficticios | prompt de viajes confirma cuando el lugar no calza | en vivo |

## 2. Merge previo (rama de Fabio)

`fix/fallos-pruebas-sitio` mergeada a `main` (`77c9ef6`) con los fallos **1/3/5/6** y el red-team.
24 tests verdes tras el merge.

## 3. Verificación (local)

- `pytest tests/test_guardrails.py` → **12 passed** (incluye leetspeak/inglés y el no-falso-positivo).
- Fallos 4 y 7 (dependen del LLM) → verificación en vivo tras reiniciar.

## 4. HSTS (fallo 6) — aplicado y verificado

El HSTS va en el **proxy inverso** (ISPConfig), no en el código. Se agregó
`Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"` en las Directivas de
Apache del website (documentado en [`../deploy/README-T2.md`](../deploy/README-T2.md)). **Verificado el
2026-11-19:** `curl -sI https://tarea2curso2.etmk.cl/login` →
`strict-transport-security: max-age=31536000; includeSubDomains`. Fallo 6 **cerrado al 100%**.

## 5. Estado

- ✅ Fallos 2/4/7 implementados; `evidencias/fallos.md` actualizado; artefactos reubicados a
  `evidencias/`. Bitácora **035**.
