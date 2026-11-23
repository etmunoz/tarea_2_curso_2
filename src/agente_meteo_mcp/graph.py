# --8<-- encabezado-grupo
# Archivo: src/agente_meteo_mcp/graph.py
# Objetivo: Grafo LangGraph del agente meteo_mcp con memoria y trazas.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261122 0000
# Última modificación: 20261122 0000
# --8<-- fin-encabezado-grupo

"""Agente meteorológico MCP ejecutable localmente y por A2A."""
from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime
from typing import Any, Literal
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import BaseModel

from src.agente_meteo_mcp.herramientas import HERRAMIENTAS
from src.agente_meteo_mcp.prompts import GUARDIA_DE_ENTRADA_PROMPT, SYSTEM_PROMPT

load_dotenv()

class Veredicto(BaseModel):
    """Clasificación estructurada de la guardia de entrada."""

    permitido: bool
    categoria: Literal[
        "pronostico_del_tiempo_hoy",
        "pronostico_del_tiempo_10_dias",
        "historial_climatico",
        "ok",
        "fuera_de_tema",
        "inyeccion",
        "datos_personales",
        "accion_no_soportada",
    ]
    motivo: str


class EstadoMeteo(MessagesState):
    """Estado del grafo con el veredicto de la guardia."""

    veredicto: dict[str, Any]


modelo = ChatGoogleGenerativeAI(
    model=os.environ.get("MODELO", "gemini-3.5-flash-lite"),
)
modelo_guardia = ChatGoogleGenerativeAI(
    model=os.environ.get("MODELO", "gemini-3.5-flash-lite"),
)
clasificador_guardia = modelo_guardia.with_structured_output(Veredicto)
fecha_actual_santiago = datetime.now(ZoneInfo("America/Santiago")).date().isoformat()
PROMPT_AGENTE = (
    f"{SYSTEM_PROMPT}\n\n"
    f"Fecha actual en America/Santiago: {fecha_actual_santiago}. "
    "Usa esta fecha para interpretar expresiones como hoy, mañana y hace N días. "
    "No uses una fecha distinta salvo que el usuario la indique explícitamente."
)

agente = create_agent(
    model=modelo,
    tools=HERRAMIENTAS,
    system_prompt=PROMPT_AGENTE,
    name="meteo_mcp",
)


async def guardia_de_entrada(estado: EstadoMeteo) -> dict[str, dict[str, Any]]:
    """Clasifica el mensaje antes de ejecutar el agente meteorológico."""
    mensajes = estado.get("messages") or []
    texto = _texto_mensaje(mensajes[-1]) if mensajes else ""
    try:
        veredicto = await clasificador_guardia.ainvoke(
            [
                {"role": "system", "content": GUARDIA_DE_ENTRADA_PROMPT},
                HumanMessage(content=texto),
            ]
        )
        if not isinstance(veredicto, Veredicto):
            veredicto = Veredicto.model_validate(veredicto)
    except Exception as error:  # noqa: BLE001
        veredicto = Veredicto(
            permitido=False,
            categoria="inyeccion",
            motivo=f"No fue posible validar el mensaje ({type(error).__name__}).",
        )
    return {"veredicto": veredicto.model_dump()}


def _ruta_guardia(estado: EstadoMeteo) -> Literal["agente", "respuesta_bloqueada"]:
    """Dirige el flujo según el veredicto estructurado."""
    return "agente" if estado.get("veredicto", {}).get("permitido") else "respuesta_bloqueada"


MENSAJES_BLOQUEO = {
    "fuera_de_tema": "No puedo ayudarte con ese tema. Sí puedo orientarte sobre el pronóstico y las condiciones del tiempo.",
    "inyeccion": "No puedo seguir esa solicitud. Sí puedo ayudarte con pronósticos meteorológicos claros y verificables.",
    "datos_personales": "No puedo guardar ni gestionar datos personales. Sí puedo ayudarte con el pronóstico del tiempo.",
    "accion_no_soportada": "No puedo reservar, comprar, enviar correos ni modificar datos. Sí puedo consultar el pronóstico del tiempo.",
}


def respuesta_bloqueada(estado: EstadoMeteo) -> dict[str, list[AIMessage]]:
    """Responde con un texto fijo sin llamar al modelo meteorológico ni a tools."""
    categoria = estado.get("veredicto", {}).get("categoria", "fuera_de_tema")
    mensaje = MENSAJES_BLOQUEO.get(
        categoria,
        "Solo puedo ayudarte con el pronóstico y las condiciones del tiempo.",
    )
    return {"messages": [AIMessage(content=mensaje)]}


flujo = StateGraph(EstadoMeteo)
flujo.add_node("guardia_de_entrada", guardia_de_entrada)
flujo.add_node("agente", agente)
flujo.add_node("respuesta_bloqueada", respuesta_bloqueada)
flujo.add_edge(START, "guardia_de_entrada")
flujo.add_conditional_edges(
    "guardia_de_entrada",
    _ruta_guardia,
    {
        "agente": "agente",
        "respuesta_bloqueada": "respuesta_bloqueada",
    },
)
flujo.add_edge("agente", END)
flujo.add_edge("respuesta_bloqueada", END)
# `graph` SIN checkpointer: es el que publica `langgraph dev` (A2A) y langgraph.json. La plataforma
# maneja la persistencia por hilo; un checkpointer propio hace que langgraph-api RECHACE el grafo y no
# levante el servidor. `_graph_mem` (con checkpointer) es solo para los helpers standalone del CLI/server.
graph = flujo.compile()
_graph_mem = flujo.compile(checkpointer=MemorySaver())


def _texto_mensaje(mensaje: Any) -> str:
    """Obtiene texto legible de un mensaje LangChain."""
    contenido = getattr(mensaje, "content", mensaje)
    if isinstance(contenido, str):
        return contenido
    return json.dumps(contenido, ensure_ascii=False, default=str)


def _limpiar_respuesta(texto: str) -> str:
    """Entrega una respuesta humana sin restos técnicos del MCP o JSON."""
    # Recorta desde el primer marcador técnico (extras/signature), tolerando comillas, espacios o comas
    # alrededor (p. ej. `"extras":`, `, extras :`) que el JSON del MCP puede dejar. Antes solo buscaba
    # `extras:`/`signature:` literales y el `"extras":` del JSON se colaba al final.
    tecnico = re.search(r'[\s",]*["\']?(?:extras|signature)["\']?\s*:', texto, re.IGNORECASE)
    if tecnico:
        texto = texto[: tecnico.start()]
    texto = re.sub(r"(?im)^\s*fuente\s*:?.*$", "", texto)
    texto = texto.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\t", " ")
    texto = re.sub(r"\*\*(.*?)\*\*", r"\1", texto)
    texto = re.sub(r"(?m)^\s*\*\s+", "- ", texto)
    texto = re.sub(r"(?i)\b(text|type)\b", "", texto)
    texto = texto.replace("{", "").replace("}", "")
    texto = texto.replace("[", "").replace("]", "")
    texto = texto.replace('"', "").replace("```", "")
    texto = re.sub(r"^\s*(?:[:;,]\s*)+", "", texto)
    texto = re.sub(r"(?m)^\s*[:;,]+\s*", "", texto)
    texto = re.sub(r"(?m)^\s*#{1,6}\s*", "", texto)
    dias = r"(?:lunes|martes|miércoles|miercoles|jueves|viernes|sábado|sabado|domingo)"
    texto = re.sub(
        rf"(?im)^\s*-\s*({dias}\b[^\n]*\b\d{{4}})\s*$",
        r"\n\nDÍA — \1\n",
        texto,
    )
    texto = re.sub(r"[ \t]{2,}", " ", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def _ultima_respuesta(estado: dict[str, Any]) -> str:
    """Devuelve el contenido del último mensaje del estado."""
    mensajes = estado.get("messages") or []
    respuesta = _texto_mensaje(mensajes[-1]) if mensajes else "No se recibió respuesta."
    return _limpiar_respuesta(respuesta)


def _configuracion(context_id: str) -> dict[str, dict[str, str]]:
    """Configura la memoria por conversación usando thread_id."""
    return {"configurable": {"thread_id": context_id}}


async def responder(texto: str, context_id: str) -> str:
    """Responde usando el grafo y conserva memoria por context_id."""
    estado = await _graph_mem.ainvoke(
        {"messages": [{"role": "user", "content": texto}]},
        config=_configuracion(context_id),
    )
    return _ultima_respuesta(estado)


async def saltos(texto: str) -> str:
    """Muestra nodos, tools y cantidad de saltos durante una ejecución."""
    context_id = f"meteo-mcp-saltos-{uuid.uuid4()}"
    cantidad = 0
    ultimo_mensaje: Any = None

    async for actualizacion in _graph_mem.astream(
        {"messages": [{"role": "user", "content": texto}]},
        config=_configuracion(context_id),
        stream_mode="updates",
    ):
        cantidad += 1
        for nodo, datos in actualizacion.items():
            print(f"[salto {cantidad}] nodo: {nodo}")
            if nodo == "guardia_de_entrada" and isinstance(datos, dict):
                veredicto = datos.get("veredicto", {})
                estado = "permitido" if veredicto.get("permitido") else "no permitido"
                print(f"  veredicto: {estado}")
                print(f"  categoría: {veredicto.get('categoria', 'desconocida')}")
            mensajes = datos.get("messages", []) if isinstance(datos, dict) else []
            for mensaje in mensajes:
                ultimo_mensaje = mensaje
                for llamada in getattr(mensaje, "tool_calls", []) or []:
                    print(f"  herramienta: {llamada.get('name', 'desconocida')}")

    print(f"Total de saltos: {cantidad}")
    if ultimo_mensaje is None:
        return "No se recibió respuesta."
    return _limpiar_respuesta(_texto_mensaje(ultimo_mensaje))


def diagrama() -> None:
    """Imprime Mermaid con la guardia, el agente y cada tool MCP como nodo."""
    nodos_tools = []
    enlaces_tools = []
    for herramienta in HERRAMIENTAS:
        nombre = herramienta.name
        identificador = re.sub(r"[^a-zA-Z0-9_]", "_", nombre)
        nodos_tools.append(f'    {identificador}["{nombre}<br/>MCP Meteosource"]')
        enlaces_tools.append(f"    agente --> {identificador}")
        enlaces_tools.append(f"    {identificador} --> agente")

    mermaid = [
        "flowchart TD",
        '    inicio(["mensaje"]) --> guardia["guardia_de_entrada<br/>Veredicto"]',
        '    guardia -->|permitido| agente["agente<br/>meteo_mcp"]',
        '    guardia -->|no permitido| bloqueada["respuesta_bloqueada"]',
        '    bloqueada --> fin(["fin"])',
        '    agente --> fin',
        "    subgraph MCP[Herramientas MCP de Meteosource]",
        *nodos_tools,
        "    end",
        *enlaces_tools,
        "    classDef control fill:#e8f0fe,stroke:#4a6fa5",
        "    classDef herramienta fill:#e8f5e9,stroke:#4c956c",
        "    class guardia,bloqueada control",
        "    class search_places,get_forecast,get_weather_history herramienta",
    ]
    print("\n".join(mermaid))
