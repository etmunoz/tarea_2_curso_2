# --8<-- encabezado-grupo
# Archivo: src/agente_cocinachilena/graph.py
# Objetivo: Agente de cocina chilena · expuesto por A2A NATIVO (molde de viajes/Ezequiel).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261110 2013
# Última modificación: 20261111 2049
# --8<-- fin-encabezado-grupo

"""Agente de cocina chilena · expuesto por A2A NATIVO (molde de viajes/Ezequiel)."""
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from src.agente_cocinachilena.herramientas import HERRAMIENTAS
from src.agente_cocinachilena.prompts import SYSTEM_COCINA

load_dotenv()

from src.config import bootstrap  # noqa: F401,E402  (ajustes web -> entorno; .env gana)
modelo = ChatGoogleGenerativeAI(model=os.environ.get("MODELO", "gemini-3.5-flash-lite"))

graph = create_agent(
    model=modelo,
    tools=HERRAMIENTAS,
    system_prompt=SYSTEM_COCINA,
    name="agente_cocinachilena",
)
