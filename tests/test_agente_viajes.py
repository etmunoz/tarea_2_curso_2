# --8<-- encabezado-grupo
# Archivo: tests/test_agente_viajes.py
# Objetivo: Pruebas del agente de viajes: tools REALES (parseo con JSON de ejemplo) + degradación.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261118 1240
# Última modificación: 20261118 1240
# --8<-- fin-encabezado-grupo

"""Pruebas del agente de viajes. El acceso a red se simula monkeypatcheando clientes._get, así el
parseo se prueba sin internet. Las tools demo siguen devolviendo datos de ejemplo."""
from src.agente_viajes import clientes
from src.agente_viajes.herramientas import (
    buscar_actividades,
    convertir_moneda,
    info_destino,
    tipo_cambio,
)


def test_geocodificar_parsea(monkeypatch):
    """Prueba: geocodificar arma el dict desde la respuesta de Open-Meteo."""
    ejemplo = {"results": [{"name": "Lima", "country": "Perú", "country_code": "PE",
                            "latitude": -12.04, "longitude": -77.03, "timezone": "America/Lima",
                            "population": 8000000, "admin1": "Lima"}]}
    monkeypatch.setattr(clientes, "_get", lambda *a, **k: ejemplo)
    g = clientes.geocodificar("Lima")
    assert g["nombre"] == "Lima" and g["cc"] == "PE" and g["timezone"] == "America/Lima"


def test_tipo_cambio_parsea(monkeypatch):
    """Prueba: tipo_cambio devuelve los CLP por unidad desde la respuesta de FX."""
    monkeypatch.setattr(clientes, "_get", lambda *a, **k: {"result": "success", "rates": {"CLP": 950.0}})
    r = tipo_cambio.invoke({"moneda": "USD"})
    assert r["moneda"] == "USD" and r["clp_por_unidad"] == 950.0


def test_convertir_moneda(monkeypatch):
    """Prueba: convertir_moneda aplica la tasa."""
    monkeypatch.setattr(clientes, "_get", lambda *a, **k: {"result": "success", "rates": {"USD": 0.001}})
    r = convertir_moneda.invoke({"monto": 10000, "desde": "CLP", "hacia": "USD"})
    assert r["resultado"] == 10.0 and r["hacia"] == "USD"


def test_info_destino_degrada(monkeypatch):
    """Prueba: si la API falla, info_destino devuelve una nota (no rompe)."""
    def _falla(*a, **k):
        raise TimeoutError("sin red")

    monkeypatch.setattr(clientes, "_get", _falla)
    r = info_destino.invoke({"ciudad": "Lima"})
    assert "nota" in r


def test_demo_actividades_marca_fuente():
    """Prueba: las tools demo marcan fuente='demo'."""
    r = buscar_actividades.invoke({"ciudad": "LIM"})
    assert r and all(a["fuente"] == "demo" for a in r)
