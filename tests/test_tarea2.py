# --8<-- encabezado-grupo
# Archivo: tests/test_tarea2.py
# Objetivo: Pruebas de las piezas nuevas de la Tarea 2 sin secretos ni red (API_KEY, memoria, clima, fichas, admin, correo).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1811
# Última modificación: 20261117 1811
# --8<-- fin-encabezado-grupo

"""Pruebas rápidas y deterministas (sin GOOGLE_API_KEY ni red) de lo construido en T2.

Cubre: validación de API_KEY, memoria SQLite (allowlist/despachos/accesos/historial), catálogo de
ciudades y mapeo WMO, persistencia de clima, fichas (8 agentes), herramientas del administrador y
composición/allowlist del correo. No llama a Gemini ni a Open-Meteo (se prueban las partes offline).
"""
import importlib


def test_api_key_clave_valida():
    from src.api import claves
    assert claves.clave_valida("abc123", "abc123") is True
    assert claves.clave_valida("abc123", "otra") is False
    assert claves.clave_valida(None, "abc123") is False
    assert claves.clave_valida("abc123", "") is False


def test_memoria(tmp_path, monkeypatch):
    monkeypatch.setenv("MEMORIA_DB", str(tmp_path / "m.sqlite"))
    from src.memoria import bd
    importlib.reload(bd)
    # allowlist
    bd.registrar_destinatario("  Uno@Example.com ", "Uno")
    assert bd.es_destinatario_permitido("uno@example.com") is True
    assert bd.es_destinatario_permitido("no@example.com") is False
    assert bd.baja_destinatario("uno@example.com") is True
    assert bd.es_destinatario_permitido("uno@example.com") is False
    # despachos
    bd.registrar_despacho("uno@example.com", "Asunto", "enviado")
    assert bd.despachos()[0]["estado"] == "enviado"
    # historial
    bd.guardar_mensaje("s1", "usuario", "hola")
    assert bd.historial("s1")[0]["contenido"] == "hola"
    # accesos + resumen
    bd.registrar_acceso("/agentes", "GET", 401, False)
    bd.registrar_acceso("/agentes", "GET", 200, True)
    r = bd.resumen_accesos()
    assert r["total"] == 2 and r["permitido"] == 1 and r["rechazado"] == 1


def test_ciudades():
    from src.agente_meteorologia import ciudades
    assert ciudades.normalizar("  Concepción ") == "concepcion"
    assert ciudades.coords("Santiago") == (-33.4489, -70.6693)
    assert ciudades.coords("Gotham") is None
    assert "Valdivia" in ciudades.listado()


def test_wmo_condicion():
    from src.agente_meteorologia import openmeteo
    assert openmeteo.condicion(0) == "Despejado"
    assert openmeteo.condicion(95) == "Tormenta"
    assert openmeteo.condicion(None) == "—"


def test_bd_clima(tmp_path, monkeypatch):
    monkeypatch.setenv("CLIMA_DB", str(tmp_path / "c.sqlite"))
    from src.agente_meteorologia import bd_clima
    importlib.reload(bd_clima)
    dias = [{"fecha": "2026-11-17", "min_c": 13.9, "max_c": 22.9, "precip_mm": 8.6, "codigo": 95, "condicion": "Tormenta"}]
    assert bd_clima.guardar_pronostico("santiago", "2026-11-17", dias) == 1
    row = bd_clima.pronostico_guardado("santiago", "2026-11-17")
    assert row[2] == 22.9  # max_c
    bd_clima.guardar_observado("santiago", {"fecha": "2026-11-07", "min_c": 8.5, "max_c": 26.1, "precip_mm": 0.0, "codigo": 1, "condicion": "Mayormente despejado"})
    assert bd_clima.observado_guardado("santiago", "2026-11-07")[1] == 26.1


def test_fichas_ocho_agentes():
    from src.fichas import FICHAS
    assert len(FICHAS) == 8
    for g in ("agente_machinelearning", "agente_meteorologia", "agente_administrador"):
        assert g in FICHAS and FICHAS[g]["name"] and FICHAS[g]["description"]


def test_administrador_tools():
    from src.agente_administrador import herramientas as h
    lista = h.listar_agentes.invoke({})
    ids = {a["agente"] for a in lista}
    assert "agente_administrador" not in ids  # no se lista a sí mismo
    assert "agente_reiki" in ids and len(lista) == 7
    d = h.describir_agente.invoke({"nombre": "agente_reiki"})
    assert d["agente"] == "agente_reiki"
    assert "error" in h.describir_agente.invoke({"nombre": "agente_inexistente"})


def test_correo(tmp_path, monkeypatch):
    monkeypatch.setenv("MEMORIA_DB", str(tmp_path / "m2.sqlite"))
    from src.memoria import bd
    importlib.reload(bd)
    from src.canales import correo, grafo_imagen
    importlib.reload(correo)
    # composición: HTML con ruta + grafo
    html, texto = correo.componer("clima?", "Hoy 22.9°C", ["supervisor", "agente_local"], "agente_meteorologia")
    assert "Ruta de los agentes" in html and "Grafo del coordinador" in html
    assert "supervisor" in texto
    # allowlist: a un no registrado -> rechazado (no toca SMTP ni red)
    res = correo.enviar("nadie@x.com", "A", "q", "r", ["supervisor"], "agente_meteorologia")
    assert res["ok"] is False and "allowlist" in res["error"]
    # registrado pero sin SMTP (evitamos red del grafo con monkeypatch) -> no_configurado
    monkeypatch.setattr(grafo_imagen, "png_coordinador", lambda: None)
    bd.registrar_destinatario("dest@etmk.cl", "Dest")
    res2 = correo.enviar("dest@etmk.cl", "A", "q", "r", ["supervisor"], "agente_meteorologia")
    assert res2["ok"] is False and "no configurado" in res2["error"]


def test_convertir_rechaza_monto_absurdo(monkeypatch):
    # fallo 1 (fallos.md): 1e308 CLP rompía al Agente de Viajes con TypeError
    from src.agente_viajes import clientes
    monkeypatch.setattr(clientes, "_get", lambda *a, **k: {"result": "success", "rates": {"USD": 0.001}})
    assert clientes.convertir(float("inf"), "CLP", "USD") is None
    assert clientes.convertir(1e308, "CLP", "USD") is None
    assert clientes.convertir(1000, "CLP", "USD")["resultado"] == 1.0


def test_consulta_rechaza_pregunta_vacia():
    # fallo 3 (fallos.md): una pregunta vacía llegaba al Administrador
    import pytest
    from pydantic import ValidationError
    from src.api.app import Consulta
    for vacia in ("", "   "):
        with pytest.raises(ValidationError):
            Consulta(pregunta=vacia)
    assert Consulta(pregunta="  hola ").pregunta == "hola"


def test_web_cabeceras_seguridad(tmp_path, monkeypatch):
    # fallo 6 (fallos.md): faltaban X-Frame-Options/nosniff y se veía la versión de Python
    import threading
    import urllib.request
    from http.server import ThreadingHTTPServer
    monkeypatch.setenv("USUARIOS_DB", str(tmp_path / "u.sqlite"))
    monkeypatch.setenv("MEMORIA_DB", str(tmp_path / "m.sqlite"))
    from src.canales import web
    srv = ThreadingHTTPServer(("127.0.0.1", 0), web.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{srv.server_port}/login") as r:
            h = r.headers
        assert h["X-Frame-Options"] == "DENY"
        assert h["X-Content-Type-Options"] == "nosniff"
        assert "Python" not in h["Server"]
    finally:
        srv.shutdown()


def test_ultimo_agente_memoria_durable(tmp_path, monkeypatch):
    # memoria de corto plazo durable: el seguimiento lee el agente del ultimo turno del store
    monkeypatch.setenv("MEMORIA_DB", str(tmp_path / "m.sqlite"))
    import importlib
    from src.memoria import bd as memoria
    importlib.reload(memoria)
    hilo = "ezequiel:sesionX"
    memoria.guardar_mensaje(hilo, "usuario", "voy a Lima, que moneda?")
    memoria.guardar_mensaje(hilo, "asistente", "[Agente de Viajes] Sol peruano", agente="Agente de Viajes")
    memoria.guardar_mensaje(hilo, "usuario", "y en Santiago?")
    assert memoria.ultimo_agente(hilo) == "Agente de Viajes"
    assert memoria.ultimo_agente("hilo:inexistente") is None
