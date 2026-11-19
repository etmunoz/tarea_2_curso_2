<!--encabezado-grupo-->
> **Archivo:** `deploy/README-T2.md`  
> **Objetivo:** Guía de despliegue y publicación de la Tarea 2 (servicios systemd t2c2-* + proxy ISPConfig)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
<!--/encabezado-grupo-->

# Despliegue — Tarea 2 (web6)

App publicada **directo en la VPS**, en el home del Shell-User `etmkuseretmk2` (sistema `web6`,
grupo `client1`): `/var/www/clients/client1/web6/home/etmkuseretmk2/tarea_2_curso_2`. **Aislada** de
web1 (Tarea 1) y web5 (lucecitaOS).

## Servicios y puertos (todo en 127.0.0.1)

| Servicio | Puerto | Rol |
|---|---|---|
| `t2c2-langgraph` | 2025 | `langgraph dev` con los 8 agentes locales (A2A nativo). Base de todo. |
| `t2c2-fichas` | — | Vigilante: re-aplica las fichas (agent cards) cuando langgraph las borra. |
| `t2c2-api` | 8796 | Gateway **FastAPI** protegido por **API_KEY**. Único acceso a los agentes. |
| `t2c2-web` | 8797 | Frontend **BFF** (chat + voz integrada, login por sesión); añade API_KEY + X-Usuario server-side. |
| `t2c2-monitor` | 8798 | Backoffice: accesos (200/401), despachos, allowlist, eventos de usuario, cuota Gemini y `/config`. |

## Requisitos previos

- **`/etc/t2c2.env`** con los secretos (ver `deploy/t2c2.env.example`): `GOOGLE_API_KEY`, `API_KEY`,
  `WEB_USUARIOS`/`WEB_ADMIN`/`CLAVE_INICIAL` (login multiusuario), `MONITOR_*`, y (para correo) `SMTP_*`.
  Sin `GOOGLE_API_KEY` los agentes no responden. Alternativa sin editar `/etc`: fijar `GOOGLE_API_KEY`,
  `API_KEY`, `SMTP_PASS` y `REDIS_URL` por el **almacén de config** (`/config` del monitor, o
  `deploy/set_redis_url.sh` para la `REDIS_URL`).
- **Swap** recomendado antes de dejar todo corriendo (la RAM está ajustada; ver evaluación de la VPS,
  registro 001). Revisar también `clamd` (≈966 MB).

## Instalación (como `administrator`, con sudo)

```bash
# 1) EnvironmentFile con los secretos (NO versionado)
sudo cp deploy/t2c2.env.example /etc/t2c2.env
sudo nano /etc/t2c2.env                 # completar valores reales
sudo chown root:client1 /etc/t2c2.env && sudo chmod 640 /etc/t2c2.env   # grupo client1: web6 lo lee

# 2) Instalar los units
sudo cp deploy/systemd/t2c2-*.service /etc/systemd/system/
sudo systemctl daemon-reload

# 3) Habilitar y arrancar EN ORDEN
sudo systemctl enable --now t2c2-langgraph
sudo systemctl enable --now t2c2-fichas
sudo systemctl enable --now t2c2-api
sudo systemctl enable --now t2c2-web
sudo systemctl enable --now t2c2-monitor

# 4) Verificar
curl -s http://127.0.0.1:8796/salud                       # {"estado":"ok"}
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8796/agentes            # 401 (sin API_KEY)
curl -s -o /dev/null -w "%{http_code}\n" -H "X-API-Key: <API_KEY>" http://127.0.0.1:8796/agentes  # 200
systemctl status t2c2-langgraph t2c2-api t2c2-web --no-pager
```

> `t2c2-langgraph` tarda en responder al primer arranque (descarga/arranque). `t2c2-fichas` y
> `t2c2-api` esperan a `:2025/ok` por su orden de dependencias.

## Publicación con proxy (ISPConfig) — SIN tocar DNS

Los subdominios `*.etmk.cl` ya resuelven (wildcard). Por **cada** subdominio:

1. **Website** en ISPConfig para `tarea2curso2.etmk.cl` y `monitortarea2curso2.etmk.cl`.
2. **Redirect** tipo **proxy**: el sitio a `http://127.0.0.1:8797/`, el monitor a `http://127.0.0.1:8798/`.
3. **SSL + Let's Encrypt** en ese website.
4. **Force-HTTPS ANTES del proxy** — en *Options → Apache Directives*, antes de la regla de proxy:
   ```apache
   RewriteEngine On
   RewriteCond %{HTTPS} off
   RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
   # HSTS (fallo 6 de evidencias/fallos.md): forzar HTTPS en el navegador por 1 año.
   Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
   ```
   (así `http://` nunca llega en claro al backend; la cookie de sesión y la API_KEY viajan cifradas).
   Las demás cabeceras de seguridad (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`) y el
   `Server: t2c2` ya los pone el BFF en `src/canales/web.py`; **HSTS** es lo único que debe ir aquí, en el
   proxy (requiere el módulo `headers` de Apache, habitualmente activo en ISPConfig).

El **login del sitio** es **por sesión** (no Basic Auth): usuarios de `WEB_USUARIOS` con clave propia
(hash PBKDF2+salt), `CLAVE_INICIAL` única con cambio obligatorio y cookie `Secure`. El **monitor** usa
`MONITOR_USER`/`MONITOR_PASS`. Los agentes (`:2025`) y el gateway (`:8796`) **no** se publican: solo
127.0.0.1. Tras desplegar el RAG a Redis, reiniciar con `sudo systemctl restart t2c2-langgraph`.

## Red / hardening (egress permitido)

La máquina tuvo hardening por ataques. Para que un endurecimiento futuro **no rompa** el sistema, estos
son los accesos que necesita. Verificado operativo el 2026-11-19 (ver `evidencias/EVIDENCIAS.md`, Anexo 12).

**Entrante (inbound):** solo **80/443** públicos (proxy ISPConfig → fuerza HTTPS). Los servicios
(`:2025`, `:8796`, `:8797`, `:8798`) escuchan **solo en 127.0.0.1**; no deben exponerse.

**Saliente (egress) — destinos HTTPS (443) que el sistema DEBE poder alcanzar:**

| Servicio | Host(s) | Usado por |
|---|---|---|
| Gemini (LLM + embeddings) | `generativelanguage.googleapis.com` | supervisor y agentes; RAG de Reiki |
| Open-Meteo | `geocoding-api.open-meteo.com`, `api.open-meteo.com`, `archive-api.open-meteo.com` | meteorología, viajes |
| UniProt | `rest.uniprot.org` | bioinformática |
| Tipo de cambio | `open.er-api.com` | viajes |
| Wikipedia | `es.wikipedia.org` | viajes |
| Redis cloud (RediSearch) | el host:puerto del `REDIS_URL` (p. ej. `…redis.io:10484`, **no** 443) | RAG de Reiki |

- **Correo (SMTP):** `SMTP_HOST=localhost:587` → es **local** (Postfix de la máquina), no requiere egress externo.
- **DNS saliente** debe estar permitido para resolver esos hosts.
- Si se agrega un firewall de **egress por defecto-deny**, hay que **allowlistear** los hosts de arriba
  (y el puerto no estándar del Redis). Un bloqueo se nota como *timeout/conexión rechazada* en el agente
  correspondiente (no un 4xx).

## Detener / reiniciar

```bash
sudo systemctl restart t2c2-api
sudo systemctl stop t2c2-monitor t2c2-web t2c2-api t2c2-fichas t2c2-langgraph   # orden inverso
```
