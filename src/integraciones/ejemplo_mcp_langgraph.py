# --8<-- encabezado-grupo
# Archivo: src/integraciones/ejemplo_mcp_langgraph.py
# Objetivo: Ejemplo de uso del adaptador MCP como herramientas LangGraph.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261122 0000
# Última modificación: 20261122 0000
# --8<-- fin-encabezado-grupo

"""Ejemplo no ejecutado automáticamente de integración MCP + LangGraph.

La sesión debe envolver la vida completa del agente: cerrar el context manager
antes de terminar el agente invalidaría las herramientas remotas.
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from langchain.agents import create_agent

from src.integraciones.mcp_langchain import ClienteMCP


@asynccontextmanager
async def herramientas_meteosource():
    """Entrega herramientas MCP manteniendo viva la sesión remota."""
    async with ClienteMCP.conectar_meteosource() as conexion:
        yield await conexion.herramientas_langchain()


async def consultar_meteosource(modelo: object, pregunta: str):
    """Ejemplo de ejecución; el modelo debe ser un ChatModel de LangChain."""
    async with herramientas_meteosource() as herramientas:
        agente = create_agent(model=modelo, tools=herramientas)
        return await agente.ainvoke({"messages": [{"role": "user", "content": pregunta}]})
