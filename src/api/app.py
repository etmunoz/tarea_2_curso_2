# --8<-- encabezado-grupo
# Archivo: src/api/app.py
# Objetivo: Gateway FastAPI: unico punto de entrada a los agentes (API_KEY); ruta por turno, correo y aviso de cuota.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1544
# Última modificación: 20261117 1941
# --8<-- fin-encabezado-grupo

"""Gateway FastAPI (requisito duro §2): todo pasa por aquí; los agentes nunca se llaman directo.

Endpoints: GET /salud, GET /estado (clave Gemini), GET /agentes (protegido), POST /consulta
(ruteo+respuesta; protegido; devuelve SOLO la ruta del turno actual), GET /destinatarios y GET /correo
(allowlist/estado; protegidos), POST /enviar (despacho de correo; protegido). Import DIFERIDO del
coordinador (requiere GOOGLE_API_KEY).
"""
from __future__ import annotations

from src.config import bootstrap  # noqa: F401  (ajustes web -> entorno; .env gana)

import os
import uuid

from fastapi import Depends, FastAPI, Header
from pydantic import BaseModel

from src.api.seguridad import verificar_api_key
from src.config import estado
from src.fichas import FICHAS

app = FastAPI(title="Gateway Tarea 2 · Curso 2", version="0.2.0")


@app.middleware("http")
async def _log_acceso(request, call_next):
    """Registra cada llamada al gateway (sin guardar la clave) en la memoria."""
    resp = await call_next(request)
    try:
        from src.memoria import bd as memoria  # noqa: PLC0415
        memoria.registrar_acceso(request.url.path, request.method, resp.status_code,
                                 bool(request.headers.get("X-API-Key")))
    except Exception:  # noqa: BLE001
        pass
    return resp


_graph = None


def _coordinador():
    """Grafo del coordinador (import diferido; requiere GOOGLE_API_KEY)."""
    global _graph  # noqa: PLW0603
    if _graph is None:
        from src.coordinador.graph import graph  # noqa: PLC0415
        _graph = graph
    return _graph


class Consulta(BaseModel):
    pregunta: str
    sesion: str | None = None


class Correo(BaseModel):
    destinatario: str
    asunto: str
    mensaje: str
    pregunta: str | None = None
    agente: str | None = None
    ruta: list | None = None


@app.get("/salud")
def salud() -> dict:
    return {"estado": "ok"}


@app.get("/estado")
def estado_clave() -> dict:
    return {"gemini": estado.gemini()}


@app.get("/agentes", dependencies=[Depends(verificar_api_key)])
def agentes() -> dict:
    return {"agentes": [{"agente": g, "nombre": f["name"], "descripcion": f["description"]}
                        for g, f in FICHAS.items()]}


@app.get("/destinatarios", dependencies=[Depends(verificar_api_key)])
def destinatarios() -> dict:
    from src.memoria import bd as memoria  # noqa: PLC0415
    return {"destinatarios": [d["correo"] for d in memoria.listar_destinatarios(True)]}


@app.get("/correo", dependencies=[Depends(verificar_api_key)])
def correo_estado() -> dict:
    from src.memoria import bd as memoria  # noqa: PLC0415
    return {"configurado": bool(os.environ.get("SMTP_USER") and os.environ.get("SMTP_PASS")),
            "destinatarios": [d["correo"] for d in memoria.listar_destinatarios(True)]}


@app.post("/enviar", dependencies=[Depends(verificar_api_key)])
def enviar(c: Correo) -> dict:
    from src.canales import correo as cmod  # noqa: PLC0415
    return cmod.enviar(c.destinatario, c.asunto, c.pregunta or "", c.mensaje, c.ruta or [], c.agente)


class RegistroCorreo(BaseModel):
    correo: str


@app.get("/mi-correo", dependencies=[Depends(verificar_api_key)])
def mi_correo(x_usuario: str | None = Header(default=None, alias="X-Usuario")) -> dict:
    from src.memoria import bd as memoria  # noqa: PLC0415
    return {"usuario": x_usuario, "correo": memoria.correo_de_usuario(x_usuario or "")}


@app.post("/registrar-correo", dependencies=[Depends(verificar_api_key)])
def registrar_correo(c: RegistroCorreo, x_usuario: str | None = Header(default=None, alias="X-Usuario")) -> dict:
    from src.memoria import bd as memoria  # noqa: PLC0415
    correo = (c.correo or "").strip()
    if "@" not in correo or "." not in correo:
        return {"ok": False, "error": "correo inválido"}
    memoria.registrar_destinatario(correo, nombre=(x_usuario or ""))
    return {"ok": True, "correo": correo.lower()}


@app.post("/consulta", dependencies=[Depends(verificar_api_key)])
def consulta(c: Consulta, x_usuario: str | None = Header(default=None, alias="X-Usuario")) -> dict:
    from langchain_core.messages import HumanMessage  # noqa: PLC0415

    from src.memoria import bd as memoria  # noqa: PLC0415

    sesion = c.sesion or uuid.uuid4().hex
    hilo = f"{(x_usuario or 'anon')}:{sesion}"
    cfg = {"configurable": {"thread_id": hilo}}
    try:
        memoria.guardar_mensaje(hilo, "usuario", c.pregunta)
    except Exception:  # noqa: BLE001
        pass
    # ruta acumulada previa: para devolver SOLO los pasos de este turno
    try:
        st = _coordinador().get_state(cfg)
        prev = len((getattr(st, "values", {}) or {}).get("ruta", []))
    except Exception:  # noqa: BLE001
        prev = 0
    try:
        res = _coordinador().invoke({"messages": [HumanMessage(content=c.pregunta)]}, cfg)
    except Exception as e:  # noqa: BLE001
        if estado.es_cuota(str(e)):
            estado.set_gemini(False, "cuota/tokens agotados")
            return {"sesion": sesion, "error": "gemini_cuota", "elegido": None, "motivo": None,
                    "origen": "error", "ruta": [],
                    "respuesta": "⚠️ La clave de Gemini se quedó sin tokens o cuota. El administrador debe "
                                 "renovarla o cambiarla en la configuración del monitor (/config)."}
        return {"sesion": sesion, "error": "interno", "elegido": None, "motivo": None, "origen": "error",
                "ruta": [], "respuesta": "Ocurrió un error procesando la consulta. Intenta nuevamente."}
    estado.set_gemini(True, "ok")
    respuesta = res.get("respuesta") or ""
    ruta = (res.get("ruta") or [])[prev:]
    try:
        memoria.guardar_mensaje(hilo, "asistente", respuesta, agente=res.get("elegido"))
    except Exception:  # noqa: BLE001
        pass
    return {"sesion": sesion, "respuesta": respuesta, "elegido": res.get("elegido"),
            "motivo": res.get("motivo"), "origen": res.get("origen"), "ruta": ruta}
