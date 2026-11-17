<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_003.md`  
> **Objetivo:** 003 · Respuesta — agente_meteorologia convertido a REAL (Open-Meteo + SQLite), probado en vivo  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1534 · **Última modificación:** 20261117 1534
<!--/encabezado-grupo-->

# 003 · Respuesta — agente_meteorologia REAL (Open-Meteo + SQLite)

**Prompt:** [`../prompts_ejecutados/prompt_003.md`](../prompts_ejecutados/prompt_003.md)

> ⚠️ **Método:** publicado **directo en la VPS** (web6, `~/tarea_2_curso_2`). Este `.md` es la bitácora.

---

## 1. Qué se hizo

Se reescribió por completo `src/agente_meteorologia/`, pasando de **datos estáticos** (diccionarios
`PRONOSTICO_HOY`/`PRONOSTICO_SEMANA` del T1) a **consulta REAL** vía Open-Meteo, con persistencia en
SQLite. Diseño clave: la lógica real vive en **módulos de solo-stdlib** (testables sin Gemini ni
dependencias), y `herramientas.py` solo los envuelve con `@tool`.

### Archivos (estructura de paquete)

| Archivo | Rol |
|---|---|
| `ciudades.py` | Catálogo de **18 ciudades de Chile** (lat/lon) + `normalizar()` (sin tildes) + `coords()` + `listado()`. |
| `openmeteo.py` | Cliente Open-Meteo con **`urllib` (stdlib, sin API key)**: `pronostico(lat,lon,dias)` (actual + diario) y `observado(lat,lon,fecha)` (API *archive*, ERA5). Traduce **códigos WMO → texto en español**. TZ fija `America/Santiago`. |
| `bd_clima.py` | **SQLite** (`sqlite3`): tablas `pronosticos` y `observados`; `guardar_pronostico`, `guardar_observado`, `pronostico_guardado`, `observado_guardado`. Ruta por env `CLIMA_DB` (def. `<repo>/logs/clima.sqlite`, sin rutas absolutas incrustadas). |
| `herramientas.py` | 4 `@tool`: `pronostico_hoy`, `pronostico_semana`, `historial_pronostico`, `comparar_pronostico_vs_real`. Las dos primeras **guardan el snapshot** del día al consultar. |
| `prompts.py` | `SYSTEM_METEOROLOGO` reescrito: clima real, SIEMPRE por herramientas, nunca inventar, español, Santiago, no fuera de Chile ni > 7 días. |
| `graph.py` | Sin cambios (ya importa `SYSTEM_METEOROLOGO` + `HERRAMIENTAS`). |

### Esquema SQLite

```sql
pronosticos(ciudad, fecha_emision, fecha_pronosticada, min_c, max_c, precip_mm, codigo, condicion)
  PRIMARY KEY (ciudad, fecha_emision, fecha_pronosticada)
observados(ciudad, fecha, min_c, max_c, precip_mm, codigo, condicion)
  PRIMARY KEY (ciudad, fecha)
```

## 2. Prueba REAL en vivo (en la VPS, stdlib, sin Gemini)

Ejecutado con el `python3` del sistema (sin `uv sync`), salida real:

```
coords Santiago: (-33.4489, -70.6693)
actual: {'temp_c': 22.3, 'codigo': 51, 'condicion': 'Llovizna débil'}
dia0:  {'fecha': '2026-11-17', 'min_c': 13.9, 'max_c': 22.9, 'precip_mm': 8.6, 'codigo': 95, 'condicion': 'Tormenta'}
dias devueltos: 7
filas pronostico guardadas: 7
historial(santiago, dia0): ('2026-11-17', 13.9, 22.9, 8.6, 'Tormenta')
observado 2026-11-07: {'fecha': '2026-11-07', 'min_c': 8.5, 'max_c': 26.1, 'precip_mm': 0.0, 'codigo': 1, 'condicion': 'Mayormente despejado'}
observado guardado OK, releer: (8.5, 26.1, 0.0, 'Mayormente despejado')
DB en: .../tarea_2_curso_2/logs/clima.sqlite
```

**Verificado:** pronóstico real (actual + 7 días), guardado de snapshot (7 filas), relectura de
historial, y **observado real** del archivo (ERA5) para una fecha pasada, guardado y releído. La
comparación pronóstico-vs-real cruza ambos y calcula la diferencia de °C.

`py_compile` de todo el paquete: **OK** (incluye `herramientas.py`, que importa `langchain` pero no se
ejecuta sin venv).

## 3. Estado y cuidados

- ✅ Publicado directo en web6. **No se iniciaron servicios**; a otros proyectos **no se los tocó**.
- ✅ Egress a `api.open-meteo.com` y `archive-api.open-meteo.com` confirmado desde la VPS.
- La ficha de `agente_meteorologia` (registro 002) ya describía esta capacidad: **ahora el código la
  cumple de verdad**.

## 4. Pendientes relacionados

- **Job diario** que tome el snapshot de pronósticos y registre los observados (para acumular
  historial y comparaciones): se hará con **systemd timer** (requiere `sudo` del usuario) o un
  scheduler liviano. Hoy, cada consulta de `pronostico_hoy`/`pronostico_semana` ya guarda el snapshot
  del día.
- **Prueba del agente end-to-end** (vía Gemini + langgraph): pendiente de `GOOGLE_API_KEY` en el `.env`
  de web6.
- Open-Meteo *archive* (ERA5) tiene algunos días de desfase; para fechas muy recientes el observado
  puede no estar aún (se maneja devolviendo "sin dato" sin romper).

## 5. Próximos pasos sugeridos

1. **Coordinador all-local** (`A2A_GRAFOS_LOCALES` con los 8 grafos, sin `URLS_AGENTES`) + `.env.example`.
2. **`src/api` (FastAPI + API_KEY)** y **`src/memoria` (SQLite)**.
3. **Prueba controlada** de `langgraph` en `:2025` cuando haya `GOOGLE_API_KEY` y swap.
