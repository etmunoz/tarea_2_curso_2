<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_029.md`  
> **Objetivo:** 029 · Respuesta — ML-bioinformática diferenciado (recomendar_pipeline)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1150 · **Última modificación:** 20261118 1150
<!--/encabezado-grupo-->

# 029 · Respuesta — Diferenciar ML-bioinformática

**Prompt:** [`../prompts_ejecutados/prompt_029.md`](../prompts_ejecutados/prompt_029.md)

---

## 1. Qué se hizo

- **`recomendar_pipeline(tipo_de_dato)`**: herramienta insignia con 6 tipos de dato biológico; devuelve
  preprocesamiento, partición, modelo, métricas y la trampa a evitar. Es la capacidad distintiva frente
  a machinelearning.
- **`_buscar`**: filtra stopwords ("de", "la", …) para no calzar por la preposición común.
- **Prompt (RF-03b)** y **ficha** actualizados (identidad bio-ML; el supervisor la distingue).
- **Tests** nuevos: **3 passed** (incluye el desconocido que antes fallaba por "de").

## 2. Verificación (herramienta directa, VPS)

- `variantes geneticas` → partición *"agrupada por gen/proteína (la misma proteína no puede estar en
  train y test)"*, trampa *"mezclar variantes de la misma proteína entre particiones"*.
- `secuencias de proteinas` → partición por identidad de secuencia; trampa: fuga por homología.

## 3. Pendiente / verificación en vivo

- `sudo systemctl restart t2c2-langgraph` (código del agente) y `t2c2-fichas` (ficha).
- Verificar por el gateway que una pregunta de **pipeline bio-ML** rutea a **ML en Bioinformática** y
  una de **ML general** a **Machine Learning** → evidencias.

## 4. Estado

- ✅ Código + prompt + ficha + tests; desplegado. Bitácora **029**.
