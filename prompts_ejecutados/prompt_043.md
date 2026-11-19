<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_043.md`  
> **Objetivo:** 043 · Endurecer la guardia contra ofuscación + derivación en machinelearning  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1330 · **Última modificación:** 20261119 1330
<!--/encabezado-grupo-->

# 043 · Guardia anti-ofuscación + derivación ML

**Contexto / pedido:** se revisó la evidencia nueva de **Fabio** (merge de `fix/prompts-mezcla-dominios`,
commit `07b46ba`): batería **masiva (24)** y de **ofuscación (56)** en producción. El usuario pidió
dejar todo en prompts/salidas/evidencias y avanzar con los arreglos.

**Hallazgos de Fabio que se atacan:**
- **Seguridad:** 0 filtraciones / 56, pero la **guardia de entrada solo veía texto plano**: dejaba pasar
  **base64, rot13, homoglifos cirílicos, ancho cero, ancho completo y texto espaciado** (defendía solo el
  LLM).
- **Funcional:** el prompt de **machinelearning** era el único sin la regla de derivar al agente correcto.

**Alcance:**
1. **`src/coordinador/guardrails.py`** (fix A, seguridad):
   - `normalizar`: **NFKC** (ancho completo/compatibilidad → normal) y eliminación de **caracteres
     invisibles/ancho cero/bidi**.
   - `_hay_inyeccion`: evalúa el patrón sobre variantes **des-ofuscadas** (de-leet, **homoglifos**,
     **rot13**, **base64 decodificado**) y una versión **compacta** (sin espacios) con firmas compactas,
     para atrapar el **texto espaciado** y el concatenado. Aplica también a `es_instruccion_remota` (A2A).
2. **`src/agente_machinelearning/prompts.py`** (fix B): agrega la regla de **derivar/sugerir** el agente
   correcto cuando una parte queda fuera de IA/Data Science.
3. **Tests** (`tests/test_guardrails.py`): bloqueo de base64/rot13/homoglifos/ancho completo/ancho
   cero/espaciado y **no-falsos-positivos** en español con acentos/ñ/números.

**Restricción:** no romper texto legítimo en español (verificado con tests); solo guardia + prompt, sin
tocar dependencias. Se mantienen los guardrails existentes.
