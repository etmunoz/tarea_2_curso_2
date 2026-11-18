<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_027.md`  
> **Objetivo:** 027 · Respuesta — catálogo ampliado (duelo, concentración, cefalea tensional)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1010 · **Última modificación:** 20261118 1010
<!--/encabezado-grupo-->

# 027 · Respuesta — Más objetivos de bienestar

**Prompt:** [`../prompts_ejecutados/prompt_027.md`](../prompts_ejecutados/prompt_027.md)

---

## 1. Qué se agregó

| Objetivo | Prácticas (resumen) | Nota de seguridad |
|---|---|---|
| **duelo** | Reiki en el corazón · respiración/gratitud · diario de recuerdos · sonoterapia y red de apoyo | duelo intenso/prolongado → apoyo psicológico |
| **concentración** | Reiki frente/corona · respiración 2–3 min · menta/romero · pausas y menos distracciones | atención sostenida difícil → consultar |
| **cefalea tensional** | manos en sienes/nuca/hombros · respiración lenta · compresa tibia · hidratación/pausas de pantalla | dolor intenso/súbito/frecuente → profesional |

- Sinónimos añadidos y **lógica "sinónimos primero"**: "dolor de cabeza tensional" → **cefalea**
  (antes el substring "tensional" lo llevaba a `tension`).
- `data/reiki/terapias-complementarias.md` ampliado y **reindexado en Redis** (19 fragmentos).
- `SYSTEM_TOMAS` lista los nuevos objetivos.

## 2. Verificación

- **Tests:** `pytest tests/test_agente_reiki.py` → **11 passed** (incluye duelo, concentración y el caso
  "dolor de cabeza tensional" → cefalea).
- **RAG:** `buscar("duelo…"/"concentracion"/"dolor de cabeza tensional")` → `terapias-complementarias.md`.
- **En vivo (tras reiniciar `t2c2-langgraph`):** ver evidencias (Anexo 4).

## 3. Estado

- ✅ Catálogo ampliado, desplegado y reindexado. Bitácora **000–027**.
- Requiere `sudo systemctl restart t2c2-langgraph` para el código nuevo.
