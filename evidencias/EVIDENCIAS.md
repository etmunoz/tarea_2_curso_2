<!--encabezado-grupo-->
> **Archivo:** `evidencias/EVIDENCIAS.md`  
> **Objetivo:** Evidencias reales de la Tarea 2 (tablas §10) + guía de capturas  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
<!--/encabezado-grupo-->

# Evidencias — Tarea 2 · Curso 2

**Entorno:** VPS `server28.etmk.cl` (web6), aislado de la Tarea 1. Publicado por HTTPS:
- App (chat + voz): **https://tarea2curso2.etmk.cl/**
- Monitor: **https://monitortarea2curso2.etmk.cl/**
- Backend local: FastAPI `127.0.0.1:8796`, agentes `langgraph` `127.0.0.1:2025`, BFF `:8797`, monitor `:8798`.

**Reproducción local:** ver `README.md` (`uv sync`, `.env`, levantar langgraph + FastAPI + web). Pruebas
automáticas sin secretos: `uv run --with pytest pytest tests/test_tarea2.py -q` → **8 passed**.

Todas las evidencias son de **ejecución real** (no simulada). Lo pendiente de capturar por el usuario se
marca como *(captura)*.

---

## Tabla de casos (§10)

| # | Caso | Entorno y fecha | Solicitud | Resultado esperado | Resultado obtenido | Obs. |
|---|---|---|---|---|---|---|
| 1 | **Seguridad — acceso RECHAZADO** | VPS, 2026-11-17 | `GET /agentes` **sin** API_KEY | HTTP **401** | **401** | sin exponer la clave |
| 2 | **Seguridad — acceso PERMITIDO** | VPS, 2026-11-17 | `GET /agentes` con `X-API-Key` | HTTP **200** + 8 agentes | **200**, 8 agentes | — |
| 3 | **Impl 1 / A2A — meteorología real** | VPS, 2026-11-17 | `POST /consulta` "clima hoy en Valdivia" | ruteo a meteorología + datos reales | **Agente de Meteorología**, datos Open-Meteo (16,5 °C; mín 12,5/máx 18,7; chubascos; 8,4 mm) | ruta: `guardia_entrada→supervisor→agente_local→guardia_salida` |
| 4 | **Ruteo meta — administrador** | VPS, 2026-11-17 | `POST /consulta` "¿qué agentes hay?" | ruteo al administrador | **Agente Administrador** lista agentes en español | — |
| 5 | **Impl 2 — web de chat (HTTPS)** | público, 2026-11-17 | `https://tarea2curso2.etmk.cl/` con login | chat responde | 200 + chat; login propio (BFF, API_KEY server-side) | *(captura del chat)* |
| 6 | **Impl 2 — correo** | VPS, 2026-11-17 | despacho a destinatario registrado | correo con ruta + grafo | **recibido** en etmunoz@gmail.com (`enviado`); fuera de allowlist → rechazado | *(captura del correo)* |
| 7 | **Impl 3 — voz (Etapa A)** | público, 2026-11-17 | `https://tarea2curso2.etmk.cl/voz` | STT→agentes→TTS | página operativa (SpeechRecognition/`es-CL` + speechSynthesis) | *(audio/video)* |
| 8 | **Monitor — operación/seguridad** | público, 2026-11-17 | `https://monitortarea2curso2.etmk.cl/` | panel con 200/401, despachos, allowlist | Accesos 8 (7 OK / 1 rechazado 401), despachos (enviado/fallo), allowlist, **Clave Gemini: OK** | *(captura del panel)* |
| 9 | **Publicación — force-HTTPS** | público, 2026-11-17 | `http://…` en ambos subdominios | redirige a `https` | **http → 301 → https** en app y monitor | — |
| 10 | **Reproducibilidad — pruebas** | VPS, 2026-11-17 | `pytest tests/test_tarea2.py` | suite en verde | **8 passed** | sin secretos ni red |

---

## Evidencia técnica (salidas reales capturadas)

**Acceso al gateway (200/401):**
```
GET /salud                 -> 200  {"estado":"ok"}
GET /agentes  SIN API_KEY  -> 401
GET /agentes  CON API_KEY  -> 200   (8 agentes)
```

**Consulta real 1 — meteorología (Open-Meteo):**
```
elegido: Agente de Meteorología | ruta: guardia_entrada → supervisor → agente_local → guardia_salida
[Agente de Meteorología] Valdivia hoy — actual 16,5 °C, mín 12,5, máx 18,7, Chubascos débiles, 8,4 mm
```

**Consulta real 2 — administrador:**
```
elegido: Agente Administrador | ruta: guardia_entrada → supervisor → agente_local → guardia_salida
[Agente Administrador] ¡Hola! … (lista de agentes y funciones en español)
```

**Correo:** `enviar(...) -> {'ok': True}` → recibido en etmunoz@gmail.com con la **ruta de los agentes**
y el **gráfico del grafo del coordinador** (PNG) al pie.

**Publicación pública (ambos subdominios):**
```
http  → 301 → https
https sin login → 401
https con login → 200   (app: chat; monitor: panel)
```

**Monitor (panel real):** Accesos 8 · Permitidos 7 · Rechazados (401) 1 · Destinatarios 1 ·
Clave Gemini: OK. Tabla de accesos con `POST /consulta 200`, `GET /agentes 200`, `GET /agentes 401`,
`GET /salud 200`. Despachos: `enviado` y `fallo`. Allowlist: etmunoz@gmail.com (activo).

---

## Guía de capturas (para el usuario)

1. **Chat** (`https://tarea2curso2.etmk.cl/`): una consulta respondida con su **ruta** (p. ej.
   "clima hoy en Valdivia").
2. **Voz** (`/voz`): breve **audio/video** hablando → transcripción → respuesta leída.
3. **Correo**: captura del correo recibido en Gmail (encabezado, respuesta, ruta y **gráfico del grafo**).
4. **Seguridad**: el **monitor** mostrando `GET /agentes` **200** (con API_KEY) y **401** (sin API_KEY).
5. **Monitor**: panel completo (accesos, despachos, allowlist, **Clave Gemini: OK**).
6. **HTTPS**: barra del navegador con el candado en `https://tarea2curso2.etmk.cl`.

> Guardar las capturas en esta carpeta `evidencias/`. Ocultar/parear cualquier secreto (API_KEY, claves).

---

## Anexo · Chat web (diseño Taller 1) — funcionalidades

- **Diseño** del Taller 1: fondo aurora, tarjetas **Chat + Ruteo del coordinador**, chips de agentes, tema claro/oscuro.
- **Ruteo por turno**: el panel muestra SOLO la ruta del turno actual (verificado: 2 consultas en la misma sesión → 4 pasos cada una, no acumula).
- **🧭 Ver ruteo**: re-muestra el ruteo de una respuesta anterior.
- **✉️ Enviar por correo**: desde cada respuesta, a destinatarios de la allowlist (con ruta + gráfico del grafo). Verificado: `/correo` configurado=True; envío fuera de allowlist → rechazado.
- Todo pasa por el BFF (`/api/...`) que agrega la API_KEY server-side; el navegador nunca la ve.

---

## Anexo 2 · Multiusuario, sesiones y seguridad

- **Usuarios con login propio:** ezequiel (admin), gustavo, fabio, cristobal, jose. Claves hasheadas (PBKDF2+salt).
- **Clave inicial única + cambio obligatorio** al primer ingreso. Verificado: login clave mala → 401; login OK → 302 /cambiar-clave; `/api/yo` con cambio pendiente → 409.
- **Admin** (ezequiel) resetea claves en `/usuarios`.
- **Seguridad de sesión:** cookie HttpOnly+SameSite=Lax+Secure, caducidad 8 h, anti-fuerza-bruta (6 intentos/5 min).
- **Flujo por usuario:** chat/historial propios (claves `t2_thread_<u>`, `t2_hist_<u>_<thread>`); el gateway namespacea el hilo `usuario:sesion`.
- **Eventos al monitor:** login, logout, cambio_clave, reset (sección "Eventos de usuario"). Verificado: evento `gustavo·login` registrado.
- **Autogestión de correo:** si el usuario no tiene correo, la UI lo da de bienvenida y le ayuda a registrarlo (allowlist).
- **Salidas formateadas (Markdown):** negritas, listas, títulos y código renderizados en el chat.

---

## Anexo 3 · RAG de Reiki en Redis cloud

- **Backend migrado a Redis** (RediSearch), índice **`t2c2_duran_reyes_munoz_reiki`** (namespaceado al
  grupo; el Redis es compartido del curso). DB lógica `0`.
- **Config sin sudo:** `REDIS_URL` guardada en el almacén `config.sqlite` vía `deploy/set_redis_url.sh`
  (lectura **oculta**, nunca en el chat ni en `/etc`). `rag.py` la resuelve desde el almacén.
- **Verificación concluyente:** con `logs/reiki_rag.json` (artefacto local) movido a `.bak`, la consulta
  al Agente de Reiki **igual respondió** correctamente → la respuesta vino de Redis.
  - `PING=True`, `FT._LIST` responde (RediSearch OK), **9 fragmentos** indexados.
  - `ruta: guardia_entrada → supervisor → agente_local → guardia_salida`.

---

## Anexo 4 · Terapias holísticas complementarias (agente_reiki)

Nuevo documento `data/reiki/terapias-complementarias.md` + herramienta `terapias_complementarias` +
prompt actualizado. Reindexado en Redis: **18 fragmentos** (antes 9). Verificado en vivo (gateway):

- **Recomendación (estrés/ansiedad)** → Agente de Reiki: *"autotratamiento de Reiki en pecho y plexo
  solar con respiración abdominal 4-6 y aromaterapia de lavanda…"* + disclaimer de bienestar.
- **Recomendación (sueño)** → Agente de Reiki: *"sesión breve de Reiki en nuca y frente, sonoterapia
  suave y rutina de sueño sin pantallas…"* + disclaimer.
- **Borde médico (hipertensión)** → **no** da consejo médico: *"no puede curar enfermedades ni
  reemplazar la medicación… sigue las indicaciones de tu médico, Reiki solo como apoyo"*. Guardrail OK.
- Todas con `ruta: guardia_entrada → supervisor → agente_local → guardia_salida`.

## Anexo 5 · Bioinformática real (UniProt en vivo)

Agente de Bioinformática con herramienta `consultar_proteina` (UniProt REST, sin API key). Verificado
en producción (gateway):

- **TP53** → `P04637` · Homo sapiens · 393 aa · función oficial · URL de UniProt.
- **BRCA1** → `P38398` · 1863 aa. **INS** → `P01308`. **hemoglobin** → `HBB` (P68871).
- Datos **en vivo** y citables (accession + URL); corregida la relevancia con `gene_exact` + humano
  por defecto (antes "TP53" por texto libre traía MDM2).
- Ruteo: `guardia_entrada → supervisor → agente_local → guardia_salida` (ficha actualizada).

---

### Catálogo ampliado (registro 027) + arreglo de ruteo

- **Duelo** → Reiki en el corazón + respiración/gratitud + diario de recuerdos (deriva a apoyo psicológico).
- **Concentración** → Reiki frente/corona + respiración 2–3 min + menta/romero + pausas.
- **Cefalea tensional** → manos en sienes/nuca/hombros + respiración + compresa tibia + hidratación
  (deriva si es intenso/súbito/frecuente).
- **Fix de ruteo:** "dolor de cabeza tensional" ruteaba a `ninguno` (el supervisor lo leía como médico);
  se enriqueció la **ficha** del `agente_reiki` (`src/fichas.py`) con los objetivos de bienestar. Tras
  aplicarla, rutea al Agente de Reiki incluso con la frase pelada *"Tengo dolor de cabeza tensional,
  qué me recomiendas?"* (`elegido: Agente de Reiki`).
- **Captura (GUI del Redis):** [`redis_reiki_indice.png`](redis_reiki_indice.png) — índice
  `t2c2_duran_reyes_munoz_reiki` con **9 keys** (HASH) en `nut-milk-xenic-58289.db.redis.io:10484`
  **DB 0**; campos `fuente`, `text`, `_index_name`, `embedding` (vector binario). No expone la clave.
