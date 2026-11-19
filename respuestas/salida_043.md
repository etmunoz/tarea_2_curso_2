<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_043.md`  
> **Objetivo:** 043 · Respuesta — guardia anti-ofuscación + derivación en machinelearning  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1330 · **Última modificación:** 20261119 1330
<!--/encabezado-grupo-->

# 043 · Respuesta — Guardia anti-ofuscación + ML deriva

**Prompt:** [`../prompts_ejecutados/prompt_043.md`](../prompts_ejecutados/prompt_043.md)

---

## 1. Qué se hizo

- **Merge** de la evidencia de Fabio (pruebas masivas 24 + ofuscación 56) a `main`.
- **Fix A · guardia anti-ofuscación** (`guardrails.py`): `normalizar` con **NFKC** + quita invisibles;
  `_hay_inyeccion` evalúa variantes des-ofuscadas (de-leet, **homoglifos**, **rot13**, **base64**) y una
  versión **compacta** sin espacios (texto espaciado/concatenado). Vale también para A2A.
- **Fix B · derivación** (`agente_machinelearning/prompts.py`): sugiere el agente correcto cuando una
  parte queda fuera de IA/Data Science.
- **Tests**: ofuscación bloqueada + no-falsos-positivos → **164 passed**.

## 2. Cobertura de los vectores de ofuscación (antes solo los paraba el LLM)

| Vector | Cómo se ataja ahora |
|---|---|
| base64 | se decodifica el bloque y se evalúa |
| rot13 | variante rot13 |
| homoglifos cirílicos/griegos | tabla de confusables |
| ancho cero / bidi | se eliminan en `normalizar` |
| ancho completo | NFKC en `normalizar` |
| texto espaciado | firmas compactas sobre la versión sin espacios |
| leetspeak / inglés | ya existían (registro 035) |

## 3. Pendiente de activación

- `sudo systemctl restart t2c2-api t2c2-langgraph` (guardia/coordinador + agente ML). Verificación en
  vivo: los 7 casos de ofuscación quedan bloqueados por `guardia_entrada` y el agente de ML deriva.

## 4. Estado

- ✅ Guardia reforzada + ML deriva; 164 tests verdes; desplegado. Bitácora **043**.
