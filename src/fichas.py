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
            "Ingeniería de IA y Data Science (datos generales/tabulares): recomienda qué técnica de "
            "machine learning usar para un problema, qué métricas mirar y qué modelo elegir según el tipo "
            "de dato; consulta su catálogo de modelos. No programa ni entrena modelos reales. El ML "
            "aplicado a datos biológicos lo deriva a agente_mlbioinformatica y la biología de fondo a "
            "agente_bioinformatica."
        ),
    },
    "agente_mlbioinformatica": {
        "name": "Agente de ML en Bioinformática",
        "description": (
            "IA y Data Science aplicada a datos biológicos (secuencias, expresión génica, estructuras, "
            "variantes): arma PIPELINES de ML de punta a punta por tipo de dato (preprocesamiento, "
            "partición sin fuga por homología, modelo, métricas y la trampa a evitar) y recomienda "
            "técnica, métricas y modelo; consulta su catálogo de modelos. No entrena ni ejecuta, ni "
            "interpreta la biología de fondo (eso es de agente_bioinformatica)."
        ),
    },
    "agente_bioinformatica": {
        "name": "Agente de Bioinformática",
        "description": (
            "Bioinformática: CONSULTA UniProt EN VIVO datos de una proteína o gen (p. ej. TP53, BRCA1, "
            "insulina, accession P04637) devolviendo accession, función, longitud, organismo y URL; "
            "además explica conceptos (alineamientos, FASTA/FASTQ, UniProt/NCBI), compara herramientas y "
            "bases de datos y diseña pipelines paso a paso. No ejecuta análisis ni da consejo médico. El "
            "machine learning lo deriva a agente_mlbioinformatica."
        ),
    },
    "agente_reiki": {
        "name": "Agente de Reiki",
        "description": (
            "Reiki y bienestar complementario: explica los cinco principios (Gokai), las posiciones de "
            "manos, los símbolos y los niveles, y RECOMIENDA terapias holísticas complementarias por "
            "objetivo de bienestar (relajación y estrés, sueño, ánimo, energía, tensión corporal, duelo, "
            "concentración y cefalea/dolor de cabeza tensional), con apoyo de búsqueda sobre documentos "
            "de Reiki. Es apoyo de bienestar, NO consejo médico ni diagnóstico; ante enfermedades o "
            "tratamientos deriva a un profesional."
        ),
    },
    "agente_cocinachilena": {
        "name": "Agente de Cocina Chilena",
        "description": (
            "Cocina chilena: conoce recetas clásicas, muestra ingredientes, calcula cuánto cuesta "
            "producir una receta (por ingrediente, total y por persona, en CLP), recomienda recetas por "
            "restricción (vegetariano, vegano, sin gluten, económica) y da una estimación nutricional "
            "aproximada (kcal). No responde fuera de la cocina."
        ),
    },
    "agente_meteorologia": {
        "name": "Agente de Meteorología",
        "description": (
            "Pronóstico del clima para ciudades de CHILE únicamente: el tiempo de hoy y de los próximos "
            "siete días (temperaturas en °C y condiciones), con historial de pronósticos y comparación de "
            "lo pronosticado con lo observado. Para clima de ciudades de otros países, deriva a "
            "agente_viajes. No responde fuera de la meteorología. Horas en America/Santiago."
        ),
    },
    "agente_viajes": {
        "name": "Agente de Viajes",
        "description": (
            "Planificación de viajes con datos REALES del destino (sin API key): país, capital, moneda, "
            "idiomas y zona horaria (info_destino), tipo de cambio y conversión a/desde CLP, el CLIMA de "
            "una ciudad de CUALQUIER país del mundo para el viaje (clima_destino) y un resumen del lugar "
            "(Wikipedia). Además una estimación DEMO de vuelos, hoteles y actividades (datos de ejemplo). "
            "Para clima fuera de Chile, este es el agente (meteorología es solo Chile). No gestiona pagos, "
            "seguros ni visas."
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
