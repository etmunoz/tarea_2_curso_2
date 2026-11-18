<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_027.md`  
> **Objetivo:** 027 · Ampliar el catálogo de terapias complementarias: duelo, concentración, cefalea tensional  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1010 · **Última modificación:** 20261118 1010
<!--/encabezado-grupo-->

# 027 · Más objetivos de terapias complementarias

**Pedido del usuario (verbatim):**

> «amplía el catálogo con duelo, concentración y dolor de cabeza tensional»

**Alcance:**
1. **Herramienta** `terapias_complementarias` (`src/agente_reiki/herramientas.py`): tres objetivos
   nuevos en `TERAPIAS` — `duelo`, `concentracion`, `cefalea` — con sus sinónimos
   (`pérdida/pena/luto`, `concentrar/atención/foco/enfoque/estudiar`, `cabeza/jaqueca/migraña`).
2. **Lógica de calce:** se cambió a **sinónimos primero** para que "dolor de cabeza tensional"
   caiga en `cefalea` y no en `tension` (el substring "tensional" capturaba "tension").
3. **RAG:** se ampliaron las "Recomendaciones por objetivo" en
   `data/reiki/terapias-complementarias.md` (duelo, concentración, cefalea). Reindexado en Redis.
4. **Prompt:** `SYSTEM_TOMAS` lista los nuevos objetivos.
5. **Pruebas:** 3 nuevas (duelo, concentración, y "dolor de cabeza tensional" → cefalea).

**Restricción:** bienestar complementario, con notas de derivación (duelo prolongado → apoyo
psicológico; cefalea intensa/súbita/frecuente → profesional). Reindexar Redis y reiniciar
`t2c2-langgraph`.
