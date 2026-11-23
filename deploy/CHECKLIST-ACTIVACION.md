<!--encabezado-grupo-->
> **Archivo:** `deploy/CHECKLIST-ACTIVACION.md`  
> **Objetivo:** Checklist para activar la Tarea 2 en la VPS (secretos + servicios + publicación)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
<!--/encabezado-grupo-->

# Checklist de activación — Tarea 2 (web6)

## 0. Antes de empezar (recomendado)
- [ ] **Swap** (la RAM está ajustada): crear 2 GB y activarlo.
  ```bash
  sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile
  sudo mkswap /swapfile && sudo swapon /swapfile
  echo "/swapfile none swap sw 0 0" | sudo tee -a /etc/fstab
  free -h
  ```
- [ ] (Opcional) revisar `clamd` (≈966 MB) si la RAM queda corta.

## 1. Secretos — `/etc/t2c2.env`
- [ ] Editar el borrador y **pegar** `GOOGLE_API_KEY` y `SMTP_PASS` (las demás ya vienen generadas):
  ```bash
  nano ~/t2c2.env.borrador      # (como etmkuseretmk2)
  ```
- [ ] Instalarlo en /etc (como administrator):
  ```bash
  sudo cp /var/www/clients/client1/web6/home/etmkuseretmk2/t2c2.env.borrador /etc/t2c2.env
  sudo chown root:client1 /etc/t2c2.env && sudo chmod 640 /etc/t2c2.env   # grupo client1: web6 lo lee
  ```
- [ ] (Opcional) **MCP de clima** `meteo_mcp`: pegar `MCP_SERVER_METEOSOURCE`, `URL_METEO_MCP`,
  `MCP_BEARER_TOKEN_ENV_VAR` (token de pago) e incluir `meteo_mcp` en `A2A_GRAFOS_LOCALES`. Sin esto,
  `meteo_mcp` usa el respaldo keyless Open-Meteo.
- [ ] (Opcional) **Memoria durable del coordinador**: crear rol/base `t2c2` en Postgres, rotar la clave
  en el VPS y dejar `PG_DSN=postgresql://t2c2:***@localhost:5432/t2c2` (ver `deploy/README-T2.md`). Sin
  esto, el coordinador usa `InMemorySaver`.

## 2. Servicios systemd
- [ ] Instalar y recargar:
  ```bash
  cd /var/www/clients/client1/web6/home/etmkuseretmk2/tarea_2_curso_2
  sudo cp deploy/systemd/t2c2-*.service /etc/systemd/system/
  sudo systemctl daemon-reload
  ```
- [ ] Habilitar y arrancar **en orden**:
  ```bash
  sudo systemctl enable --now t2c2-langgraph
  sudo systemctl enable --now t2c2-fichas
  sudo systemctl enable --now t2c2-api
  sudo systemctl enable --now t2c2-web
  sudo systemctl enable --now t2c2-monitor
  ```
- [ ] Ver estado: `systemctl status t2c2-* --no-pager`

## 3. Verificación local (en la VPS)
- [ ] Gateway salud/ acceso:
  ```bash
  curl -s http://127.0.0.1:8796/salud
  curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8796/agentes            # 401
  API_KEY=$(sudo grep '^API_KEY=' /etc/t2c2.env | cut -d= -f2)
  curl -s -o /dev/null -w "%{http_code}\n" -H "X-API-Key: $API_KEY" http://127.0.0.1:8796/agentes  # 200
  ```
- [ ] Consulta integrada (requiere GOOGLE_API_KEY y los agentes):
  ```bash
  curl -s -X POST http://127.0.0.1:8796/consulta -H "X-API-Key: $API_KEY" \
       -H "Content-Type: application/json" -d '{"pregunta":"clima hoy en Valdivia"}'
  ```

## 4. Publicación (ISPConfig, con proxy, SIN DNS)
- [ ] Website `tarea2curso2.etmk.cl` → Redirect **proxy** a `http://127.0.0.1:8797/`.
- [ ] Website `monitortarea2curso2.etmk.cl` → Redirect **proxy** a `http://127.0.0.1:8798/`.
- [ ] SSL + Let's Encrypt en cada uno.
- [ ] **Force-HTTPS antes del proxy** (Options → Apache Directives):
  ```apache
  RewriteEngine On
  RewriteCond %{HTTPS} off
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
  ```

## 5. Prueba end-to-end (evidencias de rúbrica)
- [ ] Chat de texto en `https://tarea2curso2.etmk.cl/` (login WEB_USER/WEB_PASS).
- [ ] Voz en `https://tarea2curso2.etmk.cl/voz` (Chrome/Edge, permiso de micrófono) → audio/video.
- [ ] Correo: registrar un destinatario y disparar un envío → captura del correo recibido (con ruta + grafo).
- [ ] Monitor en `https://monitortarea2curso2.etmk.cl/` (login MONITOR_USER/MONITOR_PASS): accesos 200/401.
- [ ] Capturar acceso **permitido (200)** y **rechazado (401)** sin exponer la API_KEY.

## 6. Detener / reiniciar
```bash
sudo systemctl restart t2c2-api
sudo systemctl stop t2c2-monitor t2c2-web t2c2-api t2c2-fichas t2c2-langgraph
```
