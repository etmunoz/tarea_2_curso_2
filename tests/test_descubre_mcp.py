# --8<-- encabezado-grupo
# Archivo: tests/test_descubre_mcp.py
# Objetivo: Prueba offline del formato de salida del descubridor MCP.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261122 0000
# Última modificación: 20261122 0000
# --8<-- fin-encabezado-grupo

"""Valida la tabla sin conexión a Meteosource."""
from types import SimpleNamespace

from scripts.descubre_mcp import _primer_place_id, formatear_herramientas


def test_formato_tabla_ordenada_y_argumentos():
    herramientas = [
        SimpleNamespace(
            name="zeta",
            description="Segunda línea no debe aparecer.\nDetalle adicional.",
            inputSchema={"type": "object", "properties": {}},
        ),
        SimpleNamespace(
            name="alfa",
            description="Primera línea.\nDescripción extendida.",
            inputSchema={
                "type": "object",
                "properties": {
                    "dias": {"type": "integer"},
                    "ciudad": {"type": "string"},
                },
                "required": ["ciudad"],
            },
        ),
    ]

    tabla = formatear_herramientas(herramientas)
    lineas = tabla.splitlines()

    assert lineas[0] == "HERRAMIENTAS MCP METEOSOURCE (2)"
    assert lineas.index("1. alfa") < lineas.index("2. zeta")
    assert "Primera línea." in tabla
    assert "Descripción extendida." not in tabla
    assert "ciudad: string (obligatorio)" in tabla
    assert "dias: integer" in tabla
    assert "   Argumentos:" in tabla


def test_acepta_input_schema_del_sdk_mcp_23():
    herramienta = SimpleNamespace(
        name="pronostico",
        description="Pronóstico.",
        input_schema={
            "type": "object",
            "properties": {"dias": {"type": "integer"}},
            "required": ["dias"],
        },
    )

    tabla = formatear_herramientas([herramienta])

    assert "dias: integer (obligatorio)" in tabla


def test_extrae_place_id_de_search_places():
    respuesta = '[{"name": "Berlin", "place_id": "berlin"}]'

    assert _primer_place_id(respuesta) == "berlin"
    assert _primer_place_id("respuesta no JSON") is None
