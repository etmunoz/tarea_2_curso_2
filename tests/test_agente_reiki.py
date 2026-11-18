# --8<-- encabezado-grupo
# Archivo: tests/test_agente_reiki.py
# Objetivo: Pruebas de las herramientas del agente de Tomás (Maestro Reiki). Sin API key ni servidor.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261110 1952
# Última modificación: 20261111 2049
# --8<-- fin-encabezado-grupo

"""Pruebas de las herramientas del agente de Tomás (Maestro Reiki). Sin API key ni servidor."""
from src.agente_reiki.herramientas import (
    info_simbolo,
    posiciones_manos,
    principios_reiki,
    terapias_complementarias,
)


def test_principios_son_cinco():
    """Prueba: principios son cinco."""
    r = principios_reiki.invoke({})
    assert len(r) == 5
    assert all(p.lower().startswith("solo por hoy") for p in r)


def test_posiciones_zona_conocida():
    """Prueba: posiciones zona conocida."""
    r = posiciones_manos.invoke({"zona": "espalda"})
    assert r["zona"] == "espalda" and len(r["posiciones"]) >= 2


def test_posiciones_zona_desconocida():
    """Prueba: posiciones zona desconocida."""
    r = posiciones_manos.invoke({"zona": "rodilla"})
    assert "nota" in r


def test_info_simbolo_distancia():
    """Prueba: info simbolo distancia."""
    r = info_simbolo.invoke({"nombre": "Hon Sha Ze Sho Nen"})
    assert r["nivel"] == "II" and "distancia" in r["para_que"]


def test_tema_ajeno_se_rechaza():
    """Prueba: tema ajeno se rechaza."""
    r = info_simbolo.invoke({"nombre": "bitcoin"})
    assert "nota" in r and "No tengo" in r["nota"]


def test_terapias_objetivo_conocido():
    """Prueba: recomienda terapias para un objetivo conocido."""
    r = terapias_complementarias.invoke({"objetivo": "estrés"})
    assert r["objetivo"] == "estres" and len(r["practicas"]) >= 2 and "nota" in r


def test_terapias_sinonimo():
    """Prueba: un sinónimo (ansiedad) mapea al objetivo canónico (estres)."""
    r = terapias_complementarias.invoke({"objetivo": "tengo mucha ansiedad"})
    assert r["objetivo"] == "estres"


def test_terapias_objetivo_desconocido():
    """Prueba: objetivo sin calce devuelve nota con los disponibles."""
    r = terapias_complementarias.invoke({"objetivo": "programar en rust"})
    assert "nota" in r and "No tengo" in r["nota"]


def test_terapias_duelo():
    """Prueba: 'pérdida' mapea a duelo."""
    r = terapias_complementarias.invoke({"objetivo": "estoy pasando por una pérdida"})
    assert r["objetivo"] == "duelo" and len(r["practicas"]) >= 2


def test_terapias_concentracion():
    """Prueba: 'concentración' mapea a concentracion."""
    r = terapias_complementarias.invoke({"objetivo": "me cuesta la concentración"})
    assert r["objetivo"] == "concentracion"


def test_terapias_cefalea_no_es_tension():
    """Prueba: 'dolor de cabeza tensional' cae en cefalea, no en tensión."""
    r = terapias_complementarias.invoke({"objetivo": "tengo dolor de cabeza tensional"})
    assert r["objetivo"] == "cefalea"
