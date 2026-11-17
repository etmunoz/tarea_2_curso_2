<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_001.md`  
> **Objetivo:** 001 · Respuesta — CONVENCIONES.md creado y evaluación de recursos de la VPS (solo lectura)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1438 · **Última modificación:** 20261117 1438
<!--/encabezado-grupo-->

# 001 · Respuesta — CONVENCIONES.md + evaluación de la VPS

**Prompt:** [`../prompts_ejecutados/prompt_001.md`](../prompts_ejecutados/prompt_001.md)

**Fecha/hora:** 20261117 1438 (`America/Santiago`).

---

## 1. `CONVENCIONES.md` creado

Se creó [`../CONVENCIONES.md`](../CONVENCIONES.md) (adaptado del T1) con: encabezado de archivos (hash y
markdown), **registro de prompts** con naming `prompt_NNN`/`salida_NNN` **desde `000`**, commits en
español + push por paso, e idioma/zona horaria/formato. Commit aparte, pusheado a `main`.

---

## 2. Evaluación de la VPS — `server28.etmk.cl` (IP 69.197.134.192)

Acceso **SSH por clave** como `etmkuseragente@etmk.cl` (Shell-User web1), **un solo** comando de
**solo lectura** (con `BatchMode`, sin reintentos, para no gatillar fail2ban). **No se creó ni modificó
nada.**

### 2.1 Recursos

| Recurso | Valor | Lectura |
|---|---|---|
| **SO** | Ubuntu 24.04.5 LTS | — |
| **CPU** | 2 cores · load 0.06 / 0.10 / 0.20 | ✅ ocioso |
| **Disco `/`** | 63 GB · **54 GB libres** (12% uso) | ✅ de sobra |
| **RAM** | 3.8 GB total · 2.7 GB usada · **1.1 GB disponible** | ⚠️ ajustado |
| **Swap** | **0 B** | ⚠️ sin colchón anti-OOM |

### 2.2 Mayores consumidores de RAM (RSS)

| Proceso | RAM | Nota |
|---|---:|---|
| **`clamd` (ClamAV)** | **966 MB** | 🔴 el mayor consumidor, con diferencia |
| `coordinador_web.py` (T1) | 190 MB | frontend chat T1 |
| fork RAG (InMemoryVectorStore) | 166 MB | hijo del coordinador_web |
| `mariadbd` | 132 MB | base de datos |
| vigilante de fichas (T1) | 114 MB | re-aplica agent cards |
| `langgraph dev` (7 grafos, T1) | 93 MB | A2A nativo :2024 |
| `lucecita-memory` | 86 MB | proyecto personal (ajeno al curso) |
| rspamd (×5) | ~340 MB | filtro de correo |
| fail2ban | 63 MB | seguridad |

Stack de agentes del **T1** ≈ **550 MB**. **Sin eventos OOM** registrados.

### 2.3 Puertos en escucha (relevantes)

- **Usados por apps:** `2024` (langgraph T1), `8790` (puente), `8793` (monitor), `8794` (coordinador),
  `8795` (lucecitaOS), `8080`/`8081` (ISPConfig).
- **Infra:** `6379` (redis **local**, no lo usaremos → va Redis cloud), `3306` (MariaDB),
  `11211` (memcached), `11332-11334` (rspamd), `25/465/587/110/143/993/995/4190` (correo), `53` (DNS),
  `443/80` (Apache), `22` (SSH).

### 2.4 Servicios activos

5 del T1 (`agente-coordinador`, `agente-fichas`, `agente-langgraph`, `agente-monitor`, `agente-puente`)
\+ `apache2` + `lucecitaos` + `mariadb` + `redis-server`.

---

## 3. Veredicto: **sí cabe, pero la RAM es el cuello de botella**

- **Disco y CPU:** holgados (54 GB libres, 2 cores ociosos).
- **RAM:** **1.1 GB disponible, sin swap.** El stack T2 estimado
  (`t2c2-langgraph` 8 grafos + FastAPI + web BFF + monitor + vigilante) suma **~500–650 MB**. Entra
  **justo** y con riesgo de OOM en picos. Como **Redis es cloud**, **no** sumamos Redis local (bien).

### Recomendaciones antes de desplegar (requieren `sudo` → las ejecuta el usuario)

| # | Acción | Gana | Requiere |
|---|---|---|---|
| 1 | **Añadir swap** (swapfile 2–4 GB; hay 54 GB libres) | colchón anti-OOM | `sudo` |
| 2 | **Revisar `clamd` (966 MB)**: si el escaneo *on-access* no es imprescindible, limitarlo o pasarlo a escaneo **programado** | **~1 GB** | `sudo` |
| 3 | T2 *lean*: 1 solo `langgraph` con los 8 grafos; FastAPI + web acotados; RAG → Redis cloud (sin fork InMemory) | ~150–250 MB | — |

### Puertos nuevos propuestos (todos libres)

| Servicio | Puerto |
|---|---|
| `t2c2-langgraph` | **2025** |
| `t2c2-api` (FastAPI) | **8796** |
| `t2c2-web` (frontend BFF) | **8797** |
| `t2c2-monitor` | **8798** |

---

## 4. Estado y pendientes

- ✅ `CONVENCIONES.md` creado y pusheado.
- ✅ VPS evaluada (solo lectura). **No se tocó/creó/desplegó nada.**
- ⏸️ **Pendiente del usuario/grupo:** decidir sobre swap y `clamd` (acciones con `sudo`), y dar el OK
  para empezar a desplegar T2. También siguen pendientes: **URL del Redis cloud**, **`API_KEY`** y
  (solo si se hace la Etapa C) credenciales del avatar.
- ➡️ **Próximo paso al OK:** registro 002 — crear la estructura del repo (§11 del `prompt_000.md`) con
  los agentes renombrados y locales; aún sin tocar la VPS.
