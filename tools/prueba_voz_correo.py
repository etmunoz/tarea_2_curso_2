# --8<-- encabezado-grupo
# Archivo: tools/prueba_voz_correo.py
# Objetivo: Prueba E2E reproducible del canal web: acceso rechazado/permitido, consulta al supervisor y despacho por correo.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261123 1800
# Última modificación: 20261123 1800
# --8<-- fin-encabezado-grupo

"""Prueba E2E del recorrido "hablo con el chat → me responde → me llega el correo".

Ejerce el MISMO camino HTTP que usa el navegador (BFF web → gateway FastAPI → supervisor → agente A2A
→ SMTP). La parte de voz (STT/TTS) ocurre en el navegador y se evidencia con la grabación manual
descrita en evidencias/voz_correo/README.md; aquí la pregunta entra como el texto ya transcrito.

Uso (solo biblioteca estándar; la clave NUNCA va en argumentos ni en el repo):
    T2_CLAVE='***' python3 tools/prueba_voz_correo.py --usuario fabio \\
        --pregunta "¿Cómo está el clima hoy en Talca?" --para destinatario@ejemplo.cl --enviar

Sin --enviar no se manda correo (evita envíos accidentales). Deja un JSON en evidencias/voz_correo/.
"""
from __future__ import annotations

import argparse
import getpass
import http.cookiejar
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Santiago")
SALIDA = Path(__file__).resolve().parent.parent / "evidencias" / "voz_correo"


class _SinRedireccion(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def _pedir(opener, metodo, url, datos=None, form=False):
    """Devuelve (status, cuerpo_texto, location). No lanza en 4xx/5xx."""
    cuerpo, cab = None, {}
    if datos is not None:
        cuerpo = (urllib.parse.urlencode(datos) if form else json.dumps(datos)).encode()
        cab["Content-Type"] = "application/x-www-form-urlencoded" if form else "application/json"
    req = urllib.request.Request(url, data=cuerpo, method=metodo, headers=cab)
    try:
        with opener.open(req, timeout=180) as r:
            return r.status, r.read().decode(errors="replace"), r.headers.get("Location")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace"), e.headers.get("Location")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default=os.environ.get("T2_BASE", "https://tarea2curso2.etmk.cl"))
    ap.add_argument("--usuario", required=True)
    ap.add_argument("--pregunta", required=True, help="texto que dictaste por voz (transcripción)")
    ap.add_argument("--para", help="destinatario del correo (se registra en la allowlist si falta)")
    ap.add_argument("--enviar", action="store_true", help="enviar el correo de verdad")
    a = ap.parse_args()
    if a.enviar and not a.para:
        ap.error("--enviar requiere --para")
    clave = os.environ.get("T2_CLAVE") or getpass.getpass(f"Clave de {a.usuario}: ")
    base = a.base.rstrip("/")
    ahora = lambda: datetime.now(TZ).isoformat(timespec="seconds")  # noqa: E731
    pasos: list[dict] = []

    def paso(nombre, esperado, status, ok, **extra):
        pasos.append({"paso": nombre, "ts": ahora(), "esperado": esperado, "status": status, "ok": ok, **extra})
        print(f"[{'OK ' if ok else 'FALLA'}] {nombre}: HTTP {status}")

    anon = urllib.request.build_opener(_SinRedireccion)
    # 1) Acceso rechazado: API sin sesión y login con clave errónea.
    st, _, _ = _pedir(anon, "POST", f"{base}/api/consulta", {"pregunta": a.pregunta})
    paso("acceso_sin_sesion", "401 en /api/consulta", st, st == 401)
    st, _, _ = _pedir(anon, "POST", f"{base}/login", {"usuario": a.usuario, "clave": "clave-incorrecta"}, form=True)
    paso("login_clave_incorrecta", "401", st, st == 401)

    # 2) Acceso permitido.
    jar = http.cookiejar.CookieJar()
    web = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar), _SinRedireccion)
    st, _, loc = _pedir(web, "POST", f"{base}/login", {"usuario": a.usuario, "clave": clave}, form=True)
    paso("login_correcto", "302 → /", st, st == 302 and (loc or "").rstrip("/") in ("", base), location=loc)
    if st != 302:
        return _guardar(a, pasos, ahora())

    # 3) Consulta al supervisor (el mismo POST que hace el chat tras el dictado).
    t0 = time.monotonic()
    st, txt, _ = _pedir(web, "POST", f"{base}/api/consulta", {"pregunta": a.pregunta, "sesion": f"evid-{int(time.time())}"})
    seg = round(time.monotonic() - t0, 1)
    r = json.loads(txt) if st == 200 else {}
    ok = st == 200 and bool(r.get("respuesta")) and not r.get("error")
    paso("consulta", "200 con respuesta y agente elegido", st, ok, segundos=seg, pregunta=a.pregunta,
         elegido=r.get("elegido"), motivo=r.get("motivo"), ruta=r.get("ruta"), respuesta=r.get("respuesta"),
         error=r.get("error"))

    # 4) Correo con la respuesta (solo si se pidió y la consulta salió bien).
    if a.enviar and ok:
        _, txt, _ = _pedir(web, "GET", f"{base}/api/correo")
        if a.para.lower() not in [d.lower() for d in json.loads(txt).get("destinatarios", [])]:
            st, txt, _ = _pedir(web, "POST", f"{base}/api/registrar-correo", {"correo": a.para})
            paso("registrar_destinatario", "200 ok", st, st == 200 and json.loads(txt).get("ok"))
        asunto = f"Evidencia voz→chat→correo · {r.get('elegido') or 'sin agente'} · {datetime.now(TZ):%Y-%m-%d %H:%M}"
        st, txt, _ = _pedir(web, "POST", f"{base}/api/enviar", {
            "destinatario": a.para, "asunto": asunto, "mensaje": r["respuesta"], "pregunta": a.pregunta,
            "agente": r.get("elegido"), "ruta": r.get("ruta") or []})
        e = json.loads(txt) if txt.startswith("{") else {}
        paso("enviar_correo", "200 {ok:true}", st, st == 200 and e.get("ok") is True, asunto=asunto,
             destinatario=a.para, error=e.get("error"))
    _pedir(web, "GET", f"{base}/logout")
    return _guardar(a, pasos, ahora())


def _guardar(a, pasos, fin) -> int:
    SALIDA.mkdir(parents=True, exist_ok=True)
    rep = {"entorno": a.base, "usuario": a.usuario, "fin": fin, "todo_ok": all(p["ok"] for p in pasos), "pasos": pasos}
    f = SALIDA / f"resultado_{datetime.now(TZ):%Y%m%d_%H%M%S}.json"
    f.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"→ {f}  todo_ok={rep['todo_ok']}")
    return 0 if rep["todo_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
