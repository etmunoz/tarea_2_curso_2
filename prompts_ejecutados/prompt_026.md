<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_026.md`  
> **Objetivo:** 026 · Enriquecer el agente_reiki para recomendar terapias holísticas complementarias  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 0935 · **Última modificación:** 20261118 0935
<!--/encabezado-grupo-->

# 026 · Terapias holísticas complementarias en el agente_reiki

**Pedido del usuario (verbatim):**

> «quiero que agregues más información de Reiki al agente_reiki, por favor, para que pueda entregar
> recomendaciones de terapias holísticas complementarias basadas en Reiki.»

**Alcance:**
1. **Conocimiento (RAG):** nuevo documento `data/reiki/terapias-complementarias.md` (síntesis original,
   sin copyright): prácticas que combinan con Reiki (meditación, respiración, aromaterapia, sonoterapia,
   chakras, cristales, movimiento suave, naturaleza), recomendaciones **por objetivo** (estrés/ansiedad,
   sueño, ánimo, energía, tensión), estructura de sesión y **precauciones**. Reindexado en Redis.
2. **Herramienta:** `terapias_complementarias(objetivo)` en `src/agente_reiki/herramientas.py` —
   recomendaciones estructuradas por objetivo con sinónimos (ansiedad→estrés, dormir→sueño, etc.) y
   nota de seguridad; agregada a `HERRAMIENTAS`.
3. **Prompt:** `SYSTEM_TOMAS` habilita recomendar terapias complementarias **como bienestar**, usando
   `terapias_complementarias` y `buscar_reiki`, manteniendo los guardrails (no consejo médico/psicológico,
   no reemplaza atención profesional, derivar ante enfermedad/dolor/embarazo).
4. **Pruebas:** `tests/test_agente_reiki.py` cubre objetivo conocido, sinónimo y objetivo sin calce.

**Restricción:** encuadre de **bienestar complementario**; nunca consejo médico/financiero. Solo
síntesis original (sin copiar texto con copyright). Reindexar Redis y reiniciar `t2c2-langgraph`.
