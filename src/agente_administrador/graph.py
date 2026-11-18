# --8<-- encabezado-grupo
# Archivo: src/agente_administrador/graph.py
# Objetivo: Agente administrador (recepción/orientación del sistema), A2A nativo de langgraph dev.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1508
# Última modificación: 20261117 1508
# --8<-- fin-encabezado-grupo

"""Agente administrador · se expone por A2A de forma NATIVA con el servidor de LangGraph.

`langgraph dev` lee langgraph.json, levanta este grafo y publica su Agent Card y su endpoint
/a2a/agente_administrador. Requisito: el estado debe tener la clave `messages` (la trae create_agent).
"""
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from src.agente_administrador.herramientas import HERRAMIENTAS
from src.agente_administrador.prompts import SYSTEM_ADMINISTRADOR

load_dotenv()

from src.config import bootstrap  # noqa: F401,E402  (ajustes web -> entorno; .env gana)
modelo = ChatGoogleGenerativeAI(model=os.environ.get("MODELO", "gemini-3.5-flash-lite"))

graph = create_agent(
    model=modelo,
    tools=HERRAMIENTAS,
    system_prompt=SYSTEM_ADMINISTRADOR,
    name="agente_administrador",
)
