<!--encabezado-grupo-->
> **Archivo:** `evidencias/agentes_local.md`  
> **Objetivo:** Evidencia LOCAL — funcionamiento real de todos los agentes (una consulta por agente)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
<!--/encabezado-grupo-->

# Funcionamiento de los agentes — **LOCAL**, 2026-11-23

**Entorno y fecha:** LOCAL (Mac), 2026-11-23. **Backend:** FastAPI `127.0.0.1:8796` + langgraph `127.0.0.1:2025` (los **9 agentes**, fichas aplicadas).
**Fuentes reales:** Gemini (ruteo+agentes), Redis remoto (RAG Reiki), Open-Meteo, UniProt, tipo de cambio,
Wikipedia y **MCP de Meteosource** (`meteo_mcp`; en local sin token de pago → usa el **respaldo Open-Meteo**;
en el VPS, con la clave, usa Meteosource). **Checkpointer:** PostgresSaver (Postgres local). La API_KEY no se muestra.

El supervisor elige al agente por su **nombre de ficha** y lo invoca por **A2A**; la respuesta llega como
**dato** etiquetado `[Nombre]`. Reparto del clima: Chile→`meteorologia`, mundo→`meteo_mcp`.

| # | Agente | Solicitud | Elegido (supervisor) | Ruta | OK |
|---|---|---|---|---|---|
| 1 | `agente_meteorologia` | verifica el pronóstico de hoy contra lo observado en S | Agente de Meteorología | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 2 | `meteo_mcp` | ¿qué clima hace en Madrid hoy? | meteo_mcp | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 3 | `agente_reiki` | ¿qué es el Reiki y qué beneficios tiene? | Agente de Reiki | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 4 | `agente_bioinformatica` | dame información del gen TP53 en UniProt | Agente de Bioinformática | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 5 | `agente_mlbioinformatica` | arma un pipeline de machine learning de punta a punta  | Agente de ML en Bioinformática | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 6 | `agente_machinelearning` | ¿qué técnica uso si tengo desbalance de clases? | Agente de Machine Learning | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 7 | `agente_cocinachilena` | receta de pastel de choclo con costo aproximado | Agente de Cocina Chilena | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 8 | `agente_viajes` | voy a viajar a Lima, ¿qué me cuentas del destino y el  | Agente de Viajes | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 9 | `agente_administrador` | ¿qué agentes hay disponibles? | Agente Administrador | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |

## Respuestas reales (recortadas a ~500 car.)

### agente_meteorologia — elegido: Agente de Meteorología
- **Solicitud:** verifica el pronóstico de hoy contra lo observado en Santiago
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[Agente de Meteorología] Para hoy en Santiago, el pronóstico y lo observado se comportan de la siguiente manera:

* **Temperatura actual:** 20.2 °C
* **Condición:** Llovizna débil (precipitación: 0.9 mm)
* **Comparación (Pronosticado vs. Real):**
  * **Mínima:** Pronosticada 13.7 °C | Observada 13.7 °C (Diferencia: 0.0 °C)
  * **Máxima:** Pronosticada 25.7 °C | Observada 25.6 °C (Diferencia: -0.1 °C)
  * **Condición:** Ambas coinciden en llovizna débil.
```

### meteo_mcp — elegido: meteo_mcp
- **Solicitud:** ¿qué clima hace en Madrid hoy?
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[meteo_mcp] ### Clima en Madrid (España)

* **Estado actual:** Parcialmente soleado
* **Temperatura actual:** 14.2 °C
* **Precipitaciones:** Sin lluvia (0 mm)
* **Viento:** 0.8 km/h proveniente del este

#### Pronóstico para hoy
* **Resumen:** Soleado, con aumento de nubosidad por la tarde.
* **Temperaturas esperadas:** Mínima de 1 °C y máxima de hasta 14.2 °C.
```

### agente_reiki — elegido: Agente de Reiki
- **Solicitud:** ¿qué es el Reiki y qué beneficios tiene?
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[Agente de Reiki] El Reiki es una técnica japonesa que canaliza la energía universal (Rei) y vital (Ki) para armonizar el cuerpo y la mente, enfocándose en la relajación y el bienestar físico y emocional. Como práctica complementaria, ayuda a reducir el estrés, fomentar la calma, mejorar el descanso y aliviar tensiones leves. Ten en cuenta que es un enfoque de bienestar que no reemplaza la atención médica ni psicológica; ante síntomas, dolor persistente o condiciones de salud, acude siempre a un
```

### agente_bioinformatica — elegido: Agente de Bioinformática
- **Solicitud:** dame información del gen TP53 en UniProt
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[Agente de Bioinformática] Aquí tienes la información oficial consultada en directo desde UniProt para el gen TP53 en humanos (*Homo sapiens*):

- **Nombre:** Cellular tumor antigen p53
- **Gen:** TP53
- **Accession:** P04637
- **Organismo:** *Homo sapiens*
- **Longitud:** 393 aminoácidos
- **Función principal:** Funciona como un factor de transcripción multifuncional que induce la detención del ciclo celular, la reparación del ADN o la apoptosis en respuesta a diferentes tipos de estrés celular
```

### agente_mlbioinformatica — elegido: Agente de ML en Bioinformática
- **Solicitud:** arma un pipeline de machine learning de punta a punta para clasificar secuencias, con partición sin fuga por homología y métricas
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[Agente de ML en Bioinformática] Soy ProteinMAN, creado por Fabio Durán. Para clasificar secuencias de proteínas, el pipeline de punta a punta devuelto por la herramienta es el siguiente: preprocesar deduplicando y generando embeddings (ESM-2/ProtT5); particionar por identidad de secuencia (clusters CD-HIT/MMseqs2 al 30-40 %) para evitar la trampa típica de la **fuga por homología** (secuencias casi idénticas en train y test que inflan artificialmente las métricas). El modelo recomendado es un c
```

### agente_machinelearning — elegido: Agente de Machine Learning
- **Solicitud:** ¿qué técnica uso si tengo desbalance de clases?
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[Agente de Machine Learning] Te recomiendo usar class weights, técnicas de resampleo como SMOTE o undersampling, y métricas como F1-score o PR-AUC. La accuracy engaña con clases raras, por lo que debes reponderar y medir sobre la clase minoritaria.
```

### agente_cocinachilena — elegido: Agente de Cocina Chilena
- **Solicitud:** receta de pastel de choclo con costo aproximado
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[Agente de Cocina Chilena] Aquí tienes la receta y el costo aproximado para **4 personas** del tradicional **Pastel de choclo**:

### Ingredientes
* 6 unidades de choclo
* 400 g de carne molida
* 300 g de trutro de pollo
* 2 unidades de cebolla
* 3 unidades de huevo
* 10 g de albahaca
* 20 g de azúcar

---

### Costo aproximado (para 4 personas)

* **Choclo** (6 un): $3.000
* **Carne molida** (400 g): $3.200
* **Trutro de pollo** (300 g): $1.350
* **Cebolla** (2 un): $600
* **Huevo** (3 un): $60
```

### agente_viajes — elegido: Agente de Viajes
- **Solicitud:** voy a viajar a Lima, ¿qué me cuentas del destino y el tipo de cambio?
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[Agente de Viajes] Lima es la capital y ciudad más poblada de Perú, situada frente al océano Pacífico. Es el principal centro político, cultural, financiero y gastronómico del país. 

Sobre la moneda, la unidad oficial es el Sol peruano (PEN). El tipo de cambio actual es de aproximadamente **295,37 pesos chilenos (CLP) por cada sol**.
```

### agente_administrador — elegido: Agente Administrador
- **Solicitud:** ¿qué agentes hay disponibles?
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[Agente Administrador] ¡Hola! En este sistema contamos con varios agentes especializados para ayudarte en distintas áreas. Aquí te muestro quiénes son y qué hace cada uno:

- **Agente de Machine Learning** (`agente_machinelearning`): Recomienda qué técnica, modelo y métricas usar para problemas con datos generales o tabulares.
- **Agente de ML en Bioinformática** (`agente_mlbioinformatica`): Diseña *pipelines* de Machine Learning y recomienda modelos enfocados en datos biológicos (secuencias, ex
```
