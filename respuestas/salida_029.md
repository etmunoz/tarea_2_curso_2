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

## 3. Verificación en vivo (gateway, tras reiniciar)

- **"pipeline de ML para clasificar secuencias de proteínas"** → **ML en Bioinformática**: embeddings
  ESM-2/ProtT5 + Gradient Boosting (tool `recomendar_pipeline`).
- **"overfitting en un modelo tabular"** → **Machine Learning**: regularización + early stopping + CV.
- ⇒ La **separación** entre ambos agentes funciona (cada pregunta fue al agente correcto).

## 4. Estado

- ✅ Código + prompt + ficha + tests; desplegado y **verificado en producción**. Bitácora **029**.
