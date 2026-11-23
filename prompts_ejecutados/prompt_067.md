<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_067.md`
> **Objetivo:** 067 · Montaje LOCAL y captura de evidencias (entrega base de la rúbrica)
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
> **Creación:** 20261123 1830 · **Última modificación:** 20261123 1830
<!--/encabezado-grupo-->

# 067 · Evidencia LOCAL (montaje y capturas)

**Pedido del usuario (verbatim):**

> «Luego hacemos ahora la captura local de inmediato. Copia tu las claves que necesites, y levanta un
> posgresql local y usa el redis remoto que ya tiene la solución en la VPS tu saca con cuidado las
> claves que requieras y las agregas al .env» … «estás instalando posgresql en el MAC o en un Docker?»
> → «ok» (brew nativo) … «todo registrado como prompt, luego su salida y al final evidencias como
> siempre.»

**Contexto:** del contraste (registro 066) la brecha principal es la **evidencia de ejecución LOCAL**
(la entrega obligatoria es local; el VPS cuenta como el +1). El usuario autoriza copiar con cuidado las
claves necesarias desde el VPS al `.env` local, levantar **PostgreSQL local** y **reusar el Redis
remoto** del VPS. El usuario aporta por su lado: correo recibido (su bandeja), muestra de voz
(audio/video) y capturas de la UI del sitio en vivo.

**Decisiones de montaje:**
- **Secretos al `.env` local sin pasar por el chat:** `GOOGLE_API_KEY` (desde `/etc/t2c2.env`) y el
  `REDIS_URL` REAL (desde el almacén de config `logs/config.sqlite`, no el placeholder de `/etc`).
  `RAG_BACKEND=redis`. Valores nunca impresos (solo longitudes).
- **meteo_mcp se EXCLUYE en local:** en el Mac `cryptography` no carga (`libssl.4.dylib` ausente), así
  que el adaptador MCP no importa. Se corre con los **otros 8 agentes** vía `langgraph.local.json`
  (gitignorado; apaño solo de desarrollo, no parte de la entrega). En producción (VPS) siguen los 9.
- **PostgreSQL local nativo (brew, sin sudo)**, no Docker (coincide con el VPS; más liviano). Rol/base
  `t2c2` locales; `PG_DSN` en el `.env` local → el coordinador usa `PostgresSaver` también en local.

**Alcance de captura (lo que hago yo, rotulado LOCAL + fecha):**
1. Acceso: `GET /agentes` **sin** API_KEY → 401; **con** API_KEY → 200 (sin exponer la clave).
2. Consulta real `POST /consulta` con ruteo + A2A (p. ej. clima, administrador).
3. Chat web `http://127.0.0.1:8797/` (pregunta + respuesta) — captura del navegador.
4. Monitor `http://127.0.0.1:8798/` — panel de accesos 200/401.
5. `[coordinador] checkpointer: postgres` en local (memoria durable con el Postgres local).

**Entregable:** `respuestas/salida_067.md` + capturas en `evidencias/` (rotuladas LOCAL) + Anexo 18 y
actualización de la tabla de casos de `EVIDENCIAS.md` (columna Entorno → LOCAL).
