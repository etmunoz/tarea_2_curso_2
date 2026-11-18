# --8<-- encabezado-grupo
# Archivo: src/agente_mlbioinformatica/herramientas.py
# Objetivo: Herramientas de ProteinMAN: técnica, métricas, modelo y catálogo SQLite (bio-ML).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261113 1130
# Última modificación: 20261113 1130
# --8<-- fin-encabezado-grupo

# Autor: Fabio Durán · Taller 05. Basado en tarea_1_curso_2/src/agente_machinelearning/herramientas.py (cambios en README.md).

"""Herramientas de ProteinMAN · IA y Data Science aplicada a bioinformática (agente creado por Fabio Durán).

Mismas cuatro herramientas que el agente original del repositorio del grupo; los catálogos ahora hablan de datos
biológicos (secuencias, expresión génica, estructuras, variantes). Datos simulados pero
creíbles: en producción saldrían de una guía interna o de un tracking de experimentos.
Si preguntan algo que no está en los datos, la herramienta lo dice en UNA línea; nunca lanza un error.
"""
from __future__ import annotations

import unicodedata

from langchain_core.tools import tool

from src.agente_mlbioinformatica import bd_modelos


def _norm(texto: str) -> str:
    """minúsculas, sin acentos: para casar la entrada del usuario con las claves."""
    t = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


# ── catálogos (bio-ML) ───────────────────────────────────────────────────────
# problema de ML en bioinformática  →  técnica recomendada + por qué
TECNICAS: dict[str, dict] = {
    "fuga por homologia": {"tecnica": "particionar train/test por identidad de secuencia (clusters de CD-HIT o MMseqs2 al 30-40 %), no al azar",
                           "por_que": "secuencias casi idénticas en train y test inflan las métricas; el modelo memoriza homólogos en vez de generalizar"},
    "clasificacion de secuencias": {"tecnica": "embeddings de un modelo de lenguaje de proteínas (ESM-2, ProtT5) + clasificador ligero (regresión logística, GBM)",
                                    "por_que": "los embeddings capturan señal evolutiva y estructural sin alinear, y el clasificador se entrena en minutos"},
    "pocas muestras muchos genes": {"tecnica": "regularización L1/elastic net o selección de features + validación cruzada anidada",
                                    "por_que": "con miles de genes y decenas de muestras (p >> n) el sobreajuste es casi seguro sin penalizar"},
    "desbalance de familias": {"tecnica": "class weights, submuestreo de familias grandes y métricas por clase (F1 macro, PR-AUC)",
                               "por_que": "unas pocas familias grandes dominan UniProt; la accuracy esconde el mal desempeño en las raras"},
    "efecto de lote": {"tecnica": "corrección de batch (ComBat, Harmony) dentro de cada fold y lote como covariable",
                       "por_que": "las diferencias técnicas entre corridas pueden separar las clases mejor que la biología"},
    "datos faltantes": {"tecnica": "imputación (KNN, mediana por gen) dentro de cada fold, o modelos que toleran NaN (gradient boosting)",
                        "por_que": "imputar con todo el dataset filtra información del test; los GBM manejan faltantes de forma nativa"},
    "pocos datos etiquetados": {"tecnica": "transfer learning: embeddings preentrenados (ESM-2, DNABERT) o fine-tuning ligero",
                                "por_que": "reutilizar lo aprendido sobre millones de secuencias rinde más que entrenar desde cero"},
    "alta dimensionalidad": {"tecnica": "reducción (PCA, UMAP para visualizar) o selección de genes por varianza o importancia",
                             "por_que": "menos ruido y cómputo, y modelos que generalizan mejor"},
}

# tipo de problema  →  métricas a mirar
METRICAS: dict[str, list[str]] = {
    "clasificacion": ["accuracy", "F1 (macro y por clase)", "matriz de confusión", "ROC-AUC"],
    "clasificacion desbalanceada": ["F1 macro y F1 de las clases minoritarias", "PR-AUC", "MCC (coeficiente de Matthews)",
                                    "matriz de confusión; evitar la accuracy sola"],
    "clasificacion multiclase de familias": ["F1 macro", "accuracy balanceada", "matriz de confusión por familia",
                                             "desempeño por nivel de identidad con el train"],
    "regresion": ["MAE", "RMSE", "R²", "correlación de Spearman (p. ej. expresión o afinidad)"],
    "clustering": ["silhouette", "ARI/NMI contra etiquetas conocidas", "inspección biológica de los clusters"],
    "prediccion de variantes patogenicas": ["ROC-AUC", "PR-AUC", "sensibilidad a especificidad fija", "calibración"],
    "deteccion de anomalias": ["precision@k", "recall sobre anomalías conocidas", "falsos positivos por corrida"],
}

# tipo de dato biológico  →  modelo/enfoque de arranque
MODELOS: dict[str, dict] = {
    "secuencias de proteinas": {"modelo": "embeddings de ESM-2 o ProtT5 + regresión logística o gradient boosting",
                                "nota": "parte con el modelo pequeño (ESM-2 de 35M); particiona por identidad de secuencia"},
    "secuencias de adn": {"modelo": "conteo de k-mers + gradient boosting, o embeddings de DNABERT/Nucleotide Transformer",
                          "nota": "los k-mers son un baseline fuerte y barato antes de un modelo de lenguaje"},
    "expresion genica": {"modelo": "regresión logística con L1/elastic net o random forest, tras normalizar y filtrar genes",
                         "nota": "p >> n: valida con CV anidada y corrige el efecto de lote dentro de cada fold"},
    "estructuras de proteinas": {"modelo": "redes de grafos (GNN) sobre el grafo de contactos, o embeddings estructurales",
                                 "nota": "las estructuras predichas (AlphaFold DB) sirven para ampliar el set"},
    "variantes geneticas": {"modelo": "gradient boosting sobre anotaciones (conservación, frecuencia poblacional, impacto)",
                            "nota": "cuida que la misma proteína no quede en train y test a la vez"},
    "imagenes de microscopia": {"modelo": "CNN preentrenada (ResNet/EfficientNet) o ViT con fine-tuning",
                                "nota": "el transfer learning casi siempre gana a entrenar desde cero"},
    "tabular": {"modelo": "gradient boosting (XGBoost/LightGBM)",
                "nota": "baseline fuerte para datos tabulares (por ejemplo, metadatos clínicos o anotaciones)"},
}


# tipo de dato biológico  →  pipeline de ML de punta a punta (lo distintivo de este agente)
PIPELINES: dict[str, dict] = {
    "secuencias de proteinas": {
        "preprocesamiento": "limpiar y deduplicar; representar con embeddings de ESM-2/ProtT5 (sin alinear)",
        "particion": "train/test por identidad de secuencia (clusters CD-HIT/MMseqs2 al 30-40 %), NO al azar",
        "modelo": "clasificador ligero sobre los embeddings (regresión logística o gradient boosting)",
        "metricas": ["F1 macro y por clase", "MCC", "desempeño por nivel de identidad con el train"],
        "trampa": "fuga por homología: secuencias casi idénticas en train y test inflan las métricas",
    },
    "secuencias de adn": {
        "preprocesamiento": "control de calidad (FastQC); baseline de k-mers o embeddings DNABERT/Nucleotide Transformer",
        "particion": "por identidad/no solapamiento genómico; evita duplicados entre train y test",
        "modelo": "k-mers + gradient boosting como baseline; modelo de lenguaje si hay datos",
        "metricas": ["F1/ROC-AUC según la tarea", "PR-AUC si hay desbalance"],
        "trampa": "regiones repetidas o casi idénticas filtradas entre particiones",
    },
    "expresion genica": {
        "preprocesamiento": "normalizar, filtrar genes por varianza, corregir efecto de lote (ComBat/Harmony) DENTRO de cada fold",
        "particion": "validación cruzada anidada (p >> n: miles de genes, pocas muestras)",
        "modelo": "regresión logística L1/elastic net o random forest",
        "metricas": ["F1 macro", "accuracy balanceada", "AUC"],
        "trampa": "corregir el lote o seleccionar genes con TODO el dataset filtra información del test",
    },
    "variantes geneticas": {
        "preprocesamiento": "anotar (conservación, frecuencia poblacional, impacto); escalar",
        "particion": "agrupada por gen/proteína (la misma proteína no puede estar en train y test)",
        "modelo": "gradient boosting sobre las anotaciones",
        "metricas": ["ROC-AUC", "PR-AUC", "sensibilidad a especificidad fija", "calibración"],
        "trampa": "mezclar variantes de la misma proteína entre particiones",
    },
    "estructuras de proteinas": {
        "preprocesamiento": "construir el grafo de contactos; ampliar el set con estructuras predichas (AlphaFold DB)",
        "particion": "por familia/plegamiento para evitar redundancia estructural",
        "modelo": "redes de grafos (GNN) o embeddings estructurales",
        "metricas": ["F1 macro", "ROC-AUC", "inspección estructural de los aciertos"],
        "trampa": "estructuras redundantes (mismo plegamiento) repartidas entre train y test",
    },
    "imagenes de microscopia": {
        "preprocesamiento": "normalizar por canal; aumentos (rotación/flip); control por placa/lote",
        "particion": "por lote/placa para no filtrar el efecto técnico",
        "modelo": "CNN preentrenada (ResNet/EfficientNet) o ViT con fine-tuning",
        "metricas": ["F1 macro", "matriz de confusión", "AUC"],
        "trampa": "fuga por lote: el modelo aprende la placa en vez de la biología",
    },
}


def _buscar(catalogo: dict, consulta: str) -> str | None:
    """Devuelve la clave del catálogo que mejor casa con la consulta (o None).

    Orden: coincidencia exacta → clave contenida en la consulta (gana la MÁS LARGA, así
    «clasificacion desbalanceada» no cae en «clasificacion») → palabras en común → raíz.
    """
    q = _norm(consulta).strip()
    claves = {_norm(c): c for c in catalogo}
    if q in claves:
        return claves[q]
    en_consulta = [c for c in claves if c in q]
    if en_consulta:
        return claves[max(en_consulta, key=len)]
    contienen = [c for c in claves if q and q in c]
    if contienen:  # consulta corta y genérica: la primera del catálogo (el orden refleja lo más común)
        return claves[contienen[0]]
    _VACIAS = {"de", "del", "la", "el", "los", "las", "un", "una", "y", "o", "en", "con", "para"}
    palabras = {w for w in q.split() if w not in _VACIAS and len(w) > 2}
    mejor = max(claves, key=lambda c: len(palabras & set(c.split())))
    if palabras & set(mejor.split()):
        return claves[mejor]
    for c in claves:
        for kw in c.split():
            for qw in palabras:
                if len(kw) >= 5 and len(qw) >= 5 and kw[:5] == qw[:5]:
                    return claves[c]
    return None


@tool
def recomendar_tecnica(problema: str) -> dict:
    """Recomienda una técnica de ML para un problema de bioinformática y explica por qué.
    Problemas: 'fuga por homologia', 'clasificacion de secuencias', 'pocas muestras muchos genes',
    'desbalance de familias', 'efecto de lote', 'datos faltantes', 'pocos datos etiquetados',
    'alta dimensionalidad'.
    Devuelve {problema, tecnica, por_que}. Si no reconoce el problema, lo dice en una línea."""
    clave = _buscar(TECNICAS, problema)
    if not clave:
        return {"nota": f"No tengo una técnica catalogada para «{problema}». Puedo ayudar con: {', '.join(TECNICAS)}."}
    return {"problema": clave, **TECNICAS[clave]}


@tool
def metricas_recomendadas(tipo_problema: str) -> dict:
    """Dice qué métricas usar según el tipo de problema de ML en bioinformática.
    Tipos: 'clasificacion', 'clasificacion desbalanceada', 'clasificacion multiclase de familias',
    'regresion', 'clustering', 'prediccion de variantes patogenicas', 'deteccion de anomalias'.
    Devuelve {tipo, metricas:[...]}. Si no reconoce el tipo, lo dice en una línea."""
    clave = _buscar(METRICAS, tipo_problema)
    if not clave:
        return {"nota": f"No tengo métricas catalogadas para «{tipo_problema}». Tipos que manejo: {', '.join(METRICAS)}."}
    return {"tipo": clave, "metricas": METRICAS[clave]}


@tool
def elegir_modelo(tipo_de_dato: str) -> dict:
    """Sugiere un modelo de arranque según el tipo de dato biológico.
    Tipos: 'secuencias de proteinas', 'secuencias de adn', 'expresion genica', 'estructuras de proteinas',
    'variantes geneticas', 'imagenes de microscopia', 'tabular'.
    Devuelve {tipo, modelo, nota}. Si no reconoce el tipo, lo dice en una línea."""
    clave = _buscar(MODELOS, tipo_de_dato)
    if not clave:
        return {"nota": f"No tengo un modelo catalogado para «{tipo_de_dato}». Tipos que manejo: {', '.join(MODELOS)}."}
    return {"tipo": clave, **MODELOS[clave]}


@tool
def consultar_modelos(consulta: str = "", tipo: str = "") -> list[dict]:
    """Consulta el catálogo general de modelos de ciencia de datos en la base SQLite.
    `tipo` opcional: 'supervisado', 'no supervisado' o 'refuerzo'. `consulta` busca por
    nombre, para qué sirve, cómo se usa o librerías (p. ej. 'clustering', 'xgboost').
    Devuelve, por modelo: nombre, tipo, para_que, como_se_utiliza, librerias y ejemplo_python.
    Si no hay coincidencias, devuelve una lista vacía."""
    return bd_modelos.consultar(consulta=consulta, tipo=tipo)


@tool
def recomendar_pipeline(tipo_de_dato: str) -> dict:
    """Arma un PIPELINE de ML de punta a punta para un tipo de dato biológico: preprocesamiento,
    estrategia de partición, modelo, métricas y la trampa típica a evitar. Es la herramienta
    distintiva de este agente (ML aplicado a bioinformática).
    Tipos: 'secuencias de proteinas', 'secuencias de adn', 'expresion genica', 'variantes geneticas',
    'estructuras de proteinas', 'imagenes de microscopia'.
    Devuelve {tipo, preprocesamiento, particion, modelo, metricas:[...], trampa}. Si no reconoce el
    tipo, lo dice en una línea."""
    clave = _buscar(PIPELINES, tipo_de_dato)
    if not clave:
        return {"nota": f"No tengo un pipeline catalogado para «{tipo_de_dato}». Tipos: {', '.join(PIPELINES)}."}
    return {"tipo": clave, **PIPELINES[clave]}


HERRAMIENTAS = [recomendar_pipeline, recomendar_tecnica, metricas_recomendadas, elegir_modelo, consultar_modelos]
