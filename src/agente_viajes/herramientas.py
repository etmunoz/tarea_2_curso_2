# --8<-- encabezado-grupo
# Archivo: src/agente_viajes/herramientas.py
# Objetivo: Herramientas del agente de viajes: datos REALES de destino (sin API key) + estimador demo.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261110 1514
# Última modificación: 20261118 1240
# --8<-- fin-encabezado-grupo

"""Herramientas del agente de viajes.

REALES (APIs públicas sin API key): `info_destino`, `tipo_cambio`, `convertir_moneda`,
`clima_destino`, `resumen_destino`. DEMO (datos de ejemplo, no precios reales): `buscar_vuelos`,
`buscar_hoteles`, `buscar_actividades` — se declaran como estimación de demostración.
"""
from langchain_core.tools import tool

from src.agente_meteorologia import openmeteo
from src.agente_viajes import clientes

VUELOS = {
    ("SCL", "LIM"): [{"aerolinea": "LATAM", "sale": "08:10", "llega": "10:05", "precio_clp": 189990},
                     {"aerolinea": "SKY", "sale": "15:40", "llega": "17:35", "precio_clp": 142990}],
    ("SCL", "BOG"): [{"aerolinea": "Avianca", "sale": "07:30", "llega": "12:15", "precio_clp": 329990},
                     {"aerolinea": "LATAM", "sale": "22:50", "llega": "03:40", "precio_clp": 298990}],
    ("SCL", "EZE"): [{"aerolinea": "JetSMART", "sale": "06:00", "llega": "08:15", "precio_clp": 99990}],
}
HOTELES = {
    "LIM": [{"hotel": "Hotel B", "zona": "Barranco", "estrellas": 5, "noche_clp": 210000},
            {"hotel": "Selina Miraflores", "zona": "Miraflores", "estrellas": 3, "noche_clp": 58000}],
    "BOG": [{"hotel": "Four Seasons Casa Medina", "zona": "Chapinero", "estrellas": 5, "noche_clp": 320000},
            {"hotel": "Hotel 93 Luxury Suites", "zona": "Parque 93", "estrellas": 4, "noche_clp": 95000}],
    "EZE": [{"hotel": "Palacio Duhau", "zona": "Recoleta", "estrellas": 5, "noche_clp": 390000},
            {"hotel": "Hotel Madero", "zona": "Puerto Madero", "estrellas": 4, "noche_clp": 120000}],
}
ACTIVIDADES = {
    "LIM": [{"actividad": "Tour gastronómico en Barranco", "tipo": "gastronomía", "horas": 4, "precio_clp": 45000},
            {"actividad": "City tour Centro Histórico", "tipo": "cultural", "horas": 3, "precio_clp": 28000}],
    "BOG": [{"actividad": "Cerro de Monserrate", "tipo": "naturaleza", "horas": 3, "precio_clp": 32000},
            {"actividad": "Museo del Oro + La Candelaria", "tipo": "cultural", "horas": 4, "precio_clp": 25000}],
    "EZE": [{"actividad": "Show de tango en San Telmo", "tipo": "espectáculo", "horas": 3, "precio_clp": 60000},
            {"actividad": "Tour por Recoleta y Palermo", "tipo": "cultural", "horas": 4, "precio_clp": 38000}],
}


@tool
def info_destino(ciudad: str) -> dict:
    """Datos del destino: ciudad, país, región, zona horaria, coordenadas y población EN VIVO
    (Open-Meteo Geocoding, sin API key); capital, moneda (ISO) e idiomas desde una tabla de referencia
    incluida. Devuelve un dict con esos campos, o una nota si no ubica la ciudad."""
    try:
        geo = clientes.geocodificar(ciudad)
        if not geo:
            return {"nota": f"No ubiqué la ciudad «{ciudad}»."}
        pais = clientes.pais_info(geo["cc"]) if geo.get("cc") else None
        datos = {"ciudad": geo["nombre"], "pais": geo["pais"], "region": geo.get("region"),
                 "lat": geo["lat"], "lon": geo["lon"], "zona_horaria": geo["timezone"],
                 "poblacion": geo.get("poblacion")}
        if pais:
            datos.update({"capital": pais["capital"], "moneda": pais["moneda_codigo"],
                          "idiomas": pais["idiomas"]})
        return datos
    except Exception as exc:  # noqa: BLE001
        return {"nota": f"No pude obtener datos del destino ({type(exc).__name__})."}


@tool
def tipo_cambio(moneda: str) -> dict:
    """Tipo de cambio REAL: cuántos pesos chilenos (CLP) equivale 1 unidad de `moneda` (código ISO,
    p. ej. USD, PEN, ARS, EUR). Fuente pública sin API key. Devuelve {moneda, clp_por_unidad} o nota."""
    try:
        clp = clientes.clp_por_unidad(moneda)
    except Exception as exc:  # noqa: BLE001
        return {"nota": f"No pude obtener el tipo de cambio ({type(exc).__name__})."}
    if clp is None:
        return {"nota": f"No tengo tipo de cambio para «{moneda}». Usa un código ISO (USD, PEN, ARS…)."}
    return {"moneda": moneda.upper(), "clp_por_unidad": round(clp, 2)}


@tool
def convertir_moneda(monto: float, desde: str, hacia: str) -> dict:
    """Convierte un `monto` de la moneda `desde` a la moneda `hacia` con tasa REAL (códigos ISO, p. ej.
    CLP, USD, PEN). Fuente pública sin API key. Devuelve {monto, desde, hacia, tasa, resultado} o nota."""
    try:
        r = clientes.convertir(monto, desde, hacia)
    except Exception as exc:  # noqa: BLE001
        return {"nota": f"No pude convertir ({type(exc).__name__})."}
    return r or {"nota": f"No pude convertir de «{desde}» a «{hacia}» (revisa los códigos ISO)."}


@tool
def clima_destino(ciudad: str, dias: int = 3) -> dict:
    """Clima REAL del destino (hoy + próximos días) para saber qué llevar. Ubica la ciudad y consulta
    Open-Meteo (sin API key). Devuelve {ciudad, actual, dias:[...]} o una nota."""
    try:
        geo = clientes.geocodificar(ciudad)
        if not geo:
            return {"nota": f"No ubiqué la ciudad «{ciudad}»."}
        p = openmeteo.pronostico(geo["lat"], geo["lon"], dias=dias)
        return {"ciudad": geo["nombre"], "pais": geo["pais"], **p}
    except Exception as exc:  # noqa: BLE001
        return {"nota": f"No pude obtener el clima del destino ({type(exc).__name__})."}


@tool
def resumen_destino(ciudad: str) -> dict:
    """Resumen REAL del destino (descripción breve) desde Wikipedia en español (sin API key).
    Devuelve {titulo, resumen, url} o una nota si no hay artículo."""
    try:
        r = clientes.resumen(ciudad)
    except Exception as exc:  # noqa: BLE001
        return {"nota": f"No pude obtener el resumen ({type(exc).__name__})."}
    return r or {"nota": f"No encontré un resumen de «{ciudad}» en Wikipedia."}


@tool
def buscar_vuelos(origen: str, destino: str, fecha: str) -> list[dict]:
    """DEMO (datos de ejemplo, NO precios reales). Vuelos entre dos aeropuertos (IATA: SCL, LIM, BOG, EZE)
    para una fecha AAAA-MM-DD: aerolínea, horarios y precio CLP. Preséntalo como estimación de ejemplo."""
    return [dict(v, origen=origen.upper(), destino=destino.upper(), fecha=fecha, fuente="demo")
            for v in VUELOS.get((origen.upper(), destino.upper()), [])]


@tool
def buscar_hoteles(ciudad: str, noches: int = 1) -> list[dict]:
    """DEMO (datos de ejemplo, NO precios reales). Hoteles en una ciudad (IATA: LIM, BOG, EZE): hotel,
    zona, estrellas, precio por noche y total CLP. Preséntalo como estimación de ejemplo."""
    return [dict(h, noches=noches, total_clp=h["noche_clp"] * noches, fuente="demo")
            for h in HOTELES.get(ciudad.upper(), [])]


@tool
def buscar_actividades(ciudad: str) -> list[dict]:
    """DEMO (datos de ejemplo). Actividades y panoramas en una ciudad (IATA: LIM, BOG, EZE): actividad,
    tipo, duración en horas y precio CLP. Preséntalo como sugerencias de ejemplo."""
    return [dict(a, fuente="demo") for a in ACTIVIDADES.get(ciudad.upper(), [])]


# El CLIMA del destino lo da el agente meteo_mcp (Opción "clima resiliente"): viajes NO expone
# clima_destino para no solapar el ruteo; la función queda definida pero sin publicar como herramienta.
HERRAMIENTAS = [
    info_destino, tipo_cambio, convertir_moneda, resumen_destino,  # reales
    buscar_vuelos, buscar_hoteles, buscar_actividades,             # demo
]
