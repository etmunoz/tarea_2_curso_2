# --8<-- encabezado-grupo
# Archivo: src/agente_meteo_mcp/server.py
# Objetivo: Servidor HTTP local y ficha del agente meteo_mcp.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261122 0000
# Última modificación: 20261122 0000
# --8<-- fin-encabezado-grupo

"""Publica una ficha HTTP mínima para el agente meteo_mcp."""
from __future__ import annotations

import os
from collections.abc import Awaitable, Callable
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from src.agente_meteo_mcp.graph import _limpiar_respuesta, responder

load_dotenv()


def crear_tarjeta(
    nombre: str,
    descripcion: str,
    skills: list[dict[str, Any]],
    url: str,
) -> dict[str, Any]:
    """Construye la ficha pública del agente."""
    return {
        "name": nombre,
        "description": descripcion,
        "url": url,
        "skills": skills,
    }


class Solicitud(BaseModel):
    """Entrada de consulta para el endpoint local."""

    texto: str = Field(min_length=1)
    context_id: str = "terminal"


def crear_app(
    tarjeta: dict[str, Any],
    responder_fn: Callable[[str, str], Awaitable[str]],
) -> FastAPI:
    """Construye la aplicación HTTP del agente y su endpoint de ficha."""
    app = FastAPI(title=tarjeta["name"], description=tarjeta["description"])

    @app.get("/.well-known/agent-card.json")
    async def ficha() -> dict[str, Any]:
        return tarjeta

    @app.post("/consulta", response_class=PlainTextResponse)
    async def consulta(solicitud: Solicitud) -> PlainTextResponse:
        respuesta = await responder_fn(solicitud.texto, solicitud.context_id)
        # La frontera HTTP vuelve a limpiar para evitar que ningún metadato
        # técnico llegue al cliente, aunque el proceso haya usado otro flujo.
        return PlainTextResponse(_limpiar_respuesta(respuesta))

    return app


URL_METEO_MCP = os.environ.get("URL_METEO_MCP", "http://127.0.0.1:8005")
tarjeta = crear_tarjeta(
    nombre="meteo_mcp",
    descripcion=(
        "Conozco el pronóstico meteorológico consultando las herramientas de Meteosource "
        "para ciudades y localidades. No respondo temas ajenos a la meteorología ni invento "
        "datos cuando el servidor no los entrega."
    ),
    skills=[
        {
            "name": "search_places",
            "description": "Busca localidades y sus place_id.",
            "example": "¿Cuál es el place_id de Berlín?",
        },
        {
            "name": "get_forecast",
            "description": "Obtiene el pronóstico meteorológico de localidades encontradas.",
            "example": "¿Qué tiempo habrá mañana en Santiago?",
        },
        {
            "name": "get_weather_history",
            "description": "Consulta el tiempo histórico de localidades y fechas encontradas.",
            "example": "¿Qué temperatura hubo en Santiago la semana pasada?",
        },
    ],
    url=URL_METEO_MCP,
)

app = crear_app(tarjeta, responder)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8005)
