<!--encabezado-grupo-->
> **Archivo:** `docs/ARQUITECTURA.md`  
> **Objetivo:** Diagrama arquitectónico técnico de la app (vivo) + protocolo de mantención  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1300 · **Última modificación:** 20261118 1325
<!--/encabezado-grupo-->

# Arquitectura técnica — Tarea 2 · Curso 2

Documento **vivo**: refleja la complejidad actual del sistema y se actualiza con cada evolución.
Última revisión de arquitectura: **registro 063** — integración del agente **meteo_mcp** (MCP de
Meteosource, PR #1 de Gustavo) con el patrón **"Clima resiliente en dos niveles"**: meteo_mcp es el
clima **mundial** por defecto con **respaldo keyless Open-Meteo**; `agente_meteorologia` queda para
**verificación** (pronóstico vs observado) y Chile; `agente_viajes` **deja el clima** y lo deriva a
meteo_mcp. (Hitos previos: agentes reales 028–032; seguridad 034–035 y guardia anti-ofuscación 043;
memoria durable 036; recepción personalizada 037–039.) Backlog en
[`MEJORAS_FUTURAS.md`](MEJORAS_FUTURAS.md). Decisiones:
[`decisiones/ADR-0001-memoria-corto-plazo.md`](decisiones/ADR-0001-memoria-corto-plazo.md).

---

## Prompt de mantención (para Claude)

> **Mantén este diagrama al día.** Cada vez que una tarea agregue, quite o cambie un agente, una
> herramienta con efecto externo, un servicio systemd, una fuente de datos (API/BD) o un flujo entre
> componentes, **actualiza `docs/ARQUITECTURA.md` en el MISMO cambio**: el diagrama Mermaid, la tabla de
> componentes, la lista de fuentes externas y la línea "Última revisión". Regla de fidelidad: el
> diagrama describe lo que está en el código (`src/…`, `deploy/systemd/…`, `langgraph.json`,
> `src/fichas.py`), no lo aspiracional. Valida la sintaxis Mermaid (sin `end` como id de nodo;
> `subgraph`/`end` balanceados) antes de commitear. Mantén los IDs de nodo estables para que el diff sea
> legible. Deja traza en `prompts_ejecutados/` + `respuestas/` como el resto de los cambios.

---

## Diagrama (componentes, flujos y fuentes de datos)

```mermaid
flowchart TB
    subgraph CL["Navegador (usuarios)"]
      CHAT["Chat + Voz · login por sesion"]
      MON["Monitor / backoffice"]
    end

    subgraph EDGE["Publicacion · ISPConfig proxy + HTTPS (Let's Encrypt)"]
      P1["tarea2curso2.etmk.cl"]
      P2["monitortarea2curso2.etmk.cl"]
    end

    CHAT --> P1
    MON --> P2

    subgraph APP["VPS web6 · servicios systemd · solo 127.0.0.1"]
      BFF["t2c2-web · BFF (:8797)<br/>sesion PBKDF2+cookie, agrega X-API-Key y X-Usuario"]
      MONI["t2c2-monitor (:8798)<br/>accesos 200/401, eventos, cuota Gemini, /config"]
      API["t2c2-api · FastAPI (:8796)<br/>API_KEY · unico acceso a los agentes"]
      FICHAS["t2c2-fichas · vigilante de agent cards"]
      subgraph COORD["Coordinador · supervisor (StateGraph)"]
        GE2["guardia_entrada"] --> SUP2["enrutar (supervisor)"]
        SUP2 --> CONS["consultar | sin_agente"] --> GS2["guardia_salida"]
      end
       subgraph LG["t2c2-langgraph · A2A nativo (:2025) · 9 agentes"]
        A1["meteorologia · clima REAL"]
        A2["reiki · RAG + terapias"]
        A3["bioinformatica · UniProt"]
        A4["mlbioinformatica · pipelines"]
        A5["machinelearning · tecnica/metricas/modelo"]
        A6["cocinachilena · recetas/costeo/nutricion"]
         A7["viajes · destino real + demo"]
         A8["administrador · recepcion"]
         A9["meteo_mcp · Meteosource MCP"]
      end
    end

    P1 --> BFF
    P2 --> MONI
    BFF --> API
    API --> COORD
    CONS -->|A2A| LG

    subgraph DATA["Persistencia (SQLite + Redis)"]
      MEM["Memoria SQLite<br/>conversaciones, destinatarios, despachos, accesos, eventos, perfiles"]
      CFG["Config store SQLite<br/>GOOGLE_API_KEY, API_KEY, SMTP_PASS, REDIS_URL, REDIS_INDEX"]
      REC["Recetas / Clima SQLite"]
      USR["Usuarios SQLite<br/>login multiusuario (PBKDF2)"]
    end

    subgraph EXT["Servicios externos"]
      GEM["Gemini<br/>LLM + embeddings"]
      RED["Redis cloud<br/>RediSearch (RAG Reiki)"]
      OM["Open-Meteo<br/>geocoding / forecast / archive"]
      UP["UniProt REST"]
      FXR["open.er-api.com<br/>tipo de cambio"]
      WK["Wikipedia REST"]
      SMTP["SMTP etmk.cl"]
      MCP["MCP Meteosource<br/>Streamable HTTP · Bearer"]
    end

    SUP2 -->|decide agente| GEM
    A2 --> GEM
    A2 --> RED
    A1 --> OM
    A1 --> REC
    A3 --> UP
    A4 --> GEM
    A5 --> GEM
    A6 --> REC
    A7 --> OM
    A7 --> FXR
    A7 --> WK
    BFF --> USR
    API --> MEM
    API --> CFG
    MONI --> MEM
    MONI --> CFG
    API -->|despacho correo| SMTP
    A9 -.herramientas MCP.-> MCP
    A9 -.respaldo si MCP cae.-> OM
    FICHAS -.re-aplica cards.-> LG
```

> Convención del diagrama: líneas sólidas = flujo de petición/datos; línea punteada = proceso de
> soporte. "REAL" marca datos en vivo de una API pública; "demo" marca datos de ejemplo.

---

## Flujo interno de `meteo_mcp`

```mermaid
flowchart LR
    MSTART([mensaje]) --> GDE[guardia_de_entrada<br/>Veredicto estructurado]
    GDE -->|permitido| MAG[agente<br/>Gemini + tools]
    GDE -->|no permitido| BLOQ[respuesta_bloqueada<br/>respuesta fija]
    MAG --> TOOLS[search_places<br/>get_forecast<br/>get_weather_history]
    TOOLS -->|primario| MCP[Meteosource MCP<br/>Streamable HTTP]
    MAG -.respaldo si MCP cae.-> RESP[pronostico_respaldo<br/>Open-Meteo keyless]
```

La guardia clasifica antes de ejecutar el agente meteorológico. Los mensajes fuera de alcance,
inyecciones, datos personales y acciones no soportadas reciben una respuesta fija sin usar las
tools meteorológicas.

---

## Componentes (código fuente)

| Componente | Servicio | Puerto | Código | Rol |
|---|---|---|---|---|
| Chat + Voz (BFF) | `t2c2-web` | 8797 | `src/canales/web.py` | Login por sesión, proxy server-side con `X-API-Key`/`X-Usuario` |
| Monitor | `t2c2-monitor` | 8798 | `src/canales/monitor.py` | Accesos, eventos, cuota Gemini, `/config` |
| Gateway | `t2c2-api` | 8796 | `src/api/app.py` | FastAPI protegido por `API_KEY`; único acceso a agentes |
| Coordinador | (en gateway) | — | `src/coordinador/` | Supervisor: guardias + ruteo por turno |
| Agentes A2A | `t2c2-langgraph` | 2025 | `src/agente_*/`, `src/agente_meteo_mcp/` | 9 grafos LangGraph (A2A nativo) |
| Vigilante fichas | `t2c2-fichas` | — | `tools/configurar_fichas.py` | Re-aplica las agent cards de `src/fichas.py` |
| Memoria | — | — | `src/memoria/` | SQLite (conversaciones, allowlist, accesos, eventos) |
| Config / Usuarios | — | — | `src/config/` | `ajustes.py`, `bootstrap.py`, `usuarios.py`, `estado.py` |
| Adaptador MCP | — | externo | `src/integraciones/mcp_langchain.py` | Cliente MCP 2.3 asíncrono y conversión a `StructuredTool` |

## Agentes y sus fuentes de datos

| Agente | Fuente | Tipo |
|---|---|---|
| meteorologia | Open-Meteo + SQLite | **real** |
| reiki | RAG (Redis/RediSearch) + Gemini embeddings | **real** |
| bioinformatica | UniProt REST | **real** |
| mlbioinformatica | catálogos bio-ML + pipelines | referencia |
| machinelearning | catálogos ML/DS + SQLite | referencia |
| cocinachilena | recetas/costeo/nutrición (SQLite + reglas) | referencia |
| viajes | geocoding + cambio + Wikipedia (real); vuelos/hoteles (demo). El clima lo deriva a meteo_mcp | **real** + demo |
| administrador | fichas del resto de agentes | interno |
| meteo_mcp | **clima mundial** por Meteosource MCP (`search_places`/`get_forecast`/`get_weather_history`); **respaldo keyless Open-Meteo** si el MCP cae | **real** |

## Fuentes externas (sin API key salvo Gemini)

- **Gemini** (`GOOGLE_API_KEY`): LLM del supervisor y agentes + embeddings del RAG.
- **Redis cloud** (`REDIS_URL`): índice RediSearch `t2c2_duran_reyes_munoz_reiki`.
- **Open-Meteo**: geocoding, pronóstico y archivo (clima real; sin key).
- **UniProt REST**: proteínas/genes (sin key).
- **open.er-api.com**: tipo de cambio con CLP (sin key).
- **Wikipedia REST**: resúmenes de destinos (sin key).
- **SMTP** (`tarea2curso2@etmk.cl`): despacho de correo (allowlist).
- **MCP Meteosource** (`MCP_SERVER_METEOSOURCE`): herramientas meteorológicas por Streamable HTTP; autentificación Bearer mediante `MCP_BEARER_TOKEN_ENV_VAR` (token directo o nombre de variable).

## Seguridad (resumen)

- Gateway con `API_KEY` (único acceso a agentes); agentes y gateway solo en `127.0.0.1`.
- BFF con login multiusuario (PBKDF2 + cookie `HttpOnly+SameSite=Lax+Secure`, anti-fuerza-bruta).
- Guardrails de entrada/salida en el coordinador; la respuesta de un agente es **dato**, no instrucción.
- Secretos fuera del repo (`.env`/`/etc/t2c2.env` o el config store); correo solo a la allowlist.
- El token Bearer MCP se resuelve desde `MCP_BEARER_TOKEN_ENV_VAR` y nunca se registra.
- `meteo_mcp` filtra el mensaje con `guardia_de_entrada` antes de ejecutar sus herramientas; los
  bloqueos no invocan el agente meteorológico ni las tools.

## Despliegue

`local (repo) → deploy/deploy_local_a_vps.sh (rsync) → VPS web6 → reinicio de servicios t2c2-* → commit/push`.
Detalle en [`deploy/README-T2.md`](../deploy/README-T2.md).
