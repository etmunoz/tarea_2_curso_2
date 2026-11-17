<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_000.md`  
> **Objetivo:** 000 · Respuesta — construcción, verificación y estado del prompt inicial de arranque de la Tarea 2  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1430 · **Última modificación:** 20261117 1430
<!--/encabezado-grupo-->

# 000 · Respuesta — Prompt inicial de arranque de la Tarea 2

**Prompt:** [`../prompts_ejecutados/prompt_000.md`](../prompts_ejecutados/prompt_000.md)
· **PDF:** [`../prompts_ejecutados/prompt_000.pdf`](../prompts_ejecutados/prompt_000.pdf)

**Zona horaria de referencia:** `America/Santiago`. **Idioma:** español (Chile).

---

## 1. Qué es este registro (000)

El registro `000` **no implementa código de la Tarea 2 todavía**: documenta la **construcción, depuración
y verificación del prompt inicial de arranque** (`prompt_000.md`), que es la **fuente de verdad** del
encargo, de la arquitectura heredada del Taller 1 y de **todas las decisiones ya resueltas**. La
implementación de la Tarea 2 (evaluar la VPS, crear el repo con los agentes renombrados, el gateway
FastAPI, las 3 implementaciones, SQLite y el enchufe de Redis cloud) arranca en los registros
siguientes, **a partir del OK del grupo**.

> **Estado:** ⏸️ **En pausa a la espera del feedback del grupo** (Fabio Durán · Gustavo Reyes · Ezequiel
> Muñoz). No se ha tocado la VPS ni se ha desplegado nada, conforme a la restricción dura del prompt
> («No crees nada en la VPS ni despliegues: espero tu plan para validarlo»).

---

## 2. Decisiones resueltas y consignadas en el prompt

Todas quedaron escritas y estructuradas en `prompt_000.md`:

| # | Tema | Decisión |
|---|---|---|
| 1 | **Alcance** | Aspirar a las **3 implementaciones** (puntaje 3 > 2 > 1), con **prioridad en la avanzada (3)**. Entrega **LOCAL y reproducible**; nube = +1 opcional. |
| 2 | **Arquitectura central** | **FastAPI es el ÚNICO gateway** a los agentes. Frontend/canal ↔ FastAPI ↔ coordinador ↔ agentes. Sin llamadas directas al agente. |
| 3 | **Seguridad del gateway** | Endpoints que invocan agentes exigen **`API_KEY`** (definida por el usuario en `.env`), validada en servidor → sin ella **401**. Agentes en **`127.0.0.1`**, no publicados. Web = **BFF** (la API_KEY nunca llega al browser). |
| 4 | **Agentes LOCALES** | En T2 **todos los agentes se copian y corren locales** (sin túneles de compañeros). App full operativa y autocontenida. El fallback remoto→local del T1 deja de ser necesario; ruteo/guardrails se conservan. |
| 5 | **Renombre** | Todos a **`agente_<funcionalidad>`**, con la funcionalidad **extraída de sus tools/fichas reales** (ver mapa en §4 de esta salida). |
| 6 | **8º agente** | **`agente_administrador`** (NUEVO): conoce las habilidades de todos los demás (lee fichas/catálogo), orienta y deriva amablemente en español. Atiende lo meta que antes caía en «ninguno». |
| 7 | **Dominios nuevos** | App: **`tarea2curso2.etmk.cl`** · Monitor: **`monitortarea2curso2.etmk.cl`** (distintos del T1). Agentes sin subdominio. |
| 8 | **Correo** | Despacho desde **`tarea2curso2@etmk.cl`** (SMTP 587 + STARTTLS), solo a **destinatarios registrados**; nunca auto-envío; disparo solo por el usuario. |
| 9 | **Formato del correo** | Cuerpo **HTML bien formateado** + texto plano; al pie: **(1) la RUTA de los agentes** y **(2) el gráfico del grafo de LangGraph** embebido (PNG `draw_mermaid_png()`, fallback Mermaid texto). |
| 10 | **Destinatario autogestionado** | El receptor **se registra en una interfaz de configuración**; allowlist en **SQLite** (evolución del allowlist por env del T1). |
| 11 | **Redis cloud** | Transformar la emulación local (`InMemoryVectorStore`) a **`RedisVectorStore`** sobre **Redis en la nube** (requiere **RediSearch**). URL la entrega el usuario → implementar cuando llegue; backend local queda como fallback de desarrollo. |
| 12 | **Memoria largo plazo** | **SQLite**: historial de conversación, destinatarios, bitácora de despachos, y (de meteorología) pronósticos diarios + observados reales. Job diario alimenta clima. |
| 13 | **Meteorología REAL** | `agente_meteorologia` deja de ser estático → **Open-Meteo** (gratis, sin key) para ciudades de Chile, hoy + 7 días; **guarda pronósticos a diario** y **el observado real** en SQLite para **comparar pronóstico vs real**. |
| 14 | **Idioma y zona horaria** | **Todo en español (Chile)**; **`America/Santiago`** en todo lo visible al usuario (el VPS corre en UTC → convertir al mostrar). |
| 15 | **Presentación** | Salidas **bien formateadas** (Markdown/HTML, títulos, listas, tablas, énfasis, unidades CLP/°C) sin alterar cifras/unidades (fidelidad). |
| 16 | **Integración avanzada (opción 3)** | **YA DECIDIDA: avatar conversacional por VOZ en el sitio, por etapas** — **A** voz (Web Speech API, `es-CL`, STT→FastAPI→TTS; gratis; base obligatoria), **B** avatar 2D (condicional a que A funcione), **C** avatar realista con lip-sync (HeyGen/D-ID/Simli, opcional de pago). |
| 17 | **Monitor repropuesto** | El T1 monitoreaba el **puente A2A** (tráfico de compañeros), inexistente en T2. Se **redefine** como backoffice de operación/seguridad: baneos fail2ban + accesos FastAPI + despachos + historial. El puente A2A **no se porta**. |
| 18 | **lucecitaOS fuera** | Se quitaron **todas** las referencias a lucecitaOS (proyecto personal, ajeno al curso). |
| 19 | **Estructura de paquete** | Cada agente conserva su estructura del T1: `__init__.py`, `graph.py`, `herramientas.py`, `prompts.py` + módulos de datos (`bd_*.py`, `rag.py`, cliente de API). **Nunca un solo `.py` suelto.** |

---

## 3. Verificación de fidelidad arquitectónica (prompt vs código real del T1)

Antes de cerrar el prompt se contrastó **cada afirmación de arquitectura heredada** contra el código de
`tarea_1_curso_2`. Resultado: **todo correcto** salvo dos cosas, ya corregidas (estructura de agentes y
monitor). Detalle:

| Afirmación del prompt | Fuente real en T1 | Estado |
|---|---|---|
| Tools por agente (los 7) | `src/agente_*/herramientas.py` (`@tool`) | ✓ exactas |
| Nodos coordinador `guardia_entrada→enrutar→consultar\|sin_agente→guardia_salida` | `src/coordinador/graph.py:233-243` | ✓ |
| Estado `messages, elegido, motivo, respuesta, origen, bloqueado, ruta` | `Estado(TypedDict)` | ✓ |
| `Decision{agente, motivo}` (salida estructurada) | `graph.py` | ✓ |
| Ruta usa marcador `"supervisor"` para el nodo `enrutar` | `graph.py:141` (`"ruta": ["supervisor"]`) | ✓ (el ejemplo del correo es fiel) |
| A2A: `POST /assistants/search {graph_id}`, card en `/.well-known/agent-card.json?assistant_id=…`, `contextId`=UUID | `src/coordinador/a2a.py:259, 288, uuid4` | ✓ (incluye el `?assistant_id=`) |
| Fichas vía `PATCH /assistants/<id>` + servicio vigilante | `tools/configurar_fichas.py:54,93` | ✓ |
| Modelo `gemini-3.5-flash-lite` (env `MODELO`) | todos los `graph.py` | ✓ |
| Embeddings `models/gemini-embedding-001` | `src/agente_tomas/rag.py:51` | ✓ |
| RAG `RedisVectorStore`/`InMemoryVectorStore`, índice en `logs/reiki_rag.json` | `rag.py` | ✓ |
| Puertos 2024/8790/8793/8794 · 5 servicios `agente-*` | `deploy/systemd/*.service` | ✓ |
| Despliegue Apache + ISPConfig + Let's Encrypt, force-HTTPS antes del proxy, `ExecStartPre` espera langgraph, `langgraph dev --host 127.0.0.1` | `deploy/README.md`, `.service` | ✓ |
| Frontend = `tools/coordinador_web.py` (8794) · backoffice = `tools/monitor_web.py` (8793) | encabezados de los archivos | ✓ |
| Correo heredado (SMTP 587, allowlist) | `tools/coordinador_web.py` (`smtplib`, `EmailMessage`, `COORD_MAIL_*`) | ✓ |

**Correcciones aplicadas durante la construcción:**
1. **Estructura de los agentes** — el prompt mostraba cada agente como una línea de carpeta (parecía «un solo `.py`»). Se expandió a su estructura de paquete real en §11 y se consignó el estándar en §4.
2. **Monitor** — se repropuso para T2 (ya no existe el puente A2A).
3. **Resabios del canal viejo** — se eliminaron menciones a WhatsApp/llamada/Twilio (diagrama §2, §8, §10, §15) que contradecían la decisión del avatar por voz.
4. **lucecitaOS** — eliminado del texto.

---

## 4. Mapa de renombre de agentes (origen T1 → T2)

| T2 (`agente_<funcionalidad>`) | Origen T1 | Herramientas reales |
|---|---|---|
| `agente_machinelearning` | `agente_ezequiel` | `recomendar_tecnica`, `metricas_recomendadas`, `elegir_modelo`, `consultar_modelos` |
| `agente_mlbioinformatica` | `proteinman` | las mismas 4 (datos biológicos) |
| `agente_bioinformatica` | `agente_fabio` | `consultar_mis_apuntes` |
| `agente_reiki` | `agente_tomas` | `principios_reiki`, `posiciones_manos`, `info_simbolo`, `buscar_reiki` (RAG) |
| `agente_cocinachilena` | `agente_cocina` | `listar_recetas`, `ver_receta`, `costear_receta` |
| `agente_meteorologia` | `agente_meteorologo` | `pronostico_hoy`, `pronostico_semana`, `historial_pronostico`, `comparar_pronostico_vs_real` (REAL + SQLite) |
| `agente_viajes` | `agente_viajes` | `buscar_vuelos`, `buscar_hoteles`, `buscar_actividades` |
| `agente_administrador` | **NUEVO** | `listar_agentes`, `describir_agente` |

El T1 registra **7 grafos** en `langgraph.json`; en T2 serán **8** (los 7 renombrados + `agente_administrador`).

---

## 5. Archivos tocados en este registro

| Archivo | Acción |
|---|---|
| `prompts_ejecutados/prompt_000.md` | Prompt inicial (antes `PROMPT_INICIAL_TAREA2.md`), movido con `git mv` + encabezado de grupo + ajustes de consistencia. |
| `prompts_ejecutados/prompt_000.pdf` | PDF del prompt para compartir (regenerado desde el `.md`, xhtml2pdf). |
| `respuestas/salida_000.md` | Esta salida. |
| `.gitignore` | `.env`, `.venv`, `*.sqlite`, `logs/`, `node_modules`, cachés. |

**Repositorio:** `github.com/etmunoz/tarea_2_curso_2` (**privado**). Commits en español, firmados
`Co-Authored-By: Claude Opus 4.8`.

---

## 6. Pendientes del usuario / grupo

- **URL del Redis cloud** (con RediSearch) — por vía privada.
- **`API_KEY`** del gateway — la define el usuario en `.env`.
- **Credenciales del SaaS de avatar** — **solo si** se aborda la **Etapa C** (opcional, de pago); las
  Etapas A/B no requieren credenciales.
- **Feedback del grupo** sobre el prompt antes de arrancar la implementación.

---

## 7. Próximos pasos (al recibir el OK) — §16 del prompt

1. **Evaluar la VPS** (RAM/disco/puertos) → decir si cabe y proponer puertos/servicios nuevos. *(No crear nada.)*
2. **Crear el repo** con la estructura §11: agentes **renombrados** y **locales**, coordinador, guardrails, `langgraph.json`, `fichas.py`, convenciones, `.env.example` (con `API_KEY`), `.gitignore`, encabezados.
3. **Backend FastAPI**: endpoints + dependencia que valida `API_KEY` + wrapper del coordinador.
4. **Plan de las 3 implementaciones**; la avanzada ya decidida → **plan de la Etapa A** (voz), B/C consignadas.
5. **Esquema SQLite** (historial + destinatarios + despachos + clima) y **punto de enchufe del Redis cloud**.
6. **Entregar el plan para validarlo antes de ejecutar.** No desplegar ni tocar la VPS sin OK.
