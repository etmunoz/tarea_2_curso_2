<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_026.md`  
> **Objetivo:** 026 · Respuesta — agente_reiki recomienda terapias holísticas complementarias (RAG + tool)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 0935 · **Última modificación:** 20261118 0935
<!--/encabezado-grupo-->

# 026 · Respuesta — Terapias complementarias en Reiki

**Prompt:** [`../prompts_ejecutados/prompt_026.md`](../prompts_ejecutados/prompt_026.md)

---

## 1. Qué se agregó

- **`data/reiki/terapias-complementarias.md`** (nuevo, síntesis original): prácticas complementarias,
  recomendaciones por objetivo, estructura de sesión y precauciones. **Indexado en Redis.**
- **`src/agente_reiki/herramientas.py`**: herramienta `terapias_complementarias(objetivo)` +
  catálogos `TERAPIAS` y `SINONIMOS`; agregada a `HERRAMIENTAS`.
- **`src/agente_reiki/prompts.py`**: `SYSTEM_TOMAS` habilita recomendar terapias complementarias con
  encuadre de bienestar y guardrails intactos.
- **`tests/test_agente_reiki.py`**: 3 pruebas nuevas (objetivo conocido / sinónimo / sin calce).
- **`data/reiki/FUENTES.md`**: menciona el nuevo documento como síntesis original.

## 2. Verificación

- **Tests locales:** `pytest tests/test_agente_reiki.py tests/test_rag_reiki.py` → **10 passed, 1 skipped**.
- **Reindexado en Redis:** 6 documentos (`nivel-1..4`, `FUENTES`, `terapias-complementarias`),
  **18 fragmentos** (antes 9). `buscar("terapias complementarias para el estrés")` devuelve los
  fragmentos de `terapias-complementarias.md`.
- **En vivo (tras reiniciar `t2c2-langgraph`):** consulta de recomendación ruteada al Agente de Reiki
  responde usando la nueva herramienta/contenido (ver evidencias).

## 3. Seguridad / encuadre

Bienestar **complementario**: no da consejo médico, psicológico ni financiero, no diagnostica y no
reemplaza la atención profesional; deriva ante enfermedad, dolor intenso/persistente o embarazo.

## 4. Estado

- ✅ Conocimiento + herramienta + prompt + pruebas; desplegado y reindexado.
- ✅ Bitácora **000–026**. (Requiere `sudo systemctl restart t2c2-langgraph` para el código nuevo.)
