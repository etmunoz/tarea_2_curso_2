<!--encabezado-grupo-->
> **Archivo:** `evidencias/agentes_local.md`  
> **Objetivo:** Evidencia LOCAL — funcionamiento real de todos los agentes (una consulta por agente)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
<!--/encabezado-grupo-->

# Funcionamiento de los agentes — **LOCAL**, 2026-11-23

**Entorno y fecha:** LOCAL (Mac), 2026-11-23. **Backend:** FastAPI `127.0.0.1:8796` + langgraph `127.0.0.1:2025`.
**Agentes:** 8 locales (el 9º, `meteo_mcp`, se prueba en el VPS por `cryptography` en Mac — ver Anexo 14/17).
**Fuentes reales:** Gemini (ruteo+agentes), Redis remoto (RAG Reiki), Open-Meteo, UniProt, tipo de cambio,
Wikipedia. **Checkpointer del coordinador:** PostgresSaver (Postgres local). La API_KEY no se muestra.

Cada respuesta llega etiquetada `[agente_...]` (la salida del agente es un **dato**, no instrucción) y la
**ruta** muestra el recorrido A2A del coordinador.

| # | Agente (esperado) | Solicitud | Elegido | Ruta | OK |
|---|---|---|---|---|---|
| 1 | `agente_meteorologia` | clima hoy en Valdivia | `agente_meteorologia` | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 2 | `agente_reiki` | ¿qué es el Reiki y qué beneficios tiene? | `agente_reiki` | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 3 | `agente_bioinformatica` | dame información del gen TP53 en UniProt | `agente_bioinformatica` | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 4 | `agente_mlbioinformatica` | arma un pipeline de machine learning de punta a punta para c | `agente_mlbioinformatica` | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 5 | `agente_machinelearning` | ¿qué técnica uso si tengo desbalance de clases? | `agente_machinelearning` | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 6 | `agente_cocinachilena` | receta de pastel de choclo con costo aproximado | `agente_cocinachilena` | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 7 | `agente_viajes` | voy a viajar a Lima, ¿qué me cuentas del destino y el tipo d | `agente_viajes` | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |
| 8 | `agente_administrador` | ¿qué agentes hay disponibles? | `agente_administrador` | guardia_entrada → supervisor → agente_local → guardia_salida | ✅ |

## Respuestas reales (recortadas a ~500 car.)

### agente_meteorologia
- **Solicitud:** clima hoy en Valdivia
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[agente_meteorologia] El clima actual para hoy en Valdivia es de **13.7 °C**, con una condición de **llovizna débil**. 

Para este día se espera una temperatura mínima de **10 °C**, una máxima de **16.9 °C** y una precipitación acumulada de **1.3 mm**.
```

### agente_reiki
- **Solicitud:** ¿qué es el Reiki y qué beneficios tiene?
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[agente_reiki] Hola, soy Tomás, Maestro Reiki. El Reiki es una práctica de canalización de energía universal (Rei) y energía vital (Ki) que promueve la relajación, el equilibrio y el bienestar físico y emocional. Sus beneficios complementarios incluyen la reducción del estrés, la relajación profunda y la mejora de la vitalidad. *Nota: El Reiki es una práctica de bienestar complementario y no reemplaza la atención médica ni psicológica; ante cualquier dolencia, condición de salud o embarazo, acud
```

### agente_bioinformatica
- **Solicitud:** dame información del gen TP53 en UniProt
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[agente_bioinformatica] Aquí tienes los datos oficiales obtenidos directamente de UniProt:

* **Proteína:** Cellular tumor antigen p53
* **Gen:** TP53
* **Organismo:** *Homo sapiens*
* **Accession:** P04637
* **Longitud:** 393 aminoácidos
* **Función principal:** Factor de transcripción multifuncional que induce la detención del ciclo celular, la reparación del ADN o la apoptosis en respuesta al daño en el ADN.
* **Enlace a la fuente:** [UniProt P04637](https://www.uniprot.org/uniprotkb/P04637)

```

### agente_mlbioinformatica
- **Solicitud:** arma un pipeline de machine learning de punta a punta para clasificar secuencias, con partición sin fuga por homología y métricas
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[agente_mlbioinformatica] Como el pipeline que pediste aplica para clasificar secuencias, aquí tienes el flujo completo para secuencias de proteínas usando `recomendar_pipeline`:

- **Preprocesamiento:** limpiar y deduplicar; representar con embeddings de ESM-2/ProtT5 (sin alinear).
- **Partición:** train/test por identidad de secuencia (clusters CD-HIT/MMseqs2 al 30-40 %), NO al azar.
- **Modelo:** clasificador ligero sobre los embeddings (regresión logística o gradient boosting).
- **Métricas:
```

### agente_machinelearning
- **Solicitud:** ¿qué técnica uso si tengo desbalance de clases?
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[agente_machinelearning] Te sugiero usar class weights, resampleo (SMOTE/undersampling) y métricas tipo F1/PR-AUC porque la accuracy engaña con clases raras; hay que reponderar y medir sobre la minoritaria.
```

### agente_cocinachilena
- **Solicitud:** receta de pastel de choclo con costo aproximado
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[agente_cocinachilena] ¡Aquí tienes la receta y el costo aproximado del **Pastel de choclo** para 4 personas!

### Ingredientes
* 6 unidad de choclo
* 400 g de carne molida
* 300 g de trutro de pollo
* 2 unidad de cebolla
* 3 unidad de huevo
* 10 g de albahaca
* 20 g de azúcar

---

### Costo aproximado (para 4 personas)

* **Choclo** (6 un): $3.000
* **Carne molida** (400 g): $3.200
* **Trutro de pollo** (300 g): $1.350
* **Cebolla** (2 un): $600
* **Huevo** (3 un): $600
* **Albahaca** (10 g): 
```

### agente_viajes
- **Solicitud:** voy a viajar a Lima, ¿qué me cuentas del destino y el tipo de cambio?
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[agente_viajes] ¡Hola! Lima es la capital y ciudad más poblada de Perú, situada en la costa central frente al océano Pacífico. Es considerada el centro político, cultural y gastronómico del país.

En cuanto al tipo de cambio, 1 sol peruano (PEN) equivale aproximadamente a 295,37 pesos chilenos (CLP). 

Si necesitas cotizar vuelos, hoteles o actividades de manera estimada, o planificar algo más de tu viaje, dime desde dónde viajas, las fechas o cuántas noches te quedarás.
```

### agente_administrador
- **Solicitud:** ¿qué agentes hay disponibles?
- **Ruta (A2A):** `guardia_entrada → supervisor → agente_local → guardia_salida`

```
[agente_administrador] ¡Hola, Ezequiel! Actualmente tenemos varios agentes especializados listos para ayudarte. Aquí te presento a cada uno:

* **Agente de Machine Learning** (`agente_machinelearning`): Te orienta sobre técnicas, métricas y modelos para problemas con datos generales o tabulares.
* **Agente de ML en Bioinformática** (`agente_mlbioinformatica`): Diseña pipelines de IA y Data Science específicos para datos biológicos (secuencias, expresión génica, etc.).
* **Agente de Bioinformátic
```
