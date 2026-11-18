# --8<-- encabezado-grupo
# Archivo: src/agente_machinelearning/graph.py
# Objetivo: Agente de Ezequiel (IA Engineer & Data Scientist) · expuesto por A2A NATIVO.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261110 1603
# Última modificación: 20261111 2049
# --8<-- fin-encabezado-grupo

"""Agente de Ezequiel (IA Engineer & Data Scientist) · expuesto por A2A NATIVO.

Mismo molde que el agente de viajes: no hay código de servidor aquí. `langgraph dev`
lee `langgraph.json`, levanta este grafo y publica automáticamente:
  · la Agent Card  →  GET  /.well-known/agent-card.json?assistant_id=agente_machinelearning
  · el endpoint    →  POST /a2a/agente_machinelearning   (message/send, message/stream, …)

El estado del grafo trae la clave `messages` (requisito de A2A nativo); el `contextId`
de A2A se convierte en `thread_id`, así la memoria por conversación viene gratis.
"""
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from src.agente_machinelearning.herramientas import HERRAMIENTAS
from src.agente_machinelearning.prompts import SYSTEM_EZEQUIEL

load_dotenv()

from src.config import bootstrap  # noqa: F401,E402  (ajustes web -> entorno; .env gana)
modelo = ChatGoogleGenerativeAI(model=os.environ.get("MODELO", "gemini-3.5-flash-lite"))

# Agente ReAct (LangChain 1.x): el modelo decide qué herramienta llamar, la llama,
# lee el resultado y responde. Su estado tiene `messages`: lo único que A2A necesita.
graph = create_agent(
    model=modelo,
    tools=HERRAMIENTAS,
    system_prompt=SYSTEM_EZEQUIEL,
    name="agente_machinelearning",
)
