# --8<-- encabezado-grupo
# Archivo: src/canales/web.py
# Objetivo: Frontend web (BFF): chat de texto y chat por VOZ (Etapa A); añade la API_KEY server-side.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261117 1552
# Última modificación: 20261117 1608
# --8<-- fin-encabezado-grupo

"""Frontend web como BFF (Backend for Frontend), con la biblioteca estándar.

El navegador habla SOLO con este servidor (login Basic Auth propio); este reenvía a FastAPI agregando el
header X-API-Key desde el entorno del servicio. Así la API_KEY nunca llega al browser. Dos vistas:
`/` (chat de texto) y `/voz` (chat por voz, Etapa A: STT+TTS del navegador con Web Speech API).
Variables: WEB_HOST/WEB_PORT, API_BASE (FastAPI), API_KEY, WEB_USER/WEB_PASS (login; sin PASS no entra
nadie).
"""
from __future__ import annotations

import base64
import hmac
import html
import json
import os
import secrets
import sys as _sys
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

_sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.config import usuarios  # noqa: E402
from src.memoria import bd as memoria  # noqa: E402

HOST = os.environ.get("WEB_HOST", "127.0.0.1")
PORT = int(os.environ.get("WEB_PORT", "8797"))
API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8796").rstrip("/")
API_KEY = os.environ.get("API_KEY", "")
WEB_USER = os.environ.get("WEB_USER", "")
WEB_PASS = os.environ.get("WEB_PASS", "")


def _parse_usuarios(raw: str) -> dict:
    """Objetivo: parsear WEB_USERS='u1:p1,u2:p2,...' a dict usuario->clave (logins separados)."""
    d = {}
    for par in raw.split(","):
        par = par.strip()
        if ":" in par:
            u, pw = par.split(":", 1)
            if u.strip():
                d[u.strip()] = pw
    return d


WEB_USERS = _parse_usuarios(os.environ.get("WEB_USERS", ""))
if WEB_USER and WEB_PASS:
    WEB_USERS.setdefault(WEB_USER, WEB_PASS)  # compat: admin de un solo usuario

PAGINA = r"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Tarea 2 · Agentes</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
:root{--bg:#0b0d13;--panel:rgba(22,25,34,.72);--panel-brd:rgba(255,255,255,.08);--soft:rgba(255,255,255,.05);--soft2:rgba(255,255,255,.08);--aur:.55;--txt:#e8eaf0;--mut:#9aa3b6;--acc1:#7c5cff;--acc2:#22d3ee;--ok:#34d399;--warn:#fbbf24;--bad:#f87171;}
:root[data-theme="light"]{--bg:#eef1f8;--panel:rgba(255,255,255,.80);--panel-brd:rgba(12,18,40,.10);--soft:rgba(12,18,40,.045);--soft2:rgba(12,18,40,.07);--aur:.30;--txt:#1a2033;--mut:#5c6578;--acc1:#6d4bff;--acc2:#0ea5c4;}
*{box-sizing:border-box}html,body{height:100%;margin:0}
body{font-family:Inter,system-ui,sans-serif;color:var(--txt);background:var(--bg);overflow:hidden}
.aurora{position:fixed;inset:-20% -10%;z-index:0;filter:blur(90px);opacity:var(--aur);pointer-events:none}
.aurora i{position:absolute;border-radius:50%;animation:float 18s ease-in-out infinite}
.aurora i:nth-child(1){width:46vw;height:46vw;left:-6vw;top:-10vw;background:radial-gradient(circle,#7c5cff,transparent 60%)}
.aurora i:nth-child(2){width:40vw;height:40vw;right:-6vw;top:6vw;background:radial-gradient(circle,#22d3ee,transparent 60%);animation-delay:-6s}
.aurora i:nth-child(3){width:38vw;height:38vw;left:30vw;bottom:-14vw;background:radial-gradient(circle,#f472b6,transparent 60%);animation-delay:-11s}
@keyframes float{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(2vw,-3vw) scale(1.08)}}
.app{position:relative;z-index:1;height:100%;display:flex;flex-direction:column;padding:16px;gap:14px}
header{display:flex;align-items:center;gap:14px}
.logo{width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,var(--acc1),var(--acc2));display:grid;place-items:center;font-size:20px;box-shadow:0 8px 24px rgba(124,92,255,.4)}
h1{font-size:19px;margin:0;font-weight:700;letter-spacing:.2px}
header .sub{color:var(--mut);font-size:12.5px;margin-top:2px}
.chips{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap;max-width:58%}
.chip{display:flex;align-items:center;gap:7px;padding:6px 11px;border-radius:999px;background:var(--panel);border:1px solid var(--panel-brd);font-size:12.5px;backdrop-filter:blur(8px)}
.chip .dot{width:8px;height:8px;border-radius:50%;background:var(--ok);box-shadow:0 0 8px var(--ok)}
.tbtn{width:38px;height:38px;border-radius:11px;border:1px solid var(--panel-brd);background:var(--panel);color:var(--txt);font-size:17px;cursor:pointer;backdrop-filter:blur(8px);flex:none;display:grid;place-items:center;text-decoration:none}
.tbtn:hover{border-color:var(--acc1)}
.grid{flex:1;display:grid;grid-template-columns:1.6fr 1fr;gap:14px;min-height:0}
.card{background:var(--panel);border:1px solid var(--panel-brd);border-radius:18px;backdrop-filter:blur(14px);box-shadow:0 20px 50px rgba(0,0,0,.35);display:flex;flex-direction:column;min-height:0}
.card .hd{padding:13px 18px;border-bottom:1px solid var(--panel-brd);font-weight:600;font-size:13.5px;color:var(--mut);display:flex;align-items:center;gap:8px}
#chat{flex:1;overflow:auto;padding:18px;display:flex;flex-direction:column;gap:14px}
.msg{display:flex;gap:11px;max-width:86%;animation:in .3s ease}
@keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.msg .av{width:34px;height:34px;border-radius:11px;display:grid;place-items:center;font-size:17px;flex:none;background:linear-gradient(135deg,#2a2f3e,#1a1e29);border:1px solid var(--panel-brd)}
.msg .bub{padding:11px 14px;border-radius:14px;line-height:1.5;font-size:14.5px;white-space:pre-wrap;word-break:break-word}
.msg.me{align-self:flex-end;flex-direction:row-reverse}
.msg.me .bub{background:linear-gradient(135deg,var(--acc1),#5b8cff);color:#fff;border-bottom-right-radius:5px}
.msg.me .av{background:linear-gradient(135deg,var(--acc1),var(--acc2))}
.msg.bot .bub{background:var(--soft);border:1px solid var(--panel-brd);border-bottom-left-radius:5px}
.msg .who{font-size:11.5px;color:var(--mut);margin-bottom:4px}
.typing{display:flex;gap:5px;padding:4px 2px}
.typing span{width:7px;height:7px;border-radius:50%;background:var(--acc2);animation:blink 1.2s infinite}
.typing span:nth-child(2){animation-delay:.2s}.typing span:nth-child(3){animation-delay:.4s}
@keyframes blink{0%,80%,100%{opacity:.25;transform:translateY(0)}40%{opacity:1;transform:translateY(-4px)}}
.composer{display:flex;gap:10px;padding:14px;border-top:1px solid var(--panel-brd)}
.composer input{flex:1;background:var(--soft);border:1px solid var(--panel-brd);border-radius:12px;padding:12px 14px;color:var(--txt);font-size:14.5px;font-family:inherit;outline:none}
.composer input:focus{border-color:var(--acc1);box-shadow:0 0 0 3px rgba(124,92,255,.25)}
.composer button{border:0;border-radius:12px;padding:0 18px;font-weight:700;color:#fff;background:linear-gradient(135deg,var(--acc1),var(--acc2));cursor:pointer;font-size:14px}
.composer button:disabled{opacity:.5;cursor:default}
#ruteo{padding:18px;overflow:auto;display:flex;flex-direction:column;gap:16px}
.decide{background:linear-gradient(135deg,rgba(124,92,255,.18),rgba(34,211,238,.12));border:1px solid var(--panel-brd);border-radius:14px;padding:14px}
.decide .lbl{font-size:11.5px;color:var(--mut);text-transform:uppercase;letter-spacing:.6px}
.decide .agente{display:flex;align-items:center;gap:10px;margin-top:6px;font-weight:700;font-size:16px}
.decide .agente .av{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;font-size:16px;background:var(--soft2)}
.decide .motivo{color:var(--mut);font-size:13px;margin-top:8px;font-style:italic}
.steps{display:flex;flex-direction:column;gap:9px}
.step{display:flex;align-items:center;gap:11px;animation:in .35s ease both}
.step .ic{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;font-size:15px;flex:none}
.step .nm{font-size:13.5px;font-weight:600}
.step .tag{font-size:11px;color:var(--mut)}
.step .line{width:2px;height:12px;margin-left:14px;background:var(--panel-brd)}
.empty{color:var(--mut);font-size:13px;text-align:center;margin-top:30px;line-height:1.6}
code{font-family:'"'"'JetBrains Mono'"'"',monospace;font-size:12px;color:#c9d2ff}
@media(max-width:860px){.grid{grid-template-columns:1fr;grid-template-rows:1.4fr 1fr}.chips{display:none}}
.modal{position:fixed;inset:0;z-index:10;background:rgba(0,0,0,.5);backdrop-filter:blur(4px);display:none;place-items:center}
.modal.show{display:grid}
.sheet{width:min(92vw,470px);background:var(--panel);border:1px solid var(--panel-brd);border-radius:18px;backdrop-filter:blur(18px);padding:20px;box-shadow:0 30px 80px rgba(0,0,0,.5)}
.sheet-hd{display:flex;align-items:center;font-weight:700;font-size:16px;gap:8px}
.sheet .x{margin-left:auto;background:none;border:0;color:var(--mut);font-size:24px;cursor:pointer;line-height:1}
.sheet .hint{color:var(--mut);font-size:12.5px;line-height:1.55;margin:8px 0 16px}
.sheet label{display:block;font-size:13px;font-weight:600;margin-bottom:12px}
.sheet input,.sheet select,.sheet textarea{width:100%;margin-top:5px;background:var(--soft);border:1px solid var(--panel-brd);border-radius:10px;padding:10px 12px;color:var(--txt);font-size:13.5px;font-family:inherit;outline:none}
.sheet-ft{display:flex;gap:10px;justify-content:flex-end;margin-top:6px}
.btn-ghost{background:var(--soft);border:1px solid var(--panel-brd);color:var(--txt);border-radius:10px;padding:9px 16px;cursor:pointer;font-weight:600;font-family:inherit}
.btn-acc{background:linear-gradient(135deg,var(--acc1),var(--acc2));border:0;color:#fff;border-radius:10px;padding:9px 18px;cursor:pointer;font-weight:700;font-family:inherit}
.micbtn{border:1px solid var(--panel-brd);background:var(--soft);color:var(--txt);border-radius:12px;width:48px;font-size:18px;cursor:pointer;flex:none}
.micbtn.on{background:linear-gradient(135deg,#f43f5e,#fb7185);color:#fff;border-color:transparent;animation:micpulse 1.1s infinite}
@keyframes micpulse{0%{box-shadow:0 0 0 0 rgba(244,63,94,.5)}100%{box-shadow:0 0 0 12px rgba(244,63,94,0)}}.bub p{margin:.4em 0}.bub ul,.bub ol{margin:.4em 0;padding-left:1.25em}.bub li{margin:.15em 0}.bub strong{font-weight:700}.bub em{font-style:italic}.bub h3,.bub h4,.bub h5{margin:.5em 0 .3em;font-size:14.5px;font-weight:700}.bub code{background:var(--soft2);padding:1px 5px;border-radius:5px}
</style></head><body>
<div class="aurora"><i></i><i></i><i></i></div>
<div class="app">
  <header>
    <div class="logo">🧭</div>
    <div><h1>Tarea 2 · Agentes</h1><div class="sub">Supervisor A2A · enruta tu pregunta al agente correcto</div></div>
    <div class="chips" id="chips"></div>
    <button id="tts" class="tbtn" title="Leer respuestas en voz">🔈</button>
    <button id="nuevo" class="tbtn" title="Nueva conversación">🔄</button>
    <button id="theme" class="tbtn" title="Cambiar tema">🌙</button>
    <button id="salir" class="tbtn" title="Salir (cerrar sesión)">🚪</button>
  </header>
  <div class="grid">
    <div class="card">
      <div class="hd">💬 Chat</div>
      <div id="chat"><div class="empty">Escribe una pregunta — el supervisor la enviará al agente<br>que corresponda (clima, cocina chilena, reiki, machine learning…).</div></div>
      <form class="composer" id="form" autocomplete="off">
        <button type="button" id="mic" class="micbtn" title="Hablar">🎤</button>
        <input id="inp" placeholder="¿Qué clima hará hoy en Valdivia?" />
        <button id="btn" type="submit">Enviar</button>
      </form>
    </div>
    <div class="card">
      <div class="hd">🧭 Ruteo del coordinador</div>
      <div id="ruteo"><div class="empty">Aquí verás, por cada pregunta, a qué<br>agente enrutó el supervisor y el camino que recorrió.</div></div>
    </div>
  </div>
</div>
<div id="mailModal" class="modal"><div class="sheet"><div class="sheet-hd">✉️ Enviar por correo <button id="mailX" class="x">&times;</button></div><p class="hint">Se envía desde <b>tarea2curso2@etmk.cl</b>. Solo a destinatarios de la <b>allowlist</b>.</p><label>Para<select id="m_para"></select></label><label>Asunto<input id="m_asunto"></label><label>Mensaje<textarea id="m_cuerpo" rows="7" style="resize:vertical;font-family:inherit"></textarea></label><div id="m_estado" class="hint"></div><div class="sheet-ft"><button id="mailCancel" class="btn-ghost">Cancelar</button><button id="mailSend" class="btn-acc">Enviar</button></div></div></div>
<script>
let USUARIO="";let thread="";
const chat=document.getElementById("chat"),ruteo=document.getElementById("ruteo");
const CHAT_VACIO=chat.innerHTML, RUTEO_VACIO=ruteo.innerHTML;
let historial=[];
function guardarHist(){try{sessionStorage.setItem("t2_hist_"+USUARIO+"_"+thread,JSON.stringify(historial.slice(-60)));}catch(e){}}
function iniciarUsuario(u){USUARIO=u||"anon";thread=sessionStorage.getItem("t2_thread_"+USUARIO);if(!thread){thread=crypto.randomUUID();sessionStorage.setItem("t2_thread_"+USUARIO,thread);}historial=[];chat.innerHTML=CHAT_VACIO;ruteo.innerHTML=RUTEO_VACIO;restaurarHist();}
function restaurarHist(){let h=[];try{h=JSON.parse(sessionStorage.getItem("t2_hist_"+USUARIO+"_"+thread)||"[]");}catch(e){h=[];}if(!Array.isArray(h)||!h.length)return;historial=h;let u=null;h.forEach(x=>{if(x.rol==="me")burbuja("me",x.texto);else{burbuja("bot",x.texto,x.nombre,x.d);if(x.d)u=x.d;}});if(u)pintarRuteo(u);}
let ttsOn=localStorage.getItem("t2_tts")==="1";const ttsBtn=document.getElementById("tts");
function pintarTts(){ttsBtn.textContent=ttsOn?"🔊":"🔈";ttsBtn.style.opacity=ttsOn?"1":".6";}
ttsBtn.addEventListener("click",()=>{ttsOn=!ttsOn;localStorage.setItem("t2_tts",ttsOn?"1":"0");pintarTts();if(!ttsOn&&window.speechSynthesis)speechSynthesis.cancel();});pintarTts();
function hablar(txt){if(!ttsOn||!window.speechSynthesis)return;const u=new SpeechSynthesisUtterance(txt);u.lang="es-CL";const v=speechSynthesis.getVoices().find(v=>v.lang&&v.lang.toLowerCase().startsWith("es"));if(v)u.voice=v;speechSynthesis.cancel();speechSynthesis.speak(u);}
const SR=window.SpeechRecognition||window.webkitSpeechRecognition;const micBtn=document.getElementById("mic");let rec=null,escuchando=false;
if(SR){rec=new SR();rec.lang="es-CL";rec.interimResults=true;rec.continuous=false;rec.onresult=e=>{let t="";for(const r of e.results)t+=r[0].transcript;document.getElementById("inp").value=t;};rec.onend=()=>{escuchando=false;micBtn.classList.remove("on");};rec.onerror=()=>{escuchando=false;micBtn.classList.remove("on");};}else{micBtn.style.display="none";}
micBtn.addEventListener("click",()=>{if(!rec)return;if(escuchando){rec.stop();return;}try{document.getElementById("inp").value="";rec.start();escuchando=true;micBtn.classList.add("on");}catch(_){}});
const root=document.documentElement,tbtn=document.getElementById("theme");
if(localStorage.getItem("t2_theme")==="light")root.setAttribute("data-theme","light");
function pintarTema(){tbtn.textContent=root.getAttribute("data-theme")==="light"?"☀️":"🌙";}
tbtn.addEventListener("click",()=>{const l=root.getAttribute("data-theme")!=="light";if(l)root.setAttribute("data-theme","light");else root.removeAttribute("data-theme");localStorage.setItem("t2_theme",l?"light":"dark");pintarTema();});pintarTema();
document.getElementById("nuevo").addEventListener("click",()=>{thread=crypto.randomUUID();sessionStorage.setItem("t2_thread_"+USUARIO,thread);historial=[];chat.innerHTML=CHAT_VACIO;ruteo.innerHTML=RUTEO_VACIO;document.getElementById("inp").focus();});
document.getElementById("salir").addEventListener("click",()=>{if(confirm("¿Cerrar sesión?"))location.href="/logout";});
function meta(n){n=(n||"").toLowerCase();
 if(n.includes("machine")||n.includes("learning"))return{e:"🤖",c:"#7c5cff"};
 if(n.includes("bioinform")&&n.includes("ml"))return{e:"🧪",c:"#f472b6"};
 if(n.includes("ml en"))return{e:"🧪",c:"#f472b6"};
 if(n.includes("bioinform"))return{e:"🧬",c:"#2dd4bf"};
 if(n.includes("reiki"))return{e:"🧘",c:"#34d399"};
 if(n.includes("cocina"))return{e:"🍲",c:"#fb923c"};
 if(n.includes("meteor")||n.includes("clima"))return{e:"⛅",c:"#22d3ee"};
 if(n.includes("viaje"))return{e:"✈️",c:"#60a5fa"};
 if(n.includes("admin"))return{e:"🧭",c:"#a78bfa"};
 return{e:"🛰️",c:"#9aa3b6"};}
const PASOS={"guardia_entrada":{i:"🛡️",t:"Guardia de entrada",c:"#fbbf24"},"guardia_entrada:bloqueado":{i:"🛑",t:"Bloqueado (guardrail)",c:"#f87171"},"supervisor":{i:"🧭",t:"Supervisor (decide)",c:"#7c5cff"},"agente_local":{i:"🏠",t:"Agente local",c:"#34d399"},"agente_remoto":{i:"🌐",t:"Agente remoto",c:"#22d3ee"},"fallback_local":{i:"🏠",t:"Réplica local",c:"#fb923c"},"agente_no_disponible":{i:"⚠️",t:"Agente no disponible",c:"#fb923c"},"no_autorizado":{i:"🔒",t:"No autorizado",c:"#f87171"},"sin_agente":{i:"🤷",t:"Sin agente",c:"#9aa3b6"},"guardia_salida":{i:"🛡️",t:"Guardia de salida",c:"#fbbf24"}};
function _mdEsc(t){return t.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function _mdInline(t){t=_mdEsc(t);t=t.replace(/`([^`]+)`/g,"<code>$1</code>");t=t.replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>");t=t.replace(/__([^_]+)__/g,"<strong>$1</strong>");t=t.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g,"$1<em>$2</em>");return t;}
function mdToHtml(src){const lines=(src||"").split(/\r?\n/);let out="",para=[],i=0;function flush(){if(para.length){out+="<p>"+para.map(_mdInline).join("<br>")+"</p>";para=[];}}while(i<lines.length){const ln=lines[i];const mh=ln.match(/^\s*(#{1,4})\s+(.*)$/);const mu=ln.match(/^\s*[\*\-•]\s+(.*)$/);const mo=ln.match(/^\s*\d+[\.\)]\s+(.*)$/);if(mh){flush();const lv=Math.min(mh[1].length+2,6);out+="<h"+lv+">"+_mdInline(mh[2])+"</h"+lv+">";i++;continue;}if(mu||mo){flush();const ol=!!mo;const items=[];while(i<lines.length){const u=lines[i].match(/^\s*[\*\-•]\s+(.*)$/);const o=lines[i].match(/^\s*\d+[\.\)]\s+(.*)$/);if(ol&&o){items.push(o[1]);i++;}else if(!ol&&u){items.push(u[1]);i++;}else break;}out+="<"+(ol?"ol":"ul")+">"+items.map(x=>"<li>"+_mdInline(x)+"</li>").join("")+"</"+(ol?"ol":"ul")+">";continue;}if(ln.trim()===""){flush();i++;continue;}para.push(ln);i++;}flush();return out;}
function burbuja(cls,texto,nombre,d){
 const e=chat.querySelector(".empty");if(e)e.remove();
 const m=document.createElement("div");m.className="msg "+cls;
 const av=document.createElement("div");av.className="av";const bub=document.createElement("div");bub.className="bub";
 if(cls==="me"){av.textContent="🧑";bub.textContent=texto;}
 else{const mt=meta(nombre);av.textContent=mt.e;av.style.background="linear-gradient(135deg,"+mt.c+",rgba(255,255,255,.05))";
  if(nombre){const w=document.createElement("div");w.className="who";w.textContent=nombre;bub.appendChild(w);}
  const _c=document.createElement("div");_c.style.whiteSpace="normal";_c.innerHTML=mdToHtml(texto);bub.appendChild(_c);
  if(d&&((d.ruta&&d.ruta.length)||d.elegido)){const acc=document.createElement("div");acc.style.cssText="margin-top:8px";const b=document.createElement("button");b.type="button";b.textContent="🧭 Ver ruteo";b.style.cssText="font-size:12px;padding:4px 10px;border-radius:8px;cursor:pointer;border:1px solid var(--panel-brd);background:transparent;color:inherit;opacity:.85";b.addEventListener("click",()=>pintarRuteo(d));acc.appendChild(b);if(nombre&&window.__correoOK){const bm=document.createElement("button");bm.type="button";bm.textContent="✉️ Enviar por correo";bm.style.cssText=b.style.cssText;bm.addEventListener("click",()=>abrirMail(d));acc.appendChild(bm);}bub.appendChild(acc);}}
 m.appendChild(av);m.appendChild(bub);chat.appendChild(m);chat.scrollTop=chat.scrollHeight;return bub;}
function typing(){const e=chat.querySelector(".empty");if(e)e.remove();const m=document.createElement("div");m.className="msg bot";m.id="typing";m.innerHTML="<div class=\"av\">🧭</div><div class=\"bub\"><div class=\"typing\"><span></span><span></span><span></span></div></div>";chat.appendChild(m);chat.scrollTop=chat.scrollHeight;}
function pintarRuteo(d){ruteo.innerHTML="";const mt=meta(d.elegido);
 const dec=document.createElement("div");dec.className="decide";const el=d.elegido&&d.elegido!=="ninguno"?d.elegido:"ninguno (sin agente)";
 dec.innerHTML="<div class=\"lbl\">Agente elegido por el supervisor</div><div class=\"agente\"><span class=\"av\" style=\"background:linear-gradient(135deg,"+mt.c+",rgba(255,255,255,.08))\">"+mt.e+"</span>"+el+"</div>"+(d.motivo?"<div class=\"motivo\">«"+d.motivo+"»</div>":"");
 ruteo.appendChild(dec);
 if(d.origen){const det=document.createElement("div");det.style.cssText="padding:10px 12px;border:1px solid var(--panel-brd);border-radius:12px;background:var(--soft);font-size:12px";det.innerHTML="<div style=\"text-transform:uppercase;letter-spacing:.04em;opacity:.55;font-size:11px;margin-bottom:6px\">Antecedentes</div><div style=\"display:flex;justify-content:space-between\"><span style=\"opacity:.6\">Origen</span><code>"+d.origen+"</code></div>";ruteo.appendChild(det);}
 const steps=document.createElement("div");steps.className="steps";
 (d.ruta||[]).forEach((p,idx)=>{const info=PASOS[p]||{i:"•",t:p,c:"#9aa3b6"};const s=document.createElement("div");s.className="step";s.style.animationDelay=(idx*0.08)+"s";s.innerHTML="<span class=\"ic\" style=\"background:"+info.c+"22;border:1px solid "+info.c+"55\">"+info.i+"</span><div><div class=\"nm\">"+info.t+"</div><div class=\"tag\"><code>"+p+"</code></div></div>";steps.appendChild(s);if(idx<d.ruta.length-1){const l=document.createElement("div");l.className="line";steps.appendChild(l);}});
 ruteo.appendChild(steps);}
async function cargarChips(){try{const r=await fetch("api/agentes");if(!r.ok)return;const j=await r.json();const ags=j.agentes||[];document.getElementById("chips").innerHTML=ags.map(a=>{const mt=meta(a.nombre);return "<div class=\"chip\"><span class=\"dot\"></span>"+mt.e+" "+a.nombre+"</div>";}).join("");}catch(e){}}
document.getElementById("form").addEventListener("submit",async(e)=>{e.preventDefault();const inp=document.getElementById("inp"),btn=document.getElementById("btn");const texto=inp.value.trim();if(!texto)return;inp.value="";btn.disabled=true;burbuja("me",texto);historial.push({rol:"me",texto});typing();
 try{const r=await fetch("api/consulta",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({pregunta:texto,sesion:thread})});const d=await r.json();d.pregunta=texto;document.getElementById("typing")?.remove();const resp=d.respuesta||d.detail||d.error||"(sin respuesta)";burbuja("bot",resp,d.elegido,d);historial.push({rol:"bot",texto:resp,nombre:d.elegido,d});guardarHist();pintarRuteo(d);hablar(resp);}catch(err){document.getElementById("typing")?.remove();burbuja("bot","Error de conexión: "+err);historial.push({rol:"bot",texto:"Error de conexión: "+err,nombre:"",d:null});guardarHist();}finally{btn.disabled=false;inp.focus();}});
cargarChips();
async function onboarding(){let yo={},mc={};try{yo=await (await fetch("api/yo")).json();}catch(e){}iniciarUsuario(yo.usuario||"anon");if(yo.usuario){const sb=document.querySelector("header .sub");if(sb)sb.textContent=sb.textContent+" · "+yo.usuario;}if(yo.admin){const a=document.createElement("a");a.href="/usuarios";a.className="tbtn";a.title="Gestionar usuarios";a.textContent="👤";a.style.textDecoration="none";const h=document.querySelector("header");h.insertBefore(a,document.getElementById("nuevo"));}if(historial.length)return;try{mc=await (await fetch("api/mi-correo")).json();}catch(e){}const ch=chat.querySelector(".empty");if(!ch)return;const saludo="¡Hola"+(yo.usuario?(" "+yo.usuario):"")+"! Soy tu asistente. Pregúntame por el clima de ciudades de Chile, cocina chilena, reiki, machine learning, viajes y más — escribiendo o con el 🎤. A la derecha verás el ruteo, y puedes enviar una respuesta por ✉️ correo.";if(mc.correo){ch.innerHTML=saludo+"<br><br>📧 Tu correo registrado: <b>"+mc.correo+"</b>";return;}ch.innerHTML=saludo+"<br><br>📧 Para recibir respuestas por correo, registra tu email:<br><div style=\"margin-top:10px;display:flex;gap:8px;justify-content:center;flex-wrap:wrap\"><input id=\"onbmail\" placeholder=\"tucorreo@ejemplo.com\" style=\"padding:9px 12px;border-radius:10px;border:1px solid var(--panel-brd);background:var(--soft);color:var(--txt)\"><button id=\"onbbtn\" class=\"btn-acc\">Registrar</button></div><div id=\"onbmsg\" style=\"margin-top:8px;font-size:12.5px\"></div>";const bo=document.getElementById("onbbtn");bo.addEventListener("click",async()=>{const correo=document.getElementById("onbmail").value.trim();const mg=document.getElementById("onbmsg");if(!correo||correo.indexOf("@")<0){mg.textContent="Escribe un correo válido.";return;}bo.disabled=true;mg.textContent="Registrando…";try{const r=await fetch("api/registrar-correo",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({correo})});const j=await r.json();if(j.ok){mg.innerHTML="✅ ¡Listo! Tu correo <b>"+(j.correo||correo)+"</b> quedó registrado.";cargarCorreo();}else{mg.textContent="❌ "+(j.error||"no se pudo registrar");}}catch(e){mg.textContent="❌ "+e;}finally{bo.disabled=false;}});}
onboarding();
window.__correoOK=false;let __dest=[];async function cargarCorreo(){try{const r=await fetch("api/correo");if(!r.ok)return;const c=await r.json();window.__correoOK=!!c.configurado;__dest=c.destinatarios||[];}catch(e){}}const mailModal=document.getElementById("mailModal");function abrirMail(d){const sel=document.getElementById("m_para");sel.innerHTML=(__dest.length?__dest:["(sin destinatarios)"]).map(x=>"<option>"+x+"</option>").join("");document.getElementById("m_asunto").value="Respuesta del sistema de agentes"+(d.elegido?(" — "+d.elegido):"");document.getElementById("m_cuerpo").value=d.respuesta||"";document.getElementById("m_estado").textContent="";mailModal.__d=d;mailModal.classList.add("show");}function cerrarMail(){mailModal.classList.remove("show");}document.getElementById("mailX").addEventListener("click",cerrarMail);document.getElementById("mailCancel").addEventListener("click",cerrarMail);mailModal.addEventListener("click",e=>{if(e.target===mailModal)cerrarMail();});document.getElementById("mailSend").addEventListener("click",async()=>{const d=mailModal.__d||{};const para=document.getElementById("m_para").value,asunto=document.getElementById("m_asunto").value,mensaje=document.getElementById("m_cuerpo").value;const est=document.getElementById("m_estado"),b=document.getElementById("mailSend");if(!para||para.charAt(0)==="("){est.textContent="No hay destinatario.";return;}b.disabled=true;est.textContent="Enviando…";try{const r=await fetch("api/enviar",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({destinatario:para,asunto:asunto,mensaje:mensaje,pregunta:d.pregunta||"",agente:d.elegido||null,ruta:d.ruta||[]})});const j=await r.json();est.textContent=j.ok?"✅ Enviado.":("❌ "+(j.error||j.detail||"error"));if(j.ok)setTimeout(cerrarMail,900);}catch(e){est.textContent="❌ "+e;}finally{b.disabled=false;}});
cargarCorreo();
</script></body></html>"""

PAGINA_VOZ = """<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Tarea 2 · Voz</title>
<style>
 body{font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;max-width:720px;margin:0 auto;padding:16px;color:#222;background:#fafafa}
 h1{font-size:20px} .sub{color:#888;font-weight:400;font-size:15px} a{color:#0a7}
 .panel{display:flex;align-items:center;gap:14px;margin:16px 0}
 .mic{width:72px;height:72px;border-radius:50%;border:0;background:#0b5;color:#fff;font-size:30px;cursor:pointer;transition:transform .1s}
 .mic.on{background:#e23;animation:pulse 1s infinite} .mic:disabled{background:#bbb;cursor:not-allowed}
 @keyframes pulse{0%{box-shadow:0 0 0 0 rgba(226,51,51,.5)}100%{box-shadow:0 0 0 16px rgba(226,51,51,0)}}
 .estado{font-size:15px;color:#555;padding:6px 12px;border-radius:20px;background:#eee}
 .estado.on{background:#dff3e6;color:#0a6} .estado.err{background:#fdecea;color:#c0392b}
 label{display:block;margin:10px 0 4px;color:#444;font-size:14px}
 input[type=text]{width:100%;box-sizing:border-box;padding:10px;border:1px solid #ccc;border-radius:8px}
 .row{display:flex;gap:12px;align-items:center;margin-top:10px}
 button#enviar{padding:10px 16px;border:0;border-radius:8px;background:#0b5;color:#fff;cursor:pointer}
 .tts{font-size:14px;color:#444} .resp{margin-top:16px;background:#fff;border:1px solid #e3e3e3;border-radius:10px;padding:14px;white-space:pre-wrap;line-height:1.5;min-height:60px}
</style></head><body>
<h1>Avatar por voz <span class=sub>— Tarea 2 · Etapa A</span></h1>
<p>Habla y el sistema te responde en voz. <a href=".">Ir al chat de texto</a></p>
<div class=panel><button id=mic class=mic title="Hablar">🎤</button><div id=estado class=estado>listo</div></div>
<label for=q>Transcripción (puedes corregirla antes de enviar):</label>
<input id=q type=text placeholder="Tu consulta aparecerá aquí al hablar…" autocomplete=off>
<div class=row><button id=enviar>Enviar</button>
<label class=tts><input type=checkbox id=leer checked> Leer la respuesta en voz</label></div>
<div id=resp class=resp></div>
<script>
 const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
 const mic=document.getElementById('mic'),estado=document.getElementById('estado'),
       q=document.getElementById('q'),resp=document.getElementById('resp'),leer=document.getElementById('leer');
 function setEstado(t,cls){estado.textContent=t;estado.className='estado '+(cls||'');}
 let rec=null,escuchando=false;
 if(SR){
   rec=new SR();rec.lang='es-CL';rec.interimResults=true;rec.continuous=false;
   rec.onresult=e=>{let t='';for(const r of e.results)t+=r[0].transcript;q.value=t;};
   rec.onend=()=>{escuchando=false;mic.classList.remove('on');if(estado.textContent==='escuchando…')setEstado('listo');};
   rec.onerror=e=>{escuchando=false;mic.classList.remove('on');setEstado('error de micrófono: '+e.error,'err');};
 }else{setEstado('tu navegador no soporta dictado por voz; escribe la consulta','err');mic.disabled=true;}
 mic.onclick=()=>{if(!rec)return;if(escuchando){rec.stop();return;}
   try{q.value='';rec.start();escuchando=true;mic.classList.add('on');setEstado('escuchando…','on');}catch(_){}};
 function hablar(txt){if(!leer.checked||!window.speechSynthesis)return;
   const u=new SpeechSynthesisUtterance(txt);u.lang='es-CL';
   const v=speechSynthesis.getVoices().find(v=>v.lang&&v.lang.toLowerCase().startsWith('es'));if(v)u.voice=v;
   setEstado('hablando…','on');u.onend=()=>setEstado('listo');speechSynthesis.cancel();speechSynthesis.speak(u);}
 async function enviar(){const texto=q.value.trim();if(!texto)return;if(rec&&escuchando)rec.stop();
   resp.textContent='';setEstado('pensando…','on');
   try{const r=await fetch('api/consulta',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({pregunta:texto})});
     const d=await r.json();
     if(!r.ok){setEstado('error','err');resp.textContent='Error: '+(d.detail||d.error||r.status);return;}
     const t=d.respuesta||'(sin respuesta)';
     resp.textContent=t+(d.ruta?('\\n\\nruta: '+d.ruta.join(' → ')+(d.elegido?(' · '+d.elegido):'')):'');
     setEstado('listo');hablar(t);
   }catch(err){setEstado('error de red','err');resp.textContent=''+err;}}
 document.getElementById('enviar').onclick=enviar;
 q.addEventListener('keydown',e=>{if(e.key==='Enter')enviar();});
 if(window.speechSynthesis){speechSynthesis.onvoiceschanged=()=>{};}
</script></body></html>"""


def _proxy(metodo: str, ruta: str, cuerpo: bytes | None = None, usuario: str | None = None):
    req = urllib.request.Request(f"{API_BASE}{ruta}", data=cuerpo, method=metodo)
    req.add_header("X-API-Key", API_KEY)
    if usuario:
        req.add_header("X-Usuario", usuario)
    if cuerpo is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:  # noqa: BLE001
        return 502, json.dumps({"error": f"gateway no disponible: {e}"}).encode()


# --- Usuarios con login por sesión (clave única inicial + cambio obligatorio) ---
WEB_USUARIOS = [u.strip() for u in os.environ.get("WEB_USUARIOS", "").split(",") if u.strip()]
WEB_ADMIN = os.environ.get("WEB_ADMIN", "")
CLAVE_INICIAL = os.environ.get("CLAVE_INICIAL", "")
if WEB_USUARIOS and CLAVE_INICIAL:
    usuarios.seed(WEB_USUARIOS, CLAVE_INICIAL, WEB_ADMIN)

SESIONES: dict = {}
SESION_TTL = 8 * 3600  # caducidad de la sesion (8 h)
INTENTOS: dict = {}
MAX_FALLOS = 6
VENTANA_FALLOS = 300  # 5 min


def _throttled(usuario):
    rec = INTENTOS.get(usuario)
    return bool(rec and rec[0] >= MAX_FALLOS and (time.time() - rec[1]) < VENTANA_FALLOS)


def _fallo(usuario):
    rec = INTENTOS.get(usuario, [0, 0.0])
    if time.time() - rec[1] > VENTANA_FALLOS:
        rec = [0, time.time()]
    INTENTOS[usuario] = [rec[0] + 1, time.time()]


def _ok_login(usuario):
    INTENTOS.pop(usuario, None)


def _nueva_sesion(usuario):
    tok = secrets.token_urlsafe(24)
    SESIONES[tok] = {"usuario": usuario, "ts": time.time()}
    return tok


def _usuario_sesion(headers):
    for part in headers.get("Cookie", "").split(";"):
        if "=" in part:
            k, v = part.strip().split("=", 1)
            if k == "t2sid":
                ses = SESIONES.get(v)
                if ses and (time.time() - ses["ts"]) < SESION_TTL:
                    return ses["usuario"]
    return None


_ESTILO_AUTH = """<style>
body{font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#0b0d13;color:#e8eaf0;display:grid;place-items:center;min-height:100vh;margin:0}
.card{background:#161922;border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:28px;width:min(92vw,380px);box-shadow:0 20px 60px rgba(0,0,0,.5)}
h2{margin:0 0 4px;font-size:20px}.sub{color:#9aa3b6;font-size:13px;margin-bottom:12px}
label{display:block;font-size:13px;color:#9aa3b6;margin:12px 0 4px}
input{width:100%;box-sizing:border-box;padding:11px 13px;border-radius:10px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.05);color:#e8eaf0;font-size:14px}
button{width:100%;margin-top:18px;padding:12px;border:0;border-radius:10px;background:linear-gradient(135deg,#7c5cff,#22d3ee);color:#fff;font-weight:700;font-size:15px;cursor:pointer}
.err{background:#3b1d22;color:#f8b4b4;border:1px solid #7f3f46;border-radius:8px;padding:8px 10px;font-size:13px;margin-top:12px}
table{width:100%;border-collapse:collapse;font-size:13px;margin-top:10px}th,td{border:1px solid rgba(255,255,255,.1);padding:6px 8px;text-align:left}a{color:#67e8f9}
</style>"""


def _pagina_login(error=""):
    e = '<div class="err">' + html.escape(error) + '</div>' if error else ''
    return ('<!doctype html><html lang=es><head><meta charset=utf-8>'
            '<meta name=viewport content="width=device-width,initial-scale=1"><title>Ingreso - Tarea 2</title>'
            + _ESTILO_AUTH + '</head><body><form class=card method=post action="/login">'
            '<h2>Tarea 2 - Agentes</h2><div class=sub>Inicia sesion con tu usuario.</div>'
            '<label>Usuario</label><input name=usuario autofocus autocomplete=username>'
            '<label>Clave</label><input name=clave type=password autocomplete=current-password>'
            + e + '<button type=submit>Entrar</button></form></body></html>')


def _pagina_cambiar(usuario, obligatorio=False, error=""):
    e = '<div class="err">' + html.escape(error) + '</div>' if error else ''
    aviso = ('<div class=sub>Es tu primer ingreso: define una clave nueva (minimo 6 caracteres).</div>'
             if obligatorio else '<div class=sub>Cambia tu clave.</div>')
    return ('<!doctype html><html lang=es><head><meta charset=utf-8>'
            '<meta name=viewport content="width=device-width,initial-scale=1"><title>Cambiar clave</title>'
            + _ESTILO_AUTH + '</head><body><form class=card method=post action="/cambiar-clave">'
            '<h2>Hola, ' + html.escape(usuario) + '</h2>' + aviso +
            '<label>Nueva clave</label><input name=nueva type=password autocomplete=new-password autofocus>'
            '<label>Repite la clave</label><input name=confirmar type=password autocomplete=new-password>'
            + e + '<button type=submit>Guardar</button></form></body></html>')


def _pagina_admin(usuario):
    filas = ''
    for u in usuarios.listar():
        estado = 'pendiente de cambio' if u['debe_cambiar'] else 'ok'
        filas += ('<tr><td>' + html.escape(u['usuario']) + '</td><td>' + html.escape(u['rol']) + '</td><td>'
                  + estado + '</td><td><form method=post action="/usuarios/reset" style="display:flex;gap:6px;margin:0">'
                  '<input type=hidden name=usuario value="' + html.escape(u['usuario']) + '">'
                  '<input name=nueva type=text placeholder="nueva clave" style="width:150px">'
                  '<button style="width:auto;margin:0;padding:6px 10px">Resetear</button></form></td></tr>')
    return ('<!doctype html><html lang=es><head><meta charset=utf-8>'
            '<meta name=viewport content="width=device-width,initial-scale=1"><title>Usuarios - Admin</title>'
            + _ESTILO_AUTH + '</head><body><div class=card style="width:min(94vw,680px)">'
            '<h2>Gestion de usuarios</h2><div class=sub>Admin: ' + html.escape(usuario) +
            ' - <a href="/">volver al chat</a></div>'
            '<table><tr><th>Usuario</th><th>Rol</th><th>Estado</th><th>Resetear clave</th></tr>' + filas +
            '</table><div class=sub style="margin-top:12px">Al resetear, el usuario debera cambiarla en su proximo ingreso.</div>'
            '</div></body></html>')


class Handler(BaseHTTPRequestHandler):
    def _html(self, code, body, ctype="text/html; charset=utf-8", cookie=None):
        if isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code, obj):
        self._html(code, json.dumps(obj).encode(), ctype="application/json")

    def _redirect(self, to, cookie=None):
        self.send_response(302)
        self.send_header("Location", to)
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _ruta(self):
        return self.path.split("?", 1)[0]

    def _form(self):
        n = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(n).decode("utf-8", "replace") if n else ""
        return urllib.parse.parse_qs(raw)

    def _cuerpo(self):
        n = int(self.headers.get("Content-Length", "0"))
        return self.rfile.read(n) if n else b"{}"

    def do_GET(self):  # noqa: N802
        ruta = self._ruta()
        if ruta == "/login":
            if _usuario_sesion(self.headers):
                return self._redirect("/")
            return self._html(200, _pagina_login())
        if ruta == "/logout":
            for part in self.headers.get("Cookie", "").split(";"):
                if "=" in part:
                    k, v = part.strip().split("=", 1)
                    if k == "t2sid":
                        _ses = SESIONES.pop(v, None)
                        if _ses:
                            try:
                                memoria.registrar_evento(_ses["usuario"], "logout")
                            except Exception:  # noqa: BLE001
                                pass
            return self._redirect("/login", cookie="t2sid=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax; Secure")
        usuario = _usuario_sesion(self.headers)
        if not usuario:
            if ruta.startswith("/api/"):
                return self._json(401, {"error": "no autenticado"})
            return self._redirect("/login")
        if usuarios.debe_cambiar(usuario) and ruta != "/cambiar-clave":
            if ruta.startswith("/api/"):
                return self._json(409, {"error": "debe cambiar su clave"})
            return self._redirect("/cambiar-clave")
        if ruta == "/cambiar-clave":
            return self._html(200, _pagina_cambiar(usuario, usuarios.debe_cambiar(usuario)))
        if ruta == "/usuarios":
            if not usuarios.es_admin(usuario):
                return self._html(403, "<p>Solo el administrador puede ver esto.</p>")
            return self._html(200, _pagina_admin(usuario))
        if ruta in ("/", "/index.html"):
            return self._html(200, PAGINA)
        if ruta in ("/voz", "/voz/"):
            return self._html(200, PAGINA_VOZ)
        if ruta == "/api/yo":
            return self._json(200, {"usuario": usuario, "admin": usuarios.es_admin(usuario)})
        if ruta == "/api/usuarios":
            if not usuarios.es_admin(usuario):
                return self._json(403, {"error": "solo admin"})
            return self._json(200, {"usuarios": usuarios.listar()})
        mapa = {"/api/salud": "/salud", "/api/agentes": "/agentes",
                "/api/destinatarios": "/destinatarios", "/api/correo": "/correo",
                "/api/mi-correo": "/mi-correo"}
        if ruta in mapa:
            return self._html(*_proxy("GET", mapa[ruta], usuario=usuario), ctype="application/json")
        return self._json(404, {"error": "no encontrado"})

    def do_POST(self):  # noqa: N802
        ruta = self._ruta()
        if ruta == "/login":
            f = self._form()
            u = (f.get("usuario", [""])[0]).strip()
            p = f.get("clave", [""])[0]
            if _throttled(u):
                return self._html(429, _pagina_login("Demasiados intentos. Espera unos minutos."))
            if usuarios.verificar(u, p):
                _ok_login(u)
                try:
                    memoria.registrar_evento(u, "login")
                except Exception:  # noqa: BLE001
                    pass
                tok = _nueva_sesion(u)
                destino = "/cambiar-clave" if usuarios.debe_cambiar(u) else "/"
                return self._redirect(destino, cookie="t2sid=" + tok + "; Path=/; HttpOnly; SameSite=Lax; Secure")
            _fallo(u)
            time.sleep(0.5)
            return self._html(401, _pagina_login("Usuario o clave incorrectos."))
        usuario = _usuario_sesion(self.headers)
        if not usuario:
            if ruta.startswith("/api/"):
                return self._json(401, {"error": "no autenticado"})
            return self._redirect("/login")
        if ruta == "/cambiar-clave":
            f = self._form()
            nueva = f.get("nueva", [""])[0]
            conf = f.get("confirmar", [""])[0]
            if nueva != conf:
                return self._html(200, _pagina_cambiar(usuario, usuarios.debe_cambiar(usuario), "Las claves no coinciden."))
            if not usuarios.cambiar_clave(usuario, nueva):
                return self._html(200, _pagina_cambiar(usuario, usuarios.debe_cambiar(usuario), "La clave debe tener al menos 6 caracteres."))
            try:
                memoria.registrar_evento(usuario, "cambio_clave")
            except Exception:  # noqa: BLE001
                pass
            return self._redirect("/")
        if usuarios.debe_cambiar(usuario):
            if ruta.startswith("/api/"):
                return self._json(409, {"error": "debe cambiar su clave"})
            return self._redirect("/cambiar-clave")
        if ruta == "/usuarios/reset":
            if not usuarios.es_admin(usuario):
                return self._html(403, "<p>Solo el administrador.</p>")
            f = self._form()
            _obj = f.get("usuario", [""])[0]
            usuarios.resetear_clave(_obj, f.get("nueva", [""])[0])
            try:
                memoria.registrar_evento(_obj, "reset_admin")
            except Exception:  # noqa: BLE001
                pass
            return self._redirect("/usuarios")
        mapa = {"/api/consulta": "/consulta", "/api/enviar": "/enviar",
                "/api/registrar-correo": "/registrar-correo"}
        if ruta in mapa:
            return self._html(*_proxy("POST", mapa[ruta], self._cuerpo(), usuario=usuario), ctype="application/json")
        return self._json(404, {"error": "no encontrado"})

    def log_message(self, *a):
        return


def main() -> None:
    print("BFF web en http://" + HOST + ":" + str(PORT) + " -> " + API_BASE + " (login por sesion)")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
