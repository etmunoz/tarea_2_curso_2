<!--encabezado-grupo-->
> **Archivo:** `evidencias/backend_local.md`  
> **Objetivo:** Evidencia LOCAL — control de acceso, consulta real y memoria durable (coordinador)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
<!--/encabezado-grupo-->

# Backend — **LOCAL**, 2026-11-23

**Entorno y fecha:** LOCAL (Mac), 2026-11-23. FastAPI `127.0.0.1:8796` + langgraph `127.0.0.1:2025` (8 agentes;
`meteo_mcp` se prueba en VPS). La **API_KEY no se muestra**.

## 1. Control de acceso (clave validada en el servidor)

| Solicitud | Resultado esperado | Resultado obtenido |
|---|---|---|
| `GET /salud` | 200 | **200** |
| `GET /agentes` **sin** API_KEY | 401 (rechazado) | **401** |
| `GET /agentes` **con** API_KEY | 200 + agentes | **200**, 9 fichas (8 ruteables en local; `meteo_mcp` es el 9º, probado en VPS) |

## 2. Consulta real con ruteo A2A (recorrido completo)

`POST /consulta` "¿Qué clima hará hoy en Valdivia?" → **agente_meteorologia** (Open-Meteo real):
```
ruta: guardia_entrada → supervisor → agente_local → guardia_salida
[agente_meteorologia] Valdivia hoy — actual 14,1 °C, mín 10,0, máx 16,9, Llovizna débil, 1,3 mm
```
(La misma consulta por la **UI web** en `127.0.0.1:8797` muestra la respuesta etiquetada `[agente_meteorologia]`
y el panel "Ruteo del coordinador" con la ruta A2A — captura de UI aportada por el equipo.)

## 3. Memoria durable del coordinador (PostgresSaver LOCAL)

Con `PG_DSN` a un **PostgreSQL local**, el coordinador arranca con PostgresSaver:
```
[coordinador] checkpointer: postgres
```
Tabla `checkpoints` del Postgres local: **114 filas** (con InMemorySaver serían 0 → confirma que persiste).
Regla verificada: si falta `PG_DSN` o Postgres no está, cae a `InMemorySaver` sin romper el gateway.

## 4. Funcionamiento de TODOS los agentes

Ver [`agentes_local.md`](agentes_local.md): una consulta real por agente (8/8 ruteados correctamente),
con fuentes reales (Gemini, Redis remoto, Open-Meteo, UniProt, tipo de cambio, Wikipedia).
