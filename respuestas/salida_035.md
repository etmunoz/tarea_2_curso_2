<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_035.md`  
> **Objetivo:** 035 · Respuesta — fallos 2, 4 y 7 resueltos  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 0920 · **Última modificación:** 20261119 0920
<!--/encabezado-grupo-->

# 035 · Respuesta — Fallos 2, 4 y 7

**Prompt:** [`../prompts_ejecutados/prompt_035.md`](../prompts_ejecutados/prompt_035.md)

---

## 1. Qué se hizo

| Fallo | Fix | Verificación |
|---|---|---|
| **2** · guardia ciega a leetspeak/inglés | `revisar_entrada` evalúa texto + de-leet; patrones EN ampliados + exfiltración | tests (leetspeak/inglés bloqueados; dígitos normales no) |
| **4** · pierde contexto en seguimiento | `enrutar` envía `<historial>` al supervisor; `SYSTEM_SUPERVISOR` mantiene el agente previo | en vivo |
| **7** · ubica lugares ficticios | prompt de viajes confirma cuando el lugar no calza | en vivo |

## 2. Merge previo (rama de Fabio)

`fix/fallos-pruebas-sitio` mergeada a `main` (`77c9ef6`) con los fallos **1/3/5/6** y el red-team
(`fallos.md`, `pruebas-prompts.md`). 24 tests verdes tras el merge.

## 3. Verificación (local)

- `pytest tests/test_guardrails.py` → **12 passed** (incluye leetspeak/inglés y el no-falso-positivo).
- Fallos 4 y 7 (dependen del LLM) → verificación en vivo tras reiniciar.

## 4. Pendiente de activación

- `sudo systemctl restart t2c2-langgraph t2c2-api` (coordinador/guardrails viven en el gateway;
  prompts de agentes en langgraph).
- Verificar en vivo: leetspeak bloqueado; "voy a Lima…/¿y en Santiago?" mantiene Viajes; "clima en
  Narnia" pide confirmación.

## 5. Estado

- ✅ Fallos 2/4/7 implementados; `fallos.md` actualizado. Bitácora **035**.
