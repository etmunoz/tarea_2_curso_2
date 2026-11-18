# --8<-- encabezado-grupo
# Archivo: src/canales/monitor.py
# Objetivo: Monitor/backoffice: accesos, despachos, destinatarios, historial, estado Gemini y config web de secretos.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1629
# Última modificación: 20261117 1852
# --8<-- fin-encabezado-grupo

"""Monitor/backoffice de operación (stdlib http.server, login Basic Auth).

Vistas: `/` (panel: estado de la clave Gemini, accesos 200/401, despachos, allowlist, historial) y
`/config` (ingreso ALTERNATIVO de secretos por web: GOOGLE_API_KEY, API_KEY, SMTP_PASS; el .env tiene
prioridad). Cambiar la GOOGLE_API_KEY requiere reiniciar t2c2-langgraph y t2c2-api para aplicar.
"""
from __future__ import annotations

import base64
import html as _html
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.config import ajustes, estado
from src.memoria import bd as memoria

HOST = os.environ.get("MONITOR_HOST", "127.0.0.1")
PORT = int(os.environ.get("MONITOR_PORT", "8798"))
USER = os.environ.get("MONITOR_USER", "")
PASS = os.environ.get("MONITOR_PASS", "")

_ESTILO = """<style>
 body{font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;max-width:960px;margin:0 auto;padding:16px;color:#222;background:#fafafa}
 h1{font-size:20px} h2{font-size:16px;margin-top:26px} a{color:#0a7}
 .cards{display:flex;gap:12px;flex-wrap:wrap} .card{background:#fff;border:1px solid #e3e3e3;border-radius:10px;padding:12px 16px;min-width:120px}
 .card b{font-size:24px;display:block} .ok{color:#0a6} .no{color:#c0392b}
 table{border-collapse:collapse;width:100%;background:#fff;margin-top:8px;font-size:13px}
 th,td{border:1px solid #e3e3e3;padding:6px 8px;text-align:left} th{background:#f3f3f3}
 .vacio{color:#999;text-align:center} .foot{color:#999;font-size:12px;margin-top:24px}
 form.cfg{background:#fff;border:1px solid #e3e3e3;border-radius:10px;padding:16px;max-width:520px}
 form.cfg label{display:block;margin:12px 0 4px} form.cfg input{width:100%;box-sizing:border-box;padding:9px;border:1px solid #ccc;border-radius:8px}
 form.cfg button{margin-top:14px;padding:10px 16px;border:0;border-radius:8px;background:#0b5;color:#fff;cursor:pointer}
 .aviso{background:#dff3e6;color:#0a6;padding:10px 12px;border-radius:8px;margin:10px 0}
 .nota{background:#fff8e1;color:#8a6d00;padding:10px 12px;border-radius:8px;margin:10px 0;font-size:13px}
</style>"""


def _banner_gemini() -> str:
    g = estado.gemini()
    ts = g.get("ts") or ""
    if g["ok"] is True:
        return f'<div class="aviso">Clave Gemini: OK <span style="color:#888">({ts})</span></div>'
    if g["ok"] is False:
        det = _html.escape(g.get("detalle") or "error")
        return f'<div class="nota" style="background:#fdecea;color:#c0392b">&#9888; Clave Gemini: {det} desde {ts}. Renueva o cambia la clave en Configuracion.</div>'
    return '<div class="nota">Clave Gemini: sin uso aun.</div>'


def _tabla(cols, filas, claves) -> str:
    th = "".join(f"<th>{_html.escape(c)}</th>" for c in cols)
    if not filas:
        return f"<table><tr>{th}</tr><tr><td colspan={len(cols)} class=vacio>&mdash; sin registros &mdash;</td></tr></table>"
    trs = ""
    for f in filas:
        trs += "<tr>" + "".join(f"<td>{_html.escape(str(f.get(k, '')))}</td>" for k in claves) + "</tr>"
    return f"<table><tr>{th}</tr>{trs}</table>"


def _pagina_panel() -> bytes:
    r = memoria.resumen_accesos()
    dest = memoria.listar_destinatarios(solo_activos=False)
    html = f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Monitor &middot; Tarea 2</title>{_ESTILO}</head><body>
<h1>Monitor de operacion &mdash; Tarea 2</h1>
<p><a href="config">&#9881; Configuracion (claves por web)</a></p>
{_banner_gemini()}
<div class=cards>
  <div class=card>Accesos<b>{r['total']}</b></div>
  <div class=card>Permitidos<b class=ok>{r['permitido']}</b></div>
  <div class=card>Rechazados (401)<b class=no>{r['rechazado']}</b></div>
  <div class=card>Destinatarios<b>{len(dest)}</b></div>
</div>
<h2>Accesos al gateway (recientes)</h2>
{_tabla(['Fecha','Metodo','Ruta','Status','API_KEY'], memoria.accesos(40), ['ts','metodo','ruta','status','con_api_key'])}
<h2>Despachos de correo</h2>
{_tabla(['Fecha','Destinatario','Asunto','Estado'], memoria.despachos(40), ['ts','destinatario','asunto','estado'])}
<h2>Destinatarios (allowlist)</h2>
{_tabla(['Correo','Nombre','Activo','Alta'], dest, ['correo','nombre','activo','alta_ts'])}
<h2>Eventos de usuario (sesiones)</h2>
{_tabla(['Fecha','Usuario','Evento'], memoria.eventos(40), ['ts','usuario','evento'])}
<h2>Historial de conversacion (reciente)</h2>
{_tabla(['Fecha','Sesion','Rol','Agente','Contenido'], memoria.historial_reciente(30), ['ts','sesion','rol','agente','contenido'])}
<p class=foot>fail2ban se gestiona a nivel de servidor (requiere administrador). Horas en America/Santiago.</p>
</body></html>"""
    return html.encode()


def _pagina_config(guardado: bool = False) -> bytes:
    est = ajustes.estados()

    def badge(k):
        if os.environ.get(k):
            return '<span class=ok>definida en .env (prioritaria)</span>'
        return '<span class=ok>definida por web</span>' if est.get(k) else '<span class=no>no definida</span>'

    aviso = '<div class=aviso>Ajustes guardados. Reinicia <code>t2c2-langgraph</code> y <code>t2c2-api</code> para aplicar.</div>' if guardado else ''
    html = f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Configuracion &middot; Tarea 2</title>{_ESTILO}</head><body>
<h1>Configuracion &mdash; claves por web</h1>
<p><a href=".">&larr; Volver al panel</a></p>
{_banner_gemini()}
{aviso}
<p class=nota>Ingreso <b>alternativo</b> de secretos. Si una clave ya esta en el <code>.env</code> del servicio, esa <b>tiene prioridad</b>. Deja un campo vacio para no cambiarlo.</p>
<form class=cfg method=post action=config>
  <label>GOOGLE_API_KEY &mdash; estado: {badge('GOOGLE_API_KEY')}</label>
  <input type=password name=google_api_key autocomplete=off placeholder="pegar clave de Gemini">
  <label>API_KEY (gateway) &mdash; estado: {badge('API_KEY')}</label>
  <input type=password name=api_key autocomplete=off placeholder="(opcional)">
  <label>SMTP_PASS (buzon) &mdash; estado: {badge('SMTP_PASS')}</label>
  <input type=password name=smtp_pass autocomplete=off placeholder="(opcional)">
  <button type=submit>Guardar</button>
</form>
</body></html>"""
    return html.encode()


class Handler(BaseHTTPRequestHandler):
    def _auth_ok(self) -> bool:
        if not PASS:
            return False
        cab = self.headers.get("Authorization", "")
        if not cab.startswith("Basic "):
            return False
        try:
            u, p = base64.b64decode(cab[6:]).decode().split(":", 1)
        except Exception:  # noqa: BLE001
            return False
        return u == USER and p == PASS

    def _login(self):
        self.send_response(401); self.send_header("WWW-Authenticate", 'Basic realm="Monitor Tarea 2"'); self.end_headers()

    def _html(self, code, body):
        self.send_response(code); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        if not self._auth_ok():
            return self._login()
        if self.path in ("/config", "/config/"):
            return self._html(200, _pagina_config())
        return self._html(200, _pagina_panel())

    def do_POST(self):  # noqa: N802
        if not self._auth_ok():
            return self._login()
        if self.path in ("/config", "/config/"):
            n = int(self.headers.get("Content-Length", "0"))
            datos = urllib.parse.parse_qs(self.rfile.read(n).decode()) if n else {}
            for campo, clave in {"google_api_key": "GOOGLE_API_KEY", "api_key": "API_KEY", "smtp_pass": "SMTP_PASS"}.items():
                val = (datos.get(campo, [""])[0] or "").strip()
                if val:
                    ajustes.set(clave, val)
            return self._html(200, _pagina_config(guardado=True))
        return self._html(404, b"<p>no encontrado</p>")

    def log_message(self, *a):
        return


def main() -> None:
    print(f"Monitor en http://{HOST}:{PORT} (login Basic Auth; / panel y /config)")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
