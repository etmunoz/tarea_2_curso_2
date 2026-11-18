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

## 3. Meteorología: índices adicionales

- UV, calidad del aire y alertas (Open-Meteo los ofrece sin key) como datos extra del pronóstico.
