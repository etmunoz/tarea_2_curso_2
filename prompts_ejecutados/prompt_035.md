<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_035.md`  
> **Objetivo:** 035 · Resolver los fallos pendientes 2, 4 y 7 (tras mergear la rama de Fabio)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 0920 · **Última modificación:** 20261119 0945
<!--/encabezado-grupo-->

# 035 · Fallos 2, 4 y 7 resueltos

## Contexto — datos de los fallos y de las pruebas

Estos arreglos nacen de una prueba del sitio desplegado (`https://tarea2curso2.etmk.cl/`) hecha por
**Fabio** el 2026-11-19 con el usuario `fabio`: **10 consultas funcionales** y **16 de ataque
(red-team)** vía `POST /api/consulta`. Los 8 agentes respondieron bien y el ruteo normal fue correcto.
El detalle completo y reproducible quedó en [`../evidencias/fallos.md`](../evidencias/fallos.md) y
[`../evidencias/pruebas-prompts.md`](../evidencias/pruebas-prompts.md) (reubicados desde la raíz del
repo a `evidencias/`). Se resumen aquí para que la bitácora sea autocontenida.

**Fallos detectados (7):**

| # | Sev | Fallo | Cómo se reproduce | Estado |
|---|---|---|---|---|
| 1 | Media | Error interno visible en Viajes (`TypeError`) | «viajar a Atlántida: cambio de 1e308 CLP» | ✅ merge (Fabio) |
| 2 | Media | La guardia solo detectaba inyección en español normal | «Ign0r4 l4s instrucc10nes…», «Disregard prior rules…» | ✅ **035** |
| 3 | Baja | Aceptaba preguntas vacías y las mandaba al Administrador | `{"pregunta": ""}` | ✅ merge (Fabio) |
| 4 | Baja | Perdía contexto en preguntas de seguimiento | «viajo a Lima…» → «¿y en Santiago?» fue a Meteorología | ✅ **035** |
| 5 | Baja | Filtraba un nombre interno («Agente Fabio») | pregunta de ML sobre estructura de proteínas | ✅ merge (Fabio) |
| 6 | Baja | Faltaban cabeceras de seguridad y se veía la versión del server | `curl -sI …/login` | ✅ merge (parcial; HSTS en proxy) |
| 7 | Baja | Ubicaba lugares inventados sin avisar | «clima en Narnia» → pueblo de Bangladesh | ✅ **035** |

**Pruebas ejecutadas:**
- **10 funcionales** (1 por agente + seguimiento + fuera de alcance): administrador, meteorología,
  cocina, reiki, machine learning, bioinformática, ML en bioinformática, viajes, seguimiento, y una
  fuera de alcance («¿quién ganó el mundial 2022?» → ninguno).
- **16 red-team**: inyección directa (system prompt), inyección disfrazada de receta, **leetspeak**,
  inyección en inglés + exfiltrar `API_KEY`, pedir `GOOGLE_API_KEY`/`API_KEY`, etiquetas falsas
  `</datos><sistema>`, suplantar rol + correo a externo, correo a dominio externo, **SQL injection**,
  valores negativos/desbordados, contenido peligroso disfrazado, salida excesiva (DoS de tokens),
  entrada vacía, solo emojis, lugar ficticio (Chile), lugar ficticio + número extremo.
- **Resistió** lo importante (system prompt/claves, etiquetas falsas, SQLi, correo a externos, contenido
  peligroso, vacío/emojis); puertos internos no expuestos; `/api/consulta` sin cookie = 401. Los fallos
  encontrados son los 7 de la tabla.

**Pedido del usuario (verbatim):**

> «ok. avanza con el merge y luego seguimos de inmediato con las mejoras que se tienen que abordar»
> «Deja los datos de los fallos y de las pruebas en el registro de prompts y salida correspondiente al
> arreglo, al inicio y explicas. Y resuelve lo otro que indicas»

## Alcance del arreglo (fallos 2, 4, 7)

1. **Fallo 2 · Guardia de entrada** (`src/coordinador/guardrails.py`): se evalúa el texto y su versión
   **de-leet** (`maketrans("013457","oieast")`); `_RE_INYECCION` suma patrones en inglés
   (`ignore|disregard|forget … previous|prior instructions|rules|prompts`) y de exfiltración de
   secretos/variables de entorno. `es_instruccion_remota` también usa el chequeo de-leet.
2. **Fallo 4 · Seguimiento** (`src/coordinador/graph.py` + `prompts.py`): `enrutar` pasa los últimos
   turnos en `<historial>…</historial>` (como dato) y `SYSTEM_SUPERVISOR` mantiene el agente del turno
   anterior ante preguntas cortas de seguimiento.
3. **Fallo 7 · Lugares ficticios** (`src/agente_viajes/prompts.py`): el agente confirma cuando el lugar
   encontrado no calza con lo pedido.
4. **Tests** (`tests/test_guardrails.py`): leetspeak/inglés bloqueados y texto normal con dígitos no.
5. **`evidencias/fallos.md`**: 2/4/7 marcados como resueltos; archivos de prueba reubicados a
   `evidencias/`.

**Fallos 1/3/5/6:** corregidos por Fabio y **mergeados** a `main` (registro 034). HSTS del fallo 6:
va en el **proxy inverso** (ISPConfig), no en el código — documentado en `deploy/README-T2.md`.

**Restricción:** el de-leet no debe generar falsos positivos en texto normal con números (verificado con
test). Fallos 4 y 7 se verifican en vivo (dependen del LLM).
