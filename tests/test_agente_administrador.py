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
    preferencias_usuario,
    recordar_preferencias,
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


def test_perfil_nombre_idioma_saludo(tmp_path, monkeypatch):
    """Prueba: nombre, idioma y saludo se guardan/recuperan por usuario (durable), por separado."""
    monkeypatch.setenv("MEMORIA_DB", str(tmp_path / "m.sqlite"))
    from src.memoria import bd
    importlib.reload(bd)
    # guarda solo nombre
    assert recordar_preferencias.invoke({"usuario": "ezequiel", "nombre": "Eze"})["ok"] is True
    # luego idioma y saludo, sin pisar el nombre
    recordar_preferencias.invoke({"usuario": "ezequiel", "idioma": "inglés", "saludo": "wena"})
    p = preferencias_usuario.invoke({"usuario": "ezequiel"})
    assert p["nombre"] == "Eze" and p["idioma"] == "inglés" and p["saludo"] == "wena"
    # usuario sin perfil: todo None (idioma None ⇒ español por defecto)
    vacio = preferencias_usuario.invoke({"usuario": "gustavo"})
    assert vacio["nombre"] is None and vacio["idioma"] is None and vacio["saludo"] is None
