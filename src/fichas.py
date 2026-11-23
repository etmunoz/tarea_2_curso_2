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
            "Meteorología de CHILE con una especialidad distintiva: la VERIFICACIÓN del pronóstico — "
            "guarda sus pronósticos y COMPARA lo pronosticado con lo observado (calidad del pronóstico), "
            "y su historial. También da el tiempo de hoy y 7 días en Chile sin API key (respaldo). Para "
            "el clima general de cualquier ciudad del mundo (o por hora), el agente es meteo_mcp. No "
            "responde fuera de la meteorología. Horas en America/Santiago."
        ),
    },
    "agente_viajes": {
        "name": "Agente de Viajes",
        "description": (
            "Planificación de viajes con datos REALES del destino (sin API key): país, capital, moneda, "
            "idiomas y zona horaria (info_destino), tipo de cambio y conversión a/desde CLP, y un resumen "
            "del lugar (Wikipedia). Además una estimación DEMO de vuelos, hoteles y actividades (datos de "
            "ejemplo). El CLIMA del destino NO lo da este agente: deriva a meteo_mcp. No gestiona pagos, "
            "seguros ni visas."
        ),
    },
    "agente_administrador": {
        "name": "Agente Administrador",
        "description": (
            "Recepción y orientación del sistema de agentes (se llama «tarea2curso2»): da la bienvenida "
            "saludando según la hora de Santiago, recuerda el nombre del usuario (y lo pregunta si no lo "
            "sabe), conoce las habilidades de todos los demás y dice qué agentes hay y a quién conviene "
            "preguntarle. También atiende saludos, cortesías y despedidas. No resuelve la consulta "
            "especializada él mismo: orienta y deriva."
        ),
    },
    "meteo_mcp": {
        "name": "meteo_mcp",
        "description": (
            "Clima MUNDIAL en vivo (servidor MCP de Meteosource): pronóstico de cualquier ciudad del "
            "mundo —hoy, próximos días por hora e histórico de hasta 7 días—. Es el agente de clima POR "
            "DEFECTO para cualquier país (incluido Chile). Si el servicio no está disponible, responde "
            "igual con una fuente de respaldo keyless (Open-Meteo). No responde temas ajenos a la "
            "meteorología ni inventa datos."
        ),
    },
}
