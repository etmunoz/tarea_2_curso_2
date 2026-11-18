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
| `t2c2-web` | 8797 | Frontend **BFF** (chat `/` y voz `/voz`); añade la API_KEY server-side. |
| *(pendiente)* `t2c2-monitor` | 8798 | Backoffice repropuesto (fail2ban, accesos, despachos, historial). |

## Requisitos previos

- **`/etc/t2c2.env`** con los secretos (ver `deploy/t2c2.env.example`): `GOOGLE_API_KEY`, `API_KEY`,
  `WEB_USER`/`WEB_PASS`, y (para correo) `SMTP_*`. Sin `GOOGLE_API_KEY` los agentes no responden.
- **Swap** recomendado antes de dejar todo corriendo (la RAM está ajustada; ver evaluación de la VPS,
  registro 001). Revisar también `clamd` (≈966 MB).

## Instalación (como `administrator`, con sudo)

```bash
# 1) EnvironmentFile con los secretos (NO versionado)
sudo cp deploy/t2c2.env.example /etc/t2c2.env
sudo nano /etc/t2c2.env                 # completar valores reales
sudo chown root:web6 /etc/t2c2.env && sudo chmod 640 /etc/t2c2.env

# 2) Instalar los units
sudo cp deploy/systemd/t2c2-*.service /etc/systemd/system/
sudo systemctl daemon-reload

# 3) Habilitar y arrancar EN ORDEN
sudo systemctl enable --now t2c2-langgraph
sudo systemctl enable --now t2c2-fichas
sudo systemctl enable --now t2c2-api
sudo systemctl enable --now t2c2-web

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

1. **Website** en ISPConfig para `tarea2curso2.etmk.cl` (y luego `monitortarea2curso2.etmk.cl`).
2. **Redirect** tipo **proxy** a `http://127.0.0.1:8797/` (el monitor, cuando exista, a `:8798`).
3. **SSL + Let's Encrypt** en ese website.
4. **Force-HTTPS ANTES del proxy** — en *Options → Apache Directives*, antes de la regla de proxy:
   ```apache
   RewriteEngine On
   RewriteCond %{HTTPS} off
   RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
   ```
   (así `http://` nunca llega en claro al backend; la API_KEY/Basic Auth viaja siempre cifrada).

El **login del sitio** (Basic Auth del BFF) lo controla `WEB_USER`/`WEB_PASS`. Los agentes (`:2025`) y el
gateway (`:8796`) **no** se publican: solo 127.0.0.1.

## Detener / reiniciar

```bash
sudo systemctl restart t2c2-api
sudo systemctl stop t2c2-web t2c2-api t2c2-fichas t2c2-langgraph   # orden inverso
```
