# --8<-- encabezado-grupo
# Archivo: src/integraciones/mcp_langchain.py
# Objetivo: Adaptador propio entre el SDK MCP 2.3 y las herramientas de LangChain.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261122 0000
# Última modificación: 20261122 0000
# --8<-- fin-encabezado-grupo

"""Cliente MCP asíncrono y adaptador a ``StructuredTool``.

El módulo usa directamente el SDK oficial ``mcp==2.3.0``. No depende de
``langchain-mcp-adapters``. La sesión MCP debe permanecer abierta mientras
las herramientas adaptadas sean utilizadas por un agente LangGraph; por eso
las fábricas de conexión son context managers asíncronos.
"""
from __future__ import annotations

import json
import os
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Literal

import httpx2
from dotenv import load_dotenv
from langchain_core.tools import StructuredTool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client
from pydantic import AnyUrl, BaseModel, ConfigDict, Field, create_model

load_dotenv()


def _esquema_dict(esquema: Any) -> dict[str, Any]:
    """Convierte el esquema MCP a un diccionario JSON serializable."""
    if esquema is None:
        return {"type": "object", "properties": {}}
    if isinstance(esquema, dict):
        return esquema
    if hasattr(esquema, "model_dump"):
        return esquema.model_dump(mode="json")
    return {"type": "object", "properties": {}}


def _resolver_token_bearer(token: str | None = None) -> str:
    """Obtiene el token directo o mediante el nombre de otra variable.

    La configuración histórica del proyecto guarda el token directamente en
    ``MCP_BEARER_TOKEN_ENV_VAR``. También se acepta que esa variable contenga
    el nombre de otra variable, para despliegues donde el secreto se inyecta
    separadamente.
    """
    if token and token.strip():
        return token.strip()
    configurado = os.environ.get("MCP_BEARER_TOKEN_ENV_VAR", "").strip()
    if not configurado:
        raise RuntimeError("Falta configurar el token Bearer de MCP.")
    referido = os.environ.get(configurado, "").strip()
    return referido or configurado


def _anotacion(schema: dict[str, Any]) -> Any:
    """Traduce los tipos JSON habituales a anotaciones Pydantic."""
    if "enum" in schema and schema["enum"]:
        valores = tuple(schema["enum"])
        return Literal[valores]  # type: ignore[valid-type]

    tipos = schema.get("type")
    if isinstance(tipos, list):
        tipos = next((tipo for tipo in tipos if tipo != "null"), "string")

    if tipos == "string":
        return AnyUrl if schema.get("format") == "uri" else str
    if tipos == "integer":
        return int
    if tipos == "number":
        return float
    if tipos == "boolean":
        return bool
    if tipos == "array":
        elementos = schema.get("items", {})
        return list[_anotacion(elementos)] if elementos else list[Any]
    if tipos == "object" or "properties" in schema:
        return dict[str, Any]
    return Any


def esquema_pydantic(nombre: str, esquema: Any) -> type[BaseModel]:
    """Construye un modelo Pydantic desde ``inputSchema`` de una herramienta MCP.

    Se conservan los nombres, tipos básicos, valores por defecto y campos
    obligatorios definidos por el servidor MCP. Las estructuras complejas se
    mantienen como JSON para no perder información del protocolo.
    """
    schema = _esquema_dict(esquema)
    propiedades = schema.get("properties") or {}
    obligatorios = set(schema.get("required") or ())
    campos: dict[str, tuple[Any, Any]] = {}

    for campo, definicion in propiedades.items():
        definicion = definicion if isinstance(definicion, dict) else {}
        if campo in obligatorios:
            default = Field(..., description=definicion.get("description"))
        else:
            default = Field(
                definicion.get("default", None),
                description=definicion.get("description"),
            )
        campos[campo] = (_anotacion(definicion), default)

    nombre_modelo = f"{nombre.replace('-', '_').replace('.', '_').title()}Argumentos"
    return create_model(
        nombre_modelo,
        __config__=ConfigDict(extra="allow"),
        **campos,
    )


def _texto_resultado(resultado: Any) -> str:
    """Normaliza el resultado MCP para entregarlo a LangChain."""
    if getattr(resultado, "isError", False):
        prefijo = "Error MCP"
    else:
        prefijo = ""

    partes: list[str] = []
    for contenido in getattr(resultado, "content", []) or []:
        texto = getattr(contenido, "text", None)
        if texto is not None:
            partes.append(str(texto))
            continue
        datos = getattr(contenido, "data", None)
        if datos is not None:
            partes.append(str(datos))
            continue
        if hasattr(contenido, "model_dump"):
            partes.append(json.dumps(contenido.model_dump(mode="json"), ensure_ascii=False))
        else:
            partes.append(str(contenido))

    if not partes:
        estructurado = getattr(resultado, "structuredContent", None)
        if estructurado is not None:
            partes.append(json.dumps(estructurado, ensure_ascii=False, default=str))
    salida = "\n".join(partes) or "El servidor MCP no devolvió contenido."
    return f"{prefijo}: {salida}" if prefijo else salida


class ClienteMCP:
    """Cliente MCP que expone las herramientas remotas como ``StructuredTool``."""

    def __init__(self, sesion: ClientSession):
        self.sesion = sesion
        self._inicializado = False

    async def inicializar(self) -> Any:
        """Inicializa el protocolo MCP una sola vez."""
        if not self._inicializado:
            resultado = await self.sesion.initialize()
            self._inicializado = True
            return resultado
        return None

    async def listar_herramientas(self) -> list[Any]:
        """Obtiene las herramientas publicadas por el servidor MCP."""
        if not self._inicializado:
            await self.inicializar()
        respuesta = await self.sesion.list_tools()
        return list(getattr(respuesta, "tools", []) or [])

    async def ejecutar(self, nombre: str, argumentos: dict[str, Any]) -> str:
        """Ejecuta una herramienta MCP y devuelve texto útil para el agente."""
        try:
            if not self._inicializado:
                await self.inicializar()
            resultado = await self.sesion.call_tool(nombre, arguments=argumentos)
            return _texto_resultado(resultado)
        except Exception as error:  # noqa: BLE001
            return f"Error al ejecutar la herramienta MCP '{nombre}': {error}"

    async def herramientas_langchain(self) -> list[StructuredTool]:
        """Convierte todas las herramientas MCP en herramientas LangChain."""
        herramientas: list[StructuredTool] = []
        for herramienta in await self.listar_herramientas():
            nombre = str(getattr(herramienta, "name", "herramienta_mcp"))
            descripcion = str(getattr(herramienta, "description", "") or nombre)
            esquema = getattr(herramienta, "inputSchema", None)
            if esquema is None:
                esquema = getattr(herramienta, "input_schema", None)

            async def llamar(_nombre: str = nombre, **argumentos: Any) -> str:
                return await self.ejecutar(_nombre, argumentos)

            herramientas.append(
                StructuredTool.from_function(
                    coroutine=llamar,
                    name=nombre,
                    description=descripcion,
                    args_schema=esquema_pydantic(nombre, esquema),
                )
            )
        return herramientas

    @classmethod
    @asynccontextmanager
    async def conectar_stdio(
        cls,
        comando: str,
        argumentos: list[str] | None = None,
        entorno: dict[str, str] | None = None,
    ) -> AsyncIterator["ClienteMCP"]:
        """Conecta con un servidor MCP local mediante STDIO."""
        parametros = StdioServerParameters(
            command=comando,
            args=argumentos or [],
            env=entorno,
        )
        async with stdio_client(parametros) as (entrada, salida):
            async with ClientSession(entrada, salida) as sesion:
                cliente = cls(sesion)
                await cliente.inicializar()
                yield cliente

    @classmethod
    @asynccontextmanager
    async def conectar_http(
        cls,
        url: str | None = None,
        token: str | None = None,
    ) -> AsyncIterator["ClienteMCP"]:
        """Conecta con MCP Streamable HTTP usando un Bearer token.

        Si no se entregan argumentos, lee ``MCP_SERVER_METEOSOURCE`` y
        ``MCP_BEARER_TOKEN_ENV_VAR``. Esta última puede contener directamente
        el token o el nombre de otra variable que lo contiene. El token nunca
        se imprime ni se incluye en errores.
        """
        destino = (url or os.environ.get("MCP_SERVER_METEOSOURCE", "")).strip()
        if not destino:
            raise RuntimeError("Falta configurar MCP_SERVER_METEOSOURCE.")

        credencial = _resolver_token_bearer(token)

        encabezados = {"Authorization": f"Bearer {credencial}"}
        async with httpx2.AsyncClient(headers=encabezados) as cliente_http:
            async with streamable_http_client(destino, http_client=cliente_http) as (entrada, salida):
                async with ClientSession(entrada, salida) as sesion:
                    cliente = cls(sesion)
                    await cliente.inicializar()
                    yield cliente

    @classmethod
    @asynccontextmanager
    async def conectar_meteosource(cls) -> AsyncIterator["ClienteMCP"]:
        """Conecta al servidor Meteosource configurado en el entorno."""
        async with cls.conectar_http() as cliente:
            yield cliente
