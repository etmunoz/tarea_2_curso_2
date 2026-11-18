<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_025.md`  
> **Objetivo:** 025 · Respuesta — documentación de arquitectura actualizada (README, README-T2, AGENTS)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2305 · **Última modificación:** 20261117 2305
<!--/encabezado-grupo-->

# 025 · Respuesta — Docs de arquitectura al día

**Prompt:** [`../prompts_ejecutados/prompt_025.md`](../prompts_ejecutados/prompt_025.md)

---

## 1. Qué se actualizó

| Doc | Antes (desactualizado) | Ahora (correcto) |
|---|---|---|
| `README.md` | RAG «local, conmutable»; `WEB_USER/WEB_PASS`; sin multiusuario ni almacén | RAG **en Redis cloud**; multiusuario (sesión/PBKDF2/cookie/anti-BF); almacén de config; monitor con eventos/cuota/`/config`; coordinador supervisor + ruteo por turno |
| `deploy/README-T2.md` | monitor «pendiente»; `WEB_USER/WEB_PASS`; `chown root:web6`; «Basic Auth» | monitor **activo**; `WEB_USUARIOS/WEB_ADMIN/CLAVE_INICIAL`; `chown root:client1`; login **por sesión**; alternativa por almacén de config |
| `AGENTS.md` | heredado del Taller 1 (`agente-viajes-a2a`, `consumidor`, `swarm`, OpenCode) | arquitectura, estructura y reglas **reales de T2** (8 agentes, gateway, coordinador, canales, memoria, config) |

## 2. Detalle correcto consolidado (estado real)

- **Agentes:** 8 locales (`langgraph.json`) + coordinador supervisor
  (`guardia_entrada → supervisor → agente_local → guardia_salida`), ruteo por turno.
- **Acceso:** gateway FastAPI `:8796` protegido por `API_KEY` (único acceso; agentes solo en 127.0.0.1).
- **Web `:8797`:** BFF con login **multiusuario** por sesión, voz integrada, Markdown.
- **RAG de Reiki:** **Redis cloud** (RediSearch), índice `t2c2_duran_reyes_munoz_reiki`.
- **Config:** almacén `config.sqlite` (`/config` del monitor, `set_redis_url.sh`); `.env`/`/etc` prioriza.
- **Monitor `:8798`:** accesos, despachos, allowlist, eventos de usuario, cuota Gemini, `/config`.

## 3. Estado

- ✅ `README.md`, `deploy/README-T2.md`, `AGENTS.md` al día. Solo documentación (sin tocar código).
- ✅ Desplegado a la VPS y commiteado/pusheado. Bitácora **000–025**.
