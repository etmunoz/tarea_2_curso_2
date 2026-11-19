<!--encabezado-grupo-->
> **Archivo:** `docs/ARQUITECTURA.md`  
> **Objetivo:** Diagrama arquitectónico técnico de la app (vivo) + protocolo de mantención  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1300 · **Última modificación:** 20261118 1325
<!--/encabezado-grupo-->

# Arquitectura técnica — Tarea 2 · Curso 2

Documento **vivo**: refleja la complejidad actual del sistema y se actualiza con cada evolución.
Última revisión de arquitectura: **registro 035** (agentes mejorados 028–032: bioinformática/UniProt,
ML-bio/pipelines, cocina, fichas, viajes real; + endurecimiento de seguridad/robustez 034–035: merge de
los fallos 1/3/5/6 de Fabio y resolución de 2 (guardia anti-leetspeak/inglés), 4 (contexto de
seguimiento) y 7 (lugares ficticios)). Backlog en [`MEJORAS_FUTURAS.md`](MEJORAS_FUTURAS.md).

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
      subgraph LG["t2c2-langgraph · A2A nativo (:2025) · 8 agentes"]
        A1["meteorologia · clima REAL"]
        A2["reiki · RAG + terapias"]
        A3["bioinformatica · UniProt"]
        A4["mlbioinformatica · pipelines"]
        A5["machinelearning · tecnica/metricas/modelo"]
        A6["cocinachilena · recetas/costeo/nutricion"]
        A7["viajes · destino real + demo"]
        A8["administrador · recepcion"]
      end
    end

    P1 --> BFF
    P2 --> MONI
    BFF --> API
    API --> COORD
    CONS -->|A2A| LG

    subgraph DATA["Persistencia (SQLite + Redis)"]
      MEM["Memoria SQLite<br/>conversaciones, destinatarios, despachos, accesos, eventos"]
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
    FICHAS -.re-aplica cards.-> LG
```

> Convención del diagrama: líneas sólidas = flujo de petición/datos; línea punteada = proceso de
> soporte. "REAL" marca datos en vivo de una API pública; "demo" marca datos de ejemplo.

---

## Componentes (código fuente)

| Componente | Servicio | Puerto | Código | Rol |
|---|---|---|---|---|
| Chat + Voz (BFF) | `t2c2-web` | 8797 | `src/canales/web.py` | Login por sesión, proxy server-side con `X-API-Key`/`X-Usuario` |
| Monitor | `t2c2-monitor` | 8798 | `src/canales/monitor.py` | Accesos, eventos, cuota Gemini, `/config` |
| Gateway | `t2c2-api` | 8796 | `src/api/app.py` | FastAPI protegido por `API_KEY`; único acceso a agentes |
| Coordinador | (en gateway) | — | `src/coordinador/` | Supervisor: guardias + ruteo por turno |
| Agentes A2A | `t2c2-langgraph` | 2025 | `src/agente_*/` | 8 grafos LangGraph (A2A nativo) |
| Vigilante fichas | `t2c2-fichas` | — | `tools/configurar_fichas.py` | Re-aplica las agent cards de `src/fichas.py` |
| Memoria | — | — | `src/memoria/` | SQLite (conversaciones, allowlist, accesos, eventos) |
| Config / Usuarios | — | — | `src/config/` | `ajustes.py`, `bootstrap.py`, `usuarios.py`, `estado.py` |

## Agentes y sus fuentes de datos

| Agente | Fuente | Tipo |
|---|---|---|
| meteorologia | Open-Meteo + SQLite | **real** |
| reiki | RAG (Redis/RediSearch) + Gemini embeddings | **real** |
| bioinformatica | UniProt REST | **real** |
| mlbioinformatica | catálogos bio-ML + pipelines | referencia |
| machinelearning | catálogos ML/DS + SQLite | referencia |
| cocinachilena | recetas/costeo/nutrición (SQLite + reglas) | referencia |
| viajes | geocoding + cambio + clima + Wikipedia (real); vuelos/hoteles (demo) | **real** + demo |
| administrador | fichas del resto de agentes | interno |

## Fuentes externas (sin API key salvo Gemini)

- **Gemini** (`GOOGLE_API_KEY`): LLM del supervisor y agentes + embeddings del RAG.
- **Redis cloud** (`REDIS_URL`): índice RediSearch `t2c2_duran_reyes_munoz_reiki`.
- **Open-Meteo**: geocoding, pronóstico y archivo (clima real; sin key).
- **UniProt REST**: proteínas/genes (sin key).
- **open.er-api.com**: tipo de cambio con CLP (sin key).
- **Wikipedia REST**: resúmenes de destinos (sin key).
- **SMTP** (`tarea2curso2@etmk.cl`): despacho de correo (allowlist).

## Seguridad (resumen)

- Gateway con `API_KEY` (único acceso a agentes); agentes y gateway solo en `127.0.0.1`.
- BFF con login multiusuario (PBKDF2 + cookie `HttpOnly+SameSite=Lax+Secure`, anti-fuerza-bruta).
- Guardrails de entrada/salida en el coordinador; la respuesta de un agente es **dato**, no instrucción.
- Secretos fuera del repo (`.env`/`/etc/t2c2.env` o el config store); correo solo a la allowlist.

## Despliegue

`local (repo) → deploy/deploy_local_a_vps.sh (rsync) → VPS web6 → reinicio de servicios t2c2-* → commit/push`.
Detalle en [`deploy/README-T2.md`](../deploy/README-T2.md).
