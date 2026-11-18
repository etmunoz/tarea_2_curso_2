# --8<-- encabezado-grupo
# Archivo: src/fichas.py
# Objetivo: Fichas (Agent Card) de los agentes locales: nombre y descripcion (identidad funcional).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261110 1952
# Última modificación: 20261117 1508
# --8<-- fin-encabezado-grupo

"""Fichas (Agent Card) de los agentes locales: nombre y descripción.

Con A2A nativo de `langgraph dev`, la tarjeta la publica el servidor a partir del `name` y la
`description` del assistant. Aquí se definen esos textos y `tools/configurar_fichas.py` los aplica con
`PATCH /assistants/<id>`. Tarea 2: agentes LOCALES con identidad funcional (nombre = funcionalidad); el
`agente_administrador` conoce al resto a partir de estas fichas.
"""
from __future__ import annotations

FICHAS: dict[str, dict[str, str]] = {
    "agente_machinelearning": {
        "name": "Agente de Machine Learning",
        "description": (
            "Ingeniería de IA y Data Science: recomienda qué técnica de machine learning usar para un "
            "problema, qué métricas mirar y qué modelo elegir según el tipo de dato; consulta su catálogo "
            "de modelos. No programa, no entrena modelos reales ni responde fuera de IA/Data Science. La "
            "biología la deriva a agente_bioinformatica."
        ),
    },
    "agente_mlbioinformatica": {
        "name": "Agente de ML en Bioinformática",
        "description": (
            "IA y Data Science para datos biológicos (secuencias, expresión génica, estructuras, "
            "variantes): recomienda técnica de ML, métricas y modelo, cuidando la partición sin fuga por "
            "homología; consulta su catálogo de modelos. No entrena ni ejecuta, ni interpreta la biología "
            "de fondo (eso es de agente_bioinformatica)."
        ),
    },
    "agente_bioinformatica": {
        "name": "Agente de Bioinformática",
        "description": (
            "Bioinformática: explica conceptos (alineamientos, FASTA/FASTQ, UniProt/NCBI), compara "
            "herramientas y bases de datos con criterios claros y diseña pipelines paso a paso. No ejecuta "
            "análisis ni consulta bases en vivo, y no da consejo médico. El machine learning lo deriva a "
            "agente_mlbioinformatica."
        ),
    },
    "agente_reiki": {
        "name": "Agente de Reiki",
        "description": (
            "Reiki (bienestar complementario): explica los cinco principios (Gokai), las posiciones de "
            "manos, los símbolos y los niveles, con apoyo de búsqueda sobre documentos de Reiki. No da "
            "consejo médico ni diagnósticos; para temas de salud deriva a un profesional."
        ),
    },
    "agente_cocinachilena": {
        "name": "Agente de Cocina Chilena",
        "description": (
            "Cocina chilena: conoce recetas clásicas, muestra sus ingredientes y calcula cuánto cuesta "
            "producir una receta (por ingrediente, total y por persona, en CLP). No responde fuera de la "
            "cocina."
        ),
    },
    "agente_meteorologia": {
        "name": "Agente de Meteorología",
        "description": (
            "Pronóstico del clima para ciudades de Chile: el tiempo de hoy y de los próximos siete días "
            "(temperaturas en °C y condiciones), con historial de pronósticos y comparación de lo "
            "pronosticado con lo observado. No responde fuera de la meteorología ni para ciudades sin "
            "datos. Horas en America/Santiago."
        ),
    },
    "agente_viajes": {
        "name": "Agente de Viajes",
        "description": (
            "Búsqueda de viajes: vuelos y hoteles (SCL, LIM, BOG, EZE) con precios en CLP. No gestiona "
            "pagos ni seguros."
        ),
    },
    "agente_administrador": {
        "name": "Agente Administrador",
        "description": (
            "Recepción y orientación del sistema de agentes: conoce las habilidades de todos los demás y, "
            "en español, da la bienvenida, dice qué agentes hay, qué hace cada uno y a quién conviene "
            "preguntarle según la necesidad. No resuelve la consulta especializada él mismo: orienta y "
            "deriva."
        ),
    },
}
