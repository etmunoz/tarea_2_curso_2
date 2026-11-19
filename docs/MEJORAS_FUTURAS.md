<!--encabezado-grupo-->
> **Archivo:** `docs/MEJORAS_FUTURAS.md`  
> **Objetivo:** Backlog de mejoras futuras (ideas acordadas, no implementadas aún)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1320 · **Última modificación:** 20261118 1320
<!--/encabezado-grupo-->

# Mejoras futuras (backlog)

Ideas acordadas pero **no implementadas** aún. Al tomar una, dejar su registro en
`prompts_ejecutados/` + `respuestas/` y actualizar [`ARQUITECTURA.md`](ARQUITECTURA.md).

## 1. Viajes: vuelos y hoteles con precios REALES (requiere API con key)

- **Estado hoy:** `buscar_vuelos`, `buscar_hoteles` y `buscar_actividades` son **demo** (datos de
  ejemplo, marcados `fuente="demo"`) porque los precios reales exigen una API con credenciales, lo que
  queda fuera del diseño keyless actual. Lo **real** de viajes ya funciona (destino, tipo de cambio,
  clima mundial, resumen de Wikipedia — registro 032).
- **Propuesta:** conectar una API de viajes con *free tier*, p. ej. **Amadeus Self-Service**
  (`test.api.amadeus.com`): OAuth2 client-credentials → `GET /v2/shopping/flight-offers` (vuelos) y
  `/v3/shopping/hotel-offers` (hoteles).
- **Cómo encaja sin romper la seguridad:** guardar `AMADEUS_CLIENT_ID` / `AMADEUS_CLIENT_SECRET` en el
  **almacén de config** (`src/config/ajustes.py` PERMITIDAS) o en `/etc/t2c2.env`, **nunca** en el repo;
  cliente nuevo `src/agente_viajes/amadeus.py` (stdlib, patrón de `clientes.py`), token cacheado.
  Reemplazar las tools demo por reales (o dejar fallback demo si falta la key).
- **Requisito del usuario:** conseguir las credenciales del free tier y pasarlas por pantalla/almacén
  (como se hizo con `REDIS_URL`).

## 2. Administrador + onboarding de correo

- Que el Agente Administrador ayude activamente a **registrar el correo** del usuario y dé el tutorial
  inicial (hoy ese flujo vive en la UI del chat; el administrador solo orienta).

## 3. Checkpointer persistente nativo de LangGraph (coordinador)

- **Hoy:** el coordinador compila con `InMemorySaver` (memoria de corto plazo del hilo en RAM, se pierde
  al reiniciar). El seguimiento ("¿y en Santiago?") ya es **durable** porque el agente del turno anterior
  se lee del store `memoria` SQLite (registro 036), así que esto no es urgente.
- **Propuesta:** usar un checkpointer persistente nativo (`SqliteSaver`/`PostgresSaver`) para que TODO el
  estado del hilo (mensajes + ruta) sobreviva reinicios sin lógica aparte.
- **Bloqueo actual:** `langgraph-checkpoint-sqlite` (2.0.11) pinnea `langgraph-checkpoint` 2.x, mientras
  nuestro `langgraph` 1.2 usa checkpoint 4.3.1. Requeriría **subir langgraph a 2.x**, lo que toca todo el
  runtime A2A (`langgraph-api`/`langgraph dev`, `cli`, `sdk`, `swarm`): migración deliberada y probada,
  no un cambio menor. Dejar para cuando se justifique.
- **Decisión formal:** [`decisiones/ADR-0001-memoria-corto-plazo.md`](decisiones/ADR-0001-memoria-corto-plazo.md)
  (por qué NO `SqliteSaver` y qué usamos en su lugar).

## 4. Meteorología: índices adicionales

- UV, calidad del aire y alertas (Open-Meteo los ofrece sin key) como datos extra del pronóstico.
