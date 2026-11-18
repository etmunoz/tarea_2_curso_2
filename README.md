<!--encabezado-grupo-->
> **Archivo:** `README.md`  
> **Objetivo:** Tarea 2 · Curso 2 — implementación y ejecución local del sistema de agentes  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
<!--/encabezado-grupo-->

# Tarea 2 · Curso 2 — Sistema de agentes (local y reproducible)

Evolución del Taller 1: los agentes A2A se conectan a **canales de uso reales**, todo **LOCAL** y
reproducible. **Todo en español**, horarios en `America/Santiago`.

## Las 3 implementaciones

1. **Servicio FastAPI** — gateway **único** a los agentes, protegido por **`API_KEY`** (header
   `X-API-Key`; sin clave válida → 401). Es el núcleo: ningún frontend llama a los agentes directo.
2. **Canal web + correo** — frontend de chat (BFF que habla con FastAPI, con la API_KEY server-side) y
   **despacho por correo** a destinatarios **registrados** (allowlist), con la **ruta de los agentes** y
   el **gráfico del grafo** al pie.
3. **Avatar por voz (Etapa A)** — se habla al sitio: **STT** (Web Speech API, `es-CL`) → FastAPI →
   agentes → **TTS** lee la respuesta. Etapas B (avatar 2D) y C (lip-sync) quedan consignadas.

## Arquitectura

```
[web chat / voz]  --login-->  BFF (:8797)  --X-API-Key-->  FastAPI (:8796)  -->  Coordinador
                                                                                     |
                                       (solo 127.0.0.1)  langgraph dev (:2025) --> 8 agentes locales
```

- **8 agentes locales** renombrados `agente_<funcionalidad>`: machinelearning, mlbioinformatica,
  bioinformatica, reiki, cocinachilena, **meteorologia** (clima REAL de Chile vía Open-Meteo + SQLite),
  viajes y **administrador** (recepción: conoce y deriva al resto).
- **Memoria** SQLite: historial, destinatarios (allowlist), despachos y accesos.
- **Monitor** (:8798): accesos al gateway (200/401), despachos, allowlist e historial.
- **RAG** de Reiki: local (`RAG_BACKEND=local`), conmutable a **Redis cloud** cuando se configure.

## Requisitos

- Python **3.13** y **`uv`**.
- Un `.env` (ver `.env.example`): `GOOGLE_API_KEY` (Gemini), `API_KEY` (gateway), `WEB_USER/WEB_PASS`,
  `A2A_BASE=http://127.0.0.1:2025`, `A2A_GRAFOS_LOCALES` (los 8 grafos), y opcional `SMTP_*`, `REDIS_URL`.

## Instalar y levantar (LOCAL)

```bash
uv sync
cp .env.example .env      # completar GOOGLE_API_KEY, API_KEY, WEB_USER/WEB_PASS…

# 1) agentes (A2A nativo)
uv run langgraph dev --no-browser --host 127.0.0.1 --port 2025
# 2) gateway FastAPI
uv run uvicorn src.api.app:app --host 127.0.0.1 --port 8796
# 3) frontend web (chat + /voz)
uv run python src/canales/web.py
# 4) monitor (opcional)
uv run python src/canales/monitor.py
```

En servidor, usar los servicios systemd `t2c2-*` y la publicación con proxy: ver
[`deploy/README-T2.md`](deploy/README-T2.md).

## Probar

```bash
# acceso al gateway (evidencia de seguridad)
curl -s http://127.0.0.1:8796/salud                                              # {"estado":"ok"}
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8796/agentes           # 401 (sin API_KEY)
curl -s -o /dev/null -w "%{http_code}\n" -H "X-API-Key: <API_KEY>" http://127.0.0.1:8796/agentes  # 200

# una consulta integrada (requiere los agentes y GOOGLE_API_KEY)
curl -s -X POST http://127.0.0.1:8796/consulta -H "X-API-Key: <API_KEY>" \
     -H "Content-Type: application/json" -d "{\"pregunta\": \"clima hoy en Valdivia\"}"

# pruebas automáticas sin secretos ni red
uv run --with pytest pytest tests/test_tarea2.py -q
```

El chat está en `http://127.0.0.1:8797/` y la voz en `http://127.0.0.1:8797/voz` (Chrome/Edge, con
permiso de micrófono).

## Detener

Corta cada proceso (Ctrl-C) o, con systemd: `sudo systemctl stop t2c2-web t2c2-api t2c2-fichas t2c2-langgraph`.

## Seguridad

- `API_KEY` valida **en el servidor** cada llamada que invoca agentes; el **navegador nunca la ve**
  (BFF). Los agentes escuchan **solo en 127.0.0.1**; el único acceso es por FastAPI.
- Correo **solo a la allowlist**, nunca auto-envío. Guardrails del coordinador (entrada/salida,
  respuesta = dato, no instrucción).
- **Secretos fuera del repo**: `.env`, `*.sqlite`, `logs/` y credenciales están en `.gitignore`.

## Límites

- Requiere internet para Gemini, Open-Meteo y (si se usa) Redis cloud.
- El dictado por voz (STT) funciona principalmente en **Chrome/Edge**; hay fallback a teclado.
- Open-Meteo *archive* (observados) tiene unos días de desfase.
