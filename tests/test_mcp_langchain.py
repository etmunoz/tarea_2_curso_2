# --8<-- encabezado-grupo
# Archivo: tests/test_mcp_langchain.py
# Objetivo: Pruebas offline del adaptador MCP oficial hacia StructuredTool.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261122 0000
# Última modificación: 20261122 0000
# --8<-- fin-encabezado-grupo

"""Pruebas deterministas del adaptador propio MCP/LangChain."""
from __future__ import annotations

import asyncio
from types import SimpleNamespace

from pydantic import BaseModel

import src.integraciones.mcp_langchain as modulo_mcp
from src.integraciones.mcp_langchain import ClienteMCP


class SesionFalsa:
    """Servidor MCP simulado, sin red ni proceso externo."""

    def __init__(self):
        self.inicializaciones = 0
        self.llamadas: list[tuple[str, dict]] = []

    async def initialize(self):
        self.inicializaciones += 1
        return SimpleNamespace()

    async def list_tools(self):
        return SimpleNamespace(
            tools=[
                SimpleNamespace(
                    name="buscar_clima",
                    description="Busca el clima de una ciudad.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "ciudad": {
                                "type": "string",
                                "description": "Ciudad a consultar.",
                            },
                            "dias": {"type": "integer", "default": 1},
                        },
                        "required": ["ciudad"],
                    },
                )
            ]
        )

    async def call_tool(self, nombre, arguments):
        self.llamadas.append((nombre, arguments))
        if arguments.get("ciudad") == "error":
            raise RuntimeError("fallo simulado")
        return SimpleNamespace(
            isError=False,
            content=[SimpleNamespace(type="text", text=f"Clima de {arguments['ciudad']}")],
        )


def test_descubrimiento_y_conversion_a_structured_tool():
    sesion = SesionFalsa()
    cliente = ClienteMCP(sesion)

    herramientas = asyncio.run(cliente.herramientas_langchain())

    assert len(herramientas) == 1
    assert herramientas[0].name == "buscar_clima"
    assert herramientas[0].description == "Busca el clima de una ciudad."
    assert issubclass(herramientas[0].args_schema, BaseModel)
    assert "ciudad" in herramientas[0].args_schema.model_fields
    assert sesion.inicializaciones == 1


def test_ejecucion_de_herramienta_adaptada():
    sesion = SesionFalsa()
    herramienta = asyncio.run(ClienteMCP(sesion).herramientas_langchain())[0]

    resultado = asyncio.run(herramienta.ainvoke({"ciudad": "Santiago", "dias": 2}))

    assert resultado == "Clima de Santiago"
    assert sesion.llamadas == [("buscar_clima", {"ciudad": "Santiago", "dias": 2})]


def test_error_de_herramienta_se_devuelve_como_texto():
    sesion = SesionFalsa()
    herramienta = asyncio.run(ClienteMCP(sesion).herramientas_langchain())[0]

    resultado = asyncio.run(herramienta.ainvoke({"ciudad": "error"}))

    assert "Error al ejecutar la herramienta MCP" in resultado
    assert "fallo simulado" in resultado


def test_inicializacion_no_se_repite():
    sesion = SesionFalsa()
    cliente = ClienteMCP(sesion)

    async def ejercicio():
        await cliente.inicializar()
        await cliente.inicializar()
        await cliente.listar_herramientas()

    asyncio.run(ejercicio())
    assert sesion.inicializaciones == 1


def test_conexion_stdio_cierra_transporte_y_sesion(monkeypatch):
    estado = {"transporte_cerrado": False, "sesion_cerrada": False}

    class TransporteFalso:
        async def __aenter__(self):
            return ("entrada", "salida")

        async def __aexit__(self, *_):
            estado["transporte_cerrado"] = True

    class SesionContextual(SesionFalsa):
        async def __aenter__(self):
            return self

        async def __aexit__(self, *_):
            estado["sesion_cerrada"] = True

    monkeypatch.setattr(modulo_mcp, "stdio_client", lambda *_: TransporteFalso())
    monkeypatch.setattr(
        modulo_mcp,
        "ClientSession",
        lambda *_: SesionContextual(),
    )

    async def ejercicio():
        async with ClienteMCP.conectar_stdio("servidor-mcp") as cliente:
            await cliente.listar_herramientas()

    asyncio.run(ejercicio())
    assert estado == {"transporte_cerrado": True, "sesion_cerrada": True}


def test_token_bearer_directo_y_referenciado(monkeypatch):
    monkeypatch.setenv("MCP_BEARER_TOKEN_ENV_VAR", "token-directo")
    assert modulo_mcp._resolver_token_bearer() == "token-directo"

    monkeypatch.setenv("MCP_BEARER_TOKEN_ENV_VAR", "NOMBRE_DEL_TOKEN")
    monkeypatch.setenv("NOMBRE_DEL_TOKEN", "token-referenciado")
    assert modulo_mcp._resolver_token_bearer() == "token-referenciado"


def test_version_oficial_mcp_compatible():
    import importlib.metadata

    version = importlib.metadata.version("mcp")
    assert version == "2.3.0"
