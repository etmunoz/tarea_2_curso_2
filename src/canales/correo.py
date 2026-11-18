# --8<-- encabezado-grupo
# Archivo: src/canales/correo.py
# Objetivo: Despacho por correo (HTML + texto): respuesta formateada, ruta de agentes y gráfico del grafo.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1552
# Última modificación: 20261117 1552
# --8<-- fin-encabezado-grupo

"""Despacho por correo desde el buzón dedicado (SMTP submission 587 + STARTTLS).

Solo envía a destinatarios de la allowlist (src/memoria). El correo lleva, al pie: (1) la RUTA que
hicieron los agentes y (2) el gráfico del grafo del coordinador (PNG embebido por CID; si no se pudo
renderizar, el Mermaid como texto). Nunca auto-envío: el disparo lo hace el usuario.
"""
from __future__ import annotations

import html as _html
import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from email.utils import make_msgid
from zoneinfo import ZoneInfo

from src.canales import grafo_imagen
from src.memoria import bd as memoria

SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
MAIL_FROM = os.environ.get("MAIL_FROM", SMTP_USER or "tarea2curso2@etmk.cl")
_TZ = ZoneInfo("America/Santiago")


def _ruta_txt(ruta: list[str] | None) -> str:
    return " → ".join(ruta) if ruta else "—"


def componer(pregunta: str, respuesta: str, ruta, agente, cid_grafo=None) -> tuple[str, str]:
    """Objetivo: construir (html, texto_plano) del correo. Salida: tupla (html, texto)."""
    ahora = datetime.now(_TZ).strftime("%Y-%m-%d %H:%M (America/Santiago)")
    ruta_s = _ruta_txt(ruta)
    ag = agente or "—"
    q = _html.escape(pregunta or "")
    r = _html.escape(respuesta or "").replace("\n", "<br>")
    if cid_grafo:
        grafo_html = f'<img src="cid:{cid_grafo}" alt="Grafo del coordinador" style="max-width:100%;border:1px solid #ddd;border-radius:6px">'
    else:
        grafo_html = f'<pre style="background:#f4f4f4;padding:10px;border-radius:6px;overflow:auto">{_html.escape(grafo_imagen.mermaid_coordinador())}</pre>'
    html = f"""<!doctype html><html><body style="font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#222;max-width:680px;margin:auto">
  <div style="background:#0b5; color:#fff; padding:14px 18px; border-radius:8px 8px 0 0">
    <h2 style="margin:0">Respuesta del sistema de agentes</h2>
    <div style="opacity:.9;font-size:13px">{ahora}</div>
  </div>
  <div style="border:1px solid #e3e3e3;border-top:0;padding:18px;border-radius:0 0 8px 8px">
    <p style="margin:.2em 0;color:#666;font-size:13px"><b>Tu consulta</b></p>
    <blockquote style="margin:.3em 0 1em;border-left:3px solid #ccc;padding-left:10px;color:#444">{q}</blockquote>
    <p style="margin:.2em 0;color:#666;font-size:13px"><b>Respuesta</b></p>
    <div style="line-height:1.5">{r}</div>
    <hr style="border:0;border-top:1px solid #eee;margin:18px 0">
    <p style="margin:.2em 0;color:#666;font-size:13px"><b>Trazabilidad</b></p>
    <p style="margin:.2em 0"><b>Ruta de los agentes:</b> <code>{_html.escape(ruta_s)}</code></p>
    <p style="margin:.2em 0"><b>Agente que respondió:</b> <code>{_html.escape(ag)}</code></p>
    <p style="margin:1em 0 .3em;color:#666;font-size:13px"><b>Grafo del coordinador (LangGraph)</b></p>
    {grafo_html}
  </div>
</body></html>"""
    texto = (f"Respuesta del sistema de agentes — {ahora}\n\n"
             f"Tu consulta:\n{pregunta}\n\nRespuesta:\n{respuesta}\n\n"
             f"Trazabilidad:\n- Ruta de los agentes: {ruta_s}\n- Agente que respondió: {ag}\n\n"
             f"Grafo del coordinador (Mermaid):\n{grafo_imagen.mermaid_coordinador()}\n")
    return html, texto


def enviar(destinatario: str, asunto: str, pregunta: str, respuesta: str, ruta=None, agente=None) -> dict:
    """Objetivo: enviar el correo SOLO si el destinatario está en la allowlist. Registra el despacho.

    Nunca auto-envío (lo dispara el usuario). Sin credenciales SMTP queda deshabilitado (compone igual).
    """
    if not memoria.es_destinatario_permitido(destinatario):
        memoria.registrar_despacho(destinatario, asunto, "rechazado_allowlist")
        return {"ok": False, "error": "destinatario no está en la allowlist (debe registrarse primero)"}

    png = grafo_imagen.png_coordinador()
    msg = EmailMessage()
    msg["From"] = MAIL_FROM
    msg["To"] = destinatario
    msg["Subject"] = asunto
    cid = None
    if png:
        cid = make_msgid(domain="etmk.cl")[1:-1]
    html, texto = componer(pregunta, respuesta, ruta, agente, cid_grafo=cid)
    msg.set_content(texto)
    msg.add_alternative(html, subtype="html")
    if png and cid:
        with open(png, "rb") as f:
            msg.get_payload()[1].add_related(f.read(), maintype="image", subtype="png", cid=f"<{cid}>")

    if not (SMTP_USER and SMTP_PASS):
        memoria.registrar_despacho(destinatario, asunto, "no_configurado")
        return {"ok": False, "error": "correo no configurado (faltan credenciales SMTP en el servicio)"}
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
        memoria.registrar_despacho(destinatario, asunto, "enviado")
        return {"ok": True}
    except Exception as exc:  # noqa: BLE001
        memoria.registrar_despacho(destinatario, asunto, "fallo")
        return {"ok": False, "error": f"fallo SMTP: {exc}"}
