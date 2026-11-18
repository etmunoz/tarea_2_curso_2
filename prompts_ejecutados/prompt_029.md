<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_029.md`  
> **Objetivo:** 029 · Diferenciar el Agente de ML en Bioinformática (herramienta insignia: recomendar_pipeline)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1150 · **Última modificación:** 20261118 1150
<!--/encabezado-grupo-->

# 029 · Diferenciar ML-bioinformática

**Pedido del usuario (verbatim):**

> Mejora **#3** de las acordadas: «Diferenciar ML-bioinformática» (hoy comparte los nombres de
> herramientas con machinelearning).

**Hallazgo:** los catálogos de mlbioinformática ya eran bio-específicos (fuga por homología, ESM-2,
efecto de lote, p≫n); la duplicación real eran los **nombres** de herramientas y un `consultar_modelos`
genérico compartido.

**Alcance:**
1. **Herramienta insignia** `recomendar_pipeline(tipo_de_dato)` (`herramientas.py`): pipeline de ML de
   punta a punta por tipo de dato biológico (secuencias de proteínas/ADN, expresión génica, variantes,
   estructuras, imágenes) → preprocesamiento, **partición** (sin fuga por homología), modelo, métricas
   y la **trampa** a evitar. Es la capacidad que machinelearning no tiene.
2. **Fix en `_buscar`:** filtra palabras vacías ("de", "la", …) para que una consulta desconocida no
   calce por la preposición común (lo destapó un test).
3. **`prompts.py`:** RF-03b (usar `recomendar_pipeline` para flujos completos).
4. **`src/fichas.py`:** ficha de mlbioinformática reescrita (arma PIPELINES de punta a punta) para que
   el supervisor la distinga de machinelearning.
5. **`tests/test_agente_mlbioinformatica.py`** (nuevo): pipeline conocido, expresión génica y desconocido.

**Restricción:** datos simulados pero creíbles (guía de modelado); separación clara de roles —
machinelearning = ML/DS general; mlbioinformática = ML aplicado a datos biológicos; la biología de
fondo es de agente_bioinformatica.
