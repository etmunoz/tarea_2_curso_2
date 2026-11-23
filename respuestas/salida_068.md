<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_068.md`
> **Objetivo:** 068 · Respuesta — seguimiento inteligente (re-ruteo cuando cambia el dominio)
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
> **Creación:** 20261123 1945 · **Última modificación:** 20261123 1945
<!--/encabezado-grupo-->

# 068 · Respuesta — el seguimiento ya no se queda en un agente que no puede responder

**Prompt:** [`../prompts_ejecutados/prompt_068.md`](../prompts_ejecutados/prompt_068.md)

---

## 1. Causa

El coordinador reutilizaba el agente del turno anterior **sin volver a rutear** ante cualquier pregunta
corta que empezara como seguimiento («y en…»). Así, «y en Santiago de Compostela?» se quedaba en
`agente_meteorologia` (solo Chile) → no podía responder y derivaba a Viajes. Dos capas lo forzaban: el
**atajo determinista** en `enrutar` y la **regla del prompt** del supervisor.

## 2. Arreglo

- **`src/coordinador/graph.py::enrutar`** — el agente previo es ahora una **PISTA** en un bloque
  `<pista>` para el supervisor; se eliminó el atajo que saltaba el ruteo. El supervisor decide siempre.
- **`src/coordinador/prompts.py::SYSTEM_SUPERVISOR`** — la regla de seguimiento mantiene el mismo agente
  **por defecto**, pero cambia si el nuevo lugar/entidad/tema corresponde a otro agente; «la continuidad
  nunca debe mandar la pregunta a un agente que no puede responderla».

Costo: un seguimiento ahora pasa por el supervisor (una llamada al LLM) en vez de atajarse; se prioriza
la **correcta elección** sobre ahorrar esa llamada. La memoria durable del seguimiento (`agente_previo`
del store SQLite, ADR-0001) se mantiene — ahora como pista, no como atajo.

## 3. Verificación LOCAL (hecha)

| Turno | Elegido |
|---|---|
| «qué clima hace en Santiago de Chile» | **Agente de Meteorología** (Chile) |
| «y en Santiago de Compostela?» (seguimiento) | **meteo_mcp** ✅ (antes se quedaba en Meteorología) |
| «clima en Valdivia» → «¿y mañana?» | Meteorología → **Meteorología** (continuidad intacta) |
| «¿y en Concepción?» (Chile) | **Meteorología** (no cambia de más) |

Tests del coordinador: `test_coordinador.py` + `test_guardrails.py` + `test_guardrails_auth_48.py` →
**41 passed**.

## 4. Verificación en el VPS (hecha)

Desplegado con `deploy/deploy_local_a_vps.sh` y reiniciado `t2c2-api`. Verificado en vivo (gateway
`127.0.0.1:8796` del VPS):

| Turno (mismo hilo) | Elegido |
|---|---|
| «qué clima hace en Santiago de Chile» | **Agente de Meteorología** (20,7 °C) |
| «y en Santiago de Compostela?» | **meteo_mcp** ✅ (Meteosource real, 13.5 °C) |
| «clima en Valdivia» → «¿y mañana?» → «¿y en Concepción?» | Meteorología → Meteorología → Meteorología (continuidad intacta) |

Mismo comportamiento que en local: el seguimiento re-rutea al cambiar de dominio y se mantiene en los
seguimientos del mismo tema.

## 5. Estado

- ✅ Arreglo aplicado y **verificado en LOCAL y en el VPS** (re-ruteo correcto + continuidad intacta).
  Afectaba a ambos entornos (mismo código), ahora corregido en los dos. Bitácora **068**, Anexo **19**.
