# --8<-- encabezado-grupo
# Archivo: tests/test_agente_administrador.py
# Objetivo: Pruebas del administrador: saludo por hora (Santiago) + recordar/obtener nombre (durable).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261119 1110 · Última modificación: 20261119 1110
# --8<-- fin-encabezado-grupo

"""Pruebas del agente administrador (sin API key ni servidor)."""
import importlib

from src.agente_administrador.herramientas import (
    _franja,
    nombre_usuario,
    recordar_nombre,
    saludo_hora,
)


def test_franja_por_hora():
    """Prueba: la franja de saludo según la hora de Santiago."""
    assert _franja(8) == "buenos días"
    assert _franja(15) == "buenas tardes"
    assert _franja(23) == "buenas noches"
    assert _franja(3) == "buenas noches"


def test_saludo_hora_estructura():
    """Prueba: saludo_hora devuelve saludo válido, hora y fecha."""
    r = saludo_hora.invoke({})
    assert r["saludo"] in ("buenos días", "buenas tardes", "buenas noches")
    assert ":" in r["hora"] and "-" in r["fecha"]


def test_recordar_y_obtener_nombre(tmp_path, monkeypatch):
    """Prueba: el nombre preferido se guarda y se recupera (memoria durable por usuario)."""
    monkeypatch.setenv("MEMORIA_DB", str(tmp_path / "m.sqlite"))
    from src.memoria import bd
    importlib.reload(bd)
    assert recordar_nombre.invoke({"usuario": "ezequiel", "nombre": "Eze"})["ok"] is True
    assert nombre_usuario.invoke({"usuario": "ezequiel"})["nombre"] == "Eze"
    r = nombre_usuario.invoke({"usuario": "gustavo"})
    assert r["nombre"] is None and "nota" in r
