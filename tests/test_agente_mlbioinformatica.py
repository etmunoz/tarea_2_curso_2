# --8<-- encabezado-grupo
# Archivo: tests/test_agente_mlbioinformatica.py
# Objetivo: Pruebas de ProteinMAN (ML en bioinformática): la herramienta distintiva recomendar_pipeline.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261118 1150
# Última modificación: 20261118 1150
# --8<-- fin-encabezado-grupo

"""Pruebas de la herramienta distintiva de ProteinMAN: recomendar_pipeline (sin red ni API key)."""
from src.agente_mlbioinformatica.herramientas import recomendar_pipeline


def test_pipeline_secuencias_proteinas():
    """Prueba: el pipeline de secuencias de proteínas evita fuga por homología."""
    r = recomendar_pipeline.invoke({"tipo_de_dato": "secuencias de proteinas"})
    assert r["tipo"] == "secuencias de proteinas"
    assert "identidad" in r["particion"].lower()
    assert "homolog" in r["trampa"].lower()
    assert isinstance(r["metricas"], list) and r["metricas"]


def test_pipeline_expresion_genica():
    """Prueba: expresión génica usa CV anidada y corrige lote dentro del fold."""
    r = recomendar_pipeline.invoke({"tipo_de_dato": "expresion genica"})
    assert r["tipo"] == "expresion genica"
    assert "anidada" in r["particion"].lower() or "fold" in r["preprocesamiento"].lower()


def test_pipeline_desconocido():
    """Prueba: tipo sin catálogo devuelve nota con los disponibles."""
    r = recomendar_pipeline.invoke({"tipo_de_dato": "señales de audio"})
    assert "nota" in r and "No tengo" in r["nota"]
