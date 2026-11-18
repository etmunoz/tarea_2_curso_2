# --8<-- encabezado-grupo
# Archivo: src/agente_reiki/herramientas.py
# Objetivo: Herramientas del agente de Tomás · Maestro Reiki.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261110 1952
# Última modificación: 20261111 2049
# --8<-- fin-encabezado-grupo

"""Herramientas del agente de Tomás · Maestro Reiki.

Datos simulados pero coherentes dentro del archivo (como el molde de viajes). El
Reiki es una práctica complementaria de bienestar: estas herramientas informan sobre
principios, posiciones de manos y símbolos; **no dan consejo médico**. Si piden algo
fuera del tema, la herramienta lo dice en UNA línea; nunca lanza un error.
"""
from __future__ import annotations

import unicodedata

from langchain_core.tools import tool

from src.agente_reiki import rag


def _norm(texto: str) -> str:
    """Objetivo: normalizar texto (minúsculas, sin acentos) para comparar.
    Entradas: texto (str). Salida: str normalizado."""
    t = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


# Los cinco principios (Gokai)
PRINCIPIOS = [
    "Solo por hoy, no te enojes.",
    "Solo por hoy, no te preocupes.",
    "Solo por hoy, sé agradecido.",
    "Solo por hoy, trabaja con honestidad.",
    "Solo por hoy, sé amable contigo y con los demás.",
]

# Posiciones de manos por zona (autotratamiento, simuladas)
POSICIONES = {
    "cabeza": ["corona", "sienes", "nuca", "frente y occipucio"],
    "cara": ["ojos", "mejillas y mandíbula", "oídos"],
    "garganta": ["base del cuello (sin presionar)", "nuca"],
    "pecho": ["centro del pecho (timo)", "zona del corazón", "costados"],
    "abdomen": ["plexo solar", "ombligo", "bajo vientre"],
    "espalda": ["hombros", "zona media (riñones)", "zona lumbar"],
}

# Símbolos (nivel y para qué), simulados
SIMBOLOS = {
    "cho ku rei": {"nivel": "II", "para_que": "enfocar y aumentar la energía; 'botón de encendido'"},
    "sei he ki": {"nivel": "II", "para_que": "equilibrio emocional y mental; armonizar hábitos"},
    "hon sha ze sho nen": {"nivel": "II", "para_que": "enviar Reiki a distancia (tiempo/espacio)"},
    "dai ko myo": {"nivel": "III (Maestría)", "para_que": "símbolo maestro; iniciaciones y sanación profunda"},
}

NIVELES = {
    "i": "Nivel I (Shoden): autotratamiento y tratamiento presencial; apertura de canales.",
    "ii": "Nivel II (Okuden): los tres símbolos; Reiki a distancia y trabajo mental/emocional.",
    "iii": "Nivel III / Maestría (Shinpiden): símbolo maestro Dai Ko Myo, enseñar e iniciar.",
}

# Terapias holísticas complementarias basadas en Reiki, por objetivo de bienestar.
# Es bienestar COMPLEMENTARIO: no diagnostica, no cura y no reemplaza la atención profesional.
TERAPIAS = {
    "estres": {
        "practicas": [
            "Autotratamiento de Reiki en pecho y plexo solar",
            "Respiración abdominal 4-6 (inhalar 4 · exhalar 6)",
            "Aromaterapia de lavanda (difusión suave)",
            "Principio del día: «solo por hoy, no te preocupes»",
        ],
        "nota": "Para relajarte; si la ansiedad es intensa o persistente, consulta a un profesional.",
    },
    "sueno": {
        "practicas": [
            "Sesión breve de Reiki en nuca y frente",
            "Sonoterapia suave (cuencos o música tranquila)",
            "Rutina de sueño (sin pantallas, ambiente oscuro)",
            "Diario de gratitud antes de dormir",
        ],
        "nota": "Higiene del sueño como apoyo; el insomnio sostenido lo ve un profesional de la salud.",
    },
    "animo": {
        "practicas": [
            "Reiki en el centro del pecho (zona del corazón)",
            "Aromaterapia cítrica (naranja o bergamota)",
            "Caminata consciente al aire libre con luz natural",
            "Principios de gratitud y amabilidad (Gokai)",
        ],
        "nota": "Para acompañar el ánimo; ante tristeza persistente, busca apoyo profesional.",
    },
    "energia": {
        "practicas": [
            "Reiki en plexo solar y bajo vientre",
            "Movimiento suave (yoga suave o estiramientos)",
            "Exposición moderada a luz natural",
            "Hidratación y descanso",
        ],
        "nota": "Para vitalidad cotidiana; el cansancio marcado conviene consultarlo.",
    },
    "tension": {
        "practicas": [
            "Posiciones de manos en hombros, zona media y lumbar",
            "Estiramientos suaves y calor local",
            "Respiración lenta mientras sueltas la zona",
            "Pausa consciente (Gassho) para centrarte",
        ],
        "nota": "Para tensión leve; si el dolor es intenso o persistente, acude a un profesional.",
    },
}
# Sinónimos → objetivo canónico (para que la recomendación encuentre el calce).
SINONIMOS = {
    "ansiedad": "estres", "relajacion": "estres", "calma": "estres",
    "descanso": "sueno", "dormir": "sueno", "insomnio": "sueno",
    "tristeza": "animo", "desanimo": "animo", "humor": "animo",
    "vitalidad": "energia", "cansancio": "energia", "fatiga": "energia",
    "dolor": "tension", "contractura": "tension", "rigidez": "tension",
}


def _buscar(catalogo: dict, consulta: str) -> str | None:
    """Objetivo: encontrar la clave de un catálogo que casa con la consulta (sin acentos).
    Entradas: catalogo (dict), consulta (str). Salida: str (clave) | None."""
    q = _norm(consulta)
    for clave in catalogo:
        if _norm(clave) in q or q in _norm(clave):
            return clave
    palabras = set(q.split())
    for clave in catalogo:
        if palabras & set(_norm(clave).split()):
            return clave
    return None


@tool
def principios_reiki() -> list[str]:
    """Devuelve los cinco principios del Reiki (Gokai), uno por línea."""
    return list(PRINCIPIOS)


@tool
def posiciones_manos(zona: str) -> dict:
    """Posiciones de manos para autotratamiento en una zona del cuerpo.
    Zonas: 'cabeza', 'cara', 'garganta', 'pecho', 'abdomen', 'espalda'.
    Devuelve {zona, posiciones:[...]}. Si no reconoce la zona, lo dice en una línea."""
    clave = _buscar(POSICIONES, zona)
    if not clave:
        return {"nota": f"No tengo posiciones para «{zona}». Zonas: {', '.join(POSICIONES)}."}
    return {"zona": clave, "posiciones": POSICIONES[clave]}


@tool
def info_simbolo(nombre: str) -> dict:
    """Información de un símbolo de Reiki: nivel y para qué se usa.
    Símbolos: 'Cho Ku Rei', 'Sei He Ki', 'Hon Sha Ze Sho Nen', 'Dai Ko Myo'.
    Devuelve {simbolo, nivel, para_que}. Si no lo reconoce, lo dice en una línea."""
    clave = _buscar(SIMBOLOS, nombre)
    if not clave:
        return {"nota": f"No tengo el símbolo «{nombre}». Conozco: {', '.join(s.title() for s in SIMBOLOS)}."}
    return {"simbolo": clave.title(), **SIMBOLOS[clave]}


@tool
def buscar_reiki(consulta: str) -> list[dict] | dict:
    """Busca en los documentos de Reiki (niveles 1 a 4) cargados en el RAG (local o Redis) y
    devuelve los fragmentos más relevantes [{texto, fuente}]. Úsala para responder con
    el material de los documentos (niveles, símbolos, prácticas, iniciaciones). Si el RAG
    no está disponible, lo dice en una línea."""
    try:
        if not rag.disponible():
            if rag.BACKEND == "local":
                rag.cargar()  # construye el índice local embebido la primera vez (requiere GOOGLE_API_KEY)
            else:
                return {"nota": "El RAG (Redis) no está disponible. Levanta Redis y carga con "
                                "tools/cargar_rag_reiki.py, o usa RAG_BACKEND=local (sin Docker)."}
        res = rag.buscar(consulta)
        return res or {"nota": "No encontré fragmentos para esa consulta en los documentos de Reiki."}
    except Exception as exc:  # noqa: BLE001 - reportar sin romper
        return {"nota": f"No pude consultar el RAG: {exc}"}


@tool
def terapias_complementarias(objetivo: str) -> dict:
    """Recomienda terapias holísticas complementarias basadas en Reiki para un objetivo de bienestar.
    Objetivos: 'estrés/ansiedad', 'sueño/descanso', 'ánimo', 'energía/vitalidad', 'tensión corporal'.
    Devuelve {objetivo, practicas:[...], nota}. Es bienestar COMPLEMENTARIO, NO consejo médico ni
    diagnóstico. Si no reconoce el objetivo, sugiere los disponibles en una línea."""
    clave = _buscar(TERAPIAS, objetivo)
    if not clave:
        q = _norm(objetivo)
        for syn, canon in SINONIMOS.items():
            if syn in q:
                clave = canon
                break
    if not clave:
        return {"nota": f"No tengo recomendaciones para «{objetivo}». "
                        f"Objetivos: estrés, sueño, ánimo, energía, tensión corporal."}
    datos = TERAPIAS[clave]
    return {"objetivo": clave, "practicas": datos["practicas"], "nota": datos["nota"]}


HERRAMIENTAS = [principios_reiki, posiciones_manos, info_simbolo, terapias_complementarias, buscar_reiki]
