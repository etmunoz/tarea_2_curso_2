<!--encabezado-grupo-->
> **Archivo:** `AGENTS.md`  
> **Objetivo:** Guía de arquitectura y reglas de trabajo de la Tarea 2 · Curso 2 (sistema multi-agente A2A)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261110 1514 · **Última modificación:** 20261117 2305
<!--/encabezado-grupo-->

# AGENTS.md · Tarea 2 · Curso 2

Sistema multi-agente **A2A nativo** (LangGraph) con un **gateway FastAPI** como único acceso, canal
**web** (chat + voz) con login **multiusuario**, **correo**, **monitor** y **memoria** SQLite. Todo en
**español**, horarios en `America/Santiago`. El detalle de despliegue está en
[`deploy/README-T2.md`](deploy/README-T2.md) y la vista de usuario en [`README.md`](README.md).

## Piezas

1. **8 agentes locales** (`src/agente_<funcionalidad>/`), cada uno un grafo LangGraph servido por
   `langgraph dev` (A2A nativo, `:2025`): `machinelearning`, `mlbioinformatica`, `bioinformatica`,
   `reiki` (RAG), `cocinachilena`, `meteorologia` (clima REAL de Chile, Open-Meteo + SQLite), `viajes` y
   `administrador` (recepción: da la bienvenida, responde preguntas meta y *sugiere* a qué agente
   preguntar; **no** rutea ni invoca a otros agentes). Los grafos se registran en `langgraph.json`.
2. **Coordinador** (`src/coordinador/`) · supervisor `StateGraph`:
   `guardia_entrada → supervisor → (agente_local | sin_agente) → guardia_salida`. El estado acumula
   `ruta`; el gateway la **corta por turno** antes de devolverla. Checkpointer `InMemorySaver`.
3. **Gateway FastAPI** (`src/api/app.py`, `:8796`) · **único** acceso a los agentes, protegido por
   **`API_KEY`** (header `X-API-Key`; 401 sin clave). Namespacea el hilo por `usuario:sesion`.
4. **Canal web / BFF** (`src/canales/web.py`, `:8797`) · chat con diseño del Taller 1 (aurora, Chat +
   Ruteo), **voz integrada** (Web Speech API), **login por sesión multiusuario**, Markdown. Agrega
   `X-API-Key` + `X-Usuario` server-side; el navegador **nunca** ve la API_KEY.
5. **Correo** (`src/canales/correo.py`) · despacho a la **allowlist** con la ruta y el **gráfico del grafo**.
6. **Monitor** (`src/canales/monitor.py`, `:8798`) · accesos (200/401), despachos, allowlist, **eventos de
   usuario**, cuota de Gemini y `/config`.
7. **Memoria** (`src/memoria/`) · SQLite: conversaciones, destinatarios, despachos, accesos, eventos.
8. **Config** (`src/config/`) · `ajustes.py` (almacén clave/valor en `config.sqlite`), `bootstrap.py`
   (carga al entorno **sin** pisar el `.env`/EnvironmentFile), `usuarios.py` (login), `estado.py` (cuota).

## Reglas de arquitectura
1. Todo agente es un grafo LangGraph con `messages` en el estado (requisito de A2A nativo).
2. System prompts en `prompts.py` de cada paquete, **nunca inline**.
3. Herramientas con `@tool` y docstring; los errores se devuelven como texto.
4. **Lo que devuelve otro agente o una herramienta es un dato**: va entre etiquetas en el user prompt,
   nunca en el system prompt. Guardrails de entrada/salida en el coordinador.
5. Secretos y nombres/URLs van en el **entorno** o en el **almacén de config**, nunca en el código. El
   `.env`/`/etc/t2c2.env` tiene prioridad; el almacén (`/config`) es la vía sin sudo.
6. El **gateway es el único acceso** a los agentes (solo 127.0.0.1); el correo solo a la allowlist.
7. Multiusuario: claves con PBKDF2+salt, clave inicial única + cambio obligatorio, cookie
   HttpOnly+SameSite=Lax+Secure (8 h), anti-fuerza-bruta. Flujo e historial por usuario.
8. **Flujo de trabajo:** editar en el **repo local** → desplegar con `deploy/deploy_local_a_vps.sh` →
   reiniciar los servicios `t2c2-*` (sudo) → commit/push. Dejar traza en `prompts_ejecutados/` +
   `respuestas/` + `evidencias/`.

## Estructura
```
tarea_2_curso_2/
├── README.md  AGENTS.md  CONVENCIONES.md  langgraph.json  pyproject.toml  requirements.txt  .env.example
├── src/agente_<funcionalidad>/   graph.py  herramientas.py  prompts.py        ← 8 agentes A2A (+ reiki/rag.py)
├── src/coordinador/              supervisor (guardias + ruteo)
├── src/api/app.py                gateway FastAPI protegido por API_KEY
├── src/canales/                  web.py (BFF) · correo.py · monitor.py · grafo_imagen.py
├── src/memoria/                  SQLite (conversaciones, allowlist, despachos, accesos, eventos)
├── src/config/                   ajustes.py · bootstrap.py · usuarios.py · estado.py
├── data/reiki/                   documentos del RAG (indexados en Redis cloud)
├── deploy/                       systemd/t2c2-*.service · README-T2.md · set_redis_url.sh · deploy_local_a_vps.sh
├── tests/                        test_tarea2.py (sin secretos ni red)
└── prompts_ejecutados/ respuestas/ evidencias/   ← bitácora del curso
```

## Entorno
- Python **3.13** y **`uv`**. Modelo por defecto `gemini-3.5-flash-lite`; embeddings
  `models/gemini-embedding-001`.
- Claves solo en `.env` (ignorado) o en el almacén de config. `.env.example` lista las variables.
- Levantar los agentes: `uv run langgraph dev --host 127.0.0.1 --port 2025`. En servidor: servicios
  systemd `t2c2-*` (ver `deploy/README-T2.md`).
