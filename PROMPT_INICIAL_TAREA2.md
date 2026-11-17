# PROMPT INICIAL — Tarea 2 · Curso 2 (Taller de implementación y ejecución local)

> Este es el **primer prompt** que pegaré para arrancar la Tarea 2. Es la fuente de verdad del
> encargo, la arquitectura heredada y las decisiones. **Léelo entero. No crees ni toques nada en la
> VPS hasta evaluar el espacio y tener mi OK. Entrégame un plan para validar antes de ejecutar.**

---

## 0. Identidad

- **Curso 2 · Taller de implementación** — "Implementa y entrega tu agente". **Plazo: 1 semana.**
- **Grupo:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz.
- **Repo nuevo:** `tarea_2_curso_2` (carpeta ya creada en `/Users/ezequielmunoz/proyectos/tarea_2_curso_2`).
- **Base:** se **reutiliza el Taller 1** (`tarea_1_curso_2`): agentes A2A, coordinador/supervisor,
  guardrails, coordinador web, correo, monitor, despliegue systemd+Apache+HTTPS. Taller 2 = **conectar
  esos agentes a formas de uso reales, ejecutables y probables en LOCAL.**
- **Entrega obligatoria: LOCAL y reproducible.** Nube = **+1 opcional**.

## 1. Objetivo y rúbrica (qué evalúan)

Una persona del equipo docente debe poder **repetir una consulta completa** con el código entregado.
Evalúan: **funcionamiento real**, **seguridad**, **reproducción desde la entrega** y **calidad de
evidencias**. Una respuesta fija/simulada NO cuenta. Elegir **al menos una** implementación; nosotros
**aspiramos a las TRES** (puntaje 3 > 2 > 1), con **prioridad en la avanzada (3)**. Declarar por cada
una: opción, problema que resuelve y qué se reutiliza del Taller 1.

## 2. ARQUITECTURA CENTRAL — FastAPI es el ÚNICO gateway a los agentes (requisito duro)

**Toda comunicación entre cualquier frontend/canal y los agentes pasa por un backend FastAPI. Los
agentes NUNCA se llaman directo desde el frontend ni desde fuera: solo a través de FastAPI.**

```
  [Frontend web de chat]        [Canal avanzado: avatar por VOZ en el sitio (Impl 3, §3)]
            │   (el navegador habla con su backend; la API_KEY NO viaja al browser)
            ▼
     ┌───────────────────────────────────────────────┐
     │  BACKEND FastAPI  (único punto de entrada)      │
     │  · valida API_KEY en CADA endpoint que invoca   │
     │    agentes (header, p. ej. X-API-Key)           │
     │  · guardrails de entrada/salida                 │
     │  · invoca el COORDINADOR/supervisor             │
     └───────────────────────┬───────────────────────┘
                              ▼   (solo 127.0.0.1, NO expuesto)
          Coordinador (LangGraph) → agentes locales (langgraph dev :<puerto>)
```

- **FastAPI = backbone.** El **frontend web** y el **canal avanzado** hablan con FastAPI; FastAPI
  invoca al coordinador y a los agentes. No hay llamadas directas frontend→agente.
- **Protección por `API_KEY` (del `.env`):** cada endpoint de FastAPI que **invoca agentes** exige una
  **`API_KEY`** (variable en `.env`, la define el usuario) validada en el **servidor**. Sin API_KEY
  válida → **401**. Esto **protege de llamadas intrusas directas a los agentes**: el único modo de
  llegar a un agente es por FastAPI con la API_KEY.
- **Agentes aislados:** `langgraph dev` escucha **solo en `127.0.0.1`** y **no se publica** por Apache.
  El **único subdominio público** es el de FastAPI (tras proxy + HTTPS). El monitor es aparte.
- **API_KEY fuera del navegador (rúbrica):** el web frontend es un **BFF** — el **servidor** del web
  guarda la `API_KEY` y llama a FastAPI; el **browser** nunca ve la API_KEY (solo se autentica al web
  con su propio login/sesión). Igual para el canal avanzado: el conector guarda la API_KEY server-side.
- Endpoints FastAPI mínimos: `POST /consulta` (pregunta → ruteo → respuesta integrada), `GET /salud`,
  `GET /agentes` (catálogo). Errores claros (400/401/502) sin filtrar internos.

## 3. Las TRES implementaciones (todas montadas sobre el gateway FastAPI)

### Implementación 1 — Servicio FastAPI (la API protegida; es el core)
- La API protegida por **API_KEY** que expone el coordinador/agentes (ver §2). Revisan **seguridad**,
  **colaboración A2A** y **fidelidad de la conclusión**: datos, cálculos, **unidades** y supuestos se
  conservan al integrar (p. ej. CLP, °C, métricas). Pedir datos faltantes antes de concluir.
- Reutiliza: `src/coordinador/*`, guardrails, catálogo, los agentes locales.

### Implementación 2 — Canal de atención: web de chat + correo
- **Frontend web de chat** (evolución de `tools/coordinador_web.py`): el usuario pregunta, ve la
  respuesta y el **ruteo**. **Habla con FastAPI** (BFF con la API_KEY server-side), con **control de
  acceso** propio (Basic Auth o login).
- **Despacho por correo** desde **`tarea2curso2@etmk.cl`** (SMTP submission 587 + STARTTLS), **solo a
  destinatarios registrados** (§7); **nunca auto-envío** desde respuestas de agentes; disparo solo por
  el usuario. **Formato del correo (obligatorio):**
  - Cuerpo **HTML bien formateado y legible** (encabezado, respuesta con títulos/listas/énfasis,
    tipografía y espaciado decentes), con **versión texto plano** de respaldo. Hora en **Santiago**,
    en **español**.
  - **Al pie del correo**, para dejar constancia de **por dónde pasó el flujo**:
    1. **La RUTA que hicieron los agentes** en esta consulta (p. ej. `guardia_entrada → supervisor →
       agente_X → guardia_salida`, indicando qué agente(s) respondieron).
    2. El **gráfico del grafo de LangGraph** del coordinador (diagrama del flujo), **embebido como
       imagen** al final (p. ej. PNG desde `graph.get_graph().draw_mermaid_png()`, cacheado; adjunto
       inline por CID). Si no se puede renderizar la imagen, incluir el Mermaid en texto como respaldo.
- Revisan: la solicitud que entra, la conexión con los agentes (vía FastAPI) y la respuesta/entrega.

### Implementación 3 — Integración avanzada (META PRINCIPAL) — **YA DECIDIDA: avatar conversacional por VOZ en el sitio, por etapas**

**Decisión tomada (no re-preguntar cuál hacer):** la integración avanzada es un **avatar que conversa
por VOZ en el propio sitio web**. El usuario **habla** (no teclea); el navegador transcribe su voz
(STT) y **manda el texto a FastAPI por cuenta del usuario**; los agentes responden (vía coordinador) y
el sitio **lee la respuesta en voz alta** (TTS). Todo **sobre el gateway FastAPI** (§2), con la
**API_KEY server-side** (el browser nunca la ve). Foco de la rúbrica aquí: **que funcione de verdad**;
menos profundidad A2A; se mantienen **seguridad** y **evidencias** (audio/video).

Se construye **por etapas**, cada una **condicionada** a que la anterior quede estable:

#### Etapa A — Conversación por VOZ (BASE, OBLIGATORIA)
- **Pipeline:** botón de micrófono → **STT en el navegador** (Web Speech API, `SpeechRecognition`,
  idioma **`es-CL`**) → texto → **POST a FastAPI** (BFF con la API_KEY server-side) → coordinador /
  agentes → respuesta formateada → **TTS en el navegador** (`speechSynthesis`, voz en español) que la
  **lee en voz alta**.
- **El usuario no escribe:** lo transcribe el STT "por cuenta del usuario". La transcripción se muestra
  y es **confirmable/editable** antes de enviarse (para corregir errores de reconocimiento).
- **UI:** botón de micrófono, indicador animado y **estados visibles** (escuchando / pensando /
  hablando), transcripción en pantalla, y la respuesta también **en texto** (además del audio) con el
  **formato** del §4.2 y el **ruteo** visible.
- **Costo y cuentas:** **gratis, sin API key, sin cuentas** (Web Speech API es del navegador).
- **Caveats a documentar:** funciona en **Chrome/Edge** (soporte de `SpeechRecognition` limitado en
  otros); requiere **internet** (el STT de Chrome usa servicio en la nube de Google), **permiso de
  micrófono** del usuario, y hay algo de **latencia**. Degradar con mensaje claro si el navegador no
  soporta STT/TTS (fallback: teclado + lectura TTS).
- **Evidencia:** **audio/video** de una conversación real (hablo → se transcribe → responde → lo lee).

#### Etapa B — Avatar 2D animado (CONDICIONAL a que A funcione)
- **Solo si la Etapa A quedó estable.** Se **reutiliza la misma tubería** de A (no se rehace nada del
  STT↔FastAPI↔TTS): se añade **únicamente la capa visual** — un **avatar 2D** (imagen/SVG/sprite o
  librería liviana) que **se anima mientras suena el audio** del TTS (boca/indicador al hablar, estado
  en reposo al escuchar).
- **Sin cuentas ni costos** (animación local, dirigida por los eventos de `speechSynthesis`).
- **Evidencia:** video del avatar hablando sincronizado con el audio.

#### Etapa C — Avatar realista con lip-sync (OPCIONAL, extra, de pago)
- **No se compromete en la base.** Avatar foto-realista con **lip-sync** vía SaaS (**HeyGen / D-ID /
  Simli**) por **SDK / WebRTC**. Requiere **cuenta + API key + créditos (de pago)**; la **key va
  server-side** (nunca en el browser) y hay que **controlar costos** (límites, cuentas de prueba).
- Se aborda **solo** si A y B están listas y hay tiempo/presupuesto. **Evidencia:** video con el avatar
  realista.

**Resumen de la decisión:** **A** es la meta avanzada obligatoria; **B** se intenta si **A** funciona;
**C** es un plus opcional de pago. Antes de construir, entrégame el plan de **A** (endpoints FastAPI que
usa, UI, manejo de permisos/errores) para validarlo.

## 4. Catálogo de agentes — copiar TODOS, LOCALES, renombrados `agente_<funcionalidad>`

**Cambio clave respecto del T1: en la Tarea 2 los agentes NO son remotos (sin túneles de compañeros);
se copian TODOS y corren LOCALES, para que la app quede FULL OPERATIVA y autocontenida.** El
coordinador rutea solo a agentes locales. El fallback remoto→local del T1 deja de ser necesario (no hay
remotos), pero el ruteo/guardrails se conservan. Al renombrar, actualizar `langgraph.json`,
`src/fichas.py`, el catálogo y los tests. **Cada agente conserva su estructura de PAQUETE del T1 —
`__init__.py`, `graph.py`, `herramientas.py`, `prompts.py` + sus módulos de datos (`bd_*.py`, `rag.py`,
cliente de API); NUNCA un solo `.py` suelto** (detalle de archivos por agente en §11).

| Nuevo nombre | Origen T1 | Herramientas (reales) |
|---|---|---|
| `agente_machinelearning` | `agente_ezequiel` | `recomendar_tecnica`, `metricas_recomendadas`, `elegir_modelo`, `consultar_modelos` (SQLite) |
| `agente_mlbioinformatica` | `proteinman` | mismas 4 (catálogos de datos biológicos) |
| `agente_bioinformatica` | `agente_fabio` | `consultar_mis_apuntes` |
| `agente_reiki` | `agente_tomas` | `principios_reiki`, `posiciones_manos`, `info_simbolo`, `buscar_reiki` (RAG) |
| `agente_cocinachilena` | `agente_cocina` | `listar_recetas`, `ver_receta`, `costear_receta` (SQLite) |
| `agente_meteorologia` | `agente_meteorologo` | `pronostico_hoy`, `pronostico_semana`, `historial_pronostico`, `comparar_pronostico_vs_real` (API real + SQLite) |
| `agente_viajes` | `agente_viajes` | `buscar_vuelos`, `buscar_hoteles`, `buscar_actividades` |
| `agente_administrador` | **NUEVO** | `listar_agentes`, `describir_agente` (conoce TODO el catálogo) |

### Definición estructurada de cada agente

**`agente_machinelearning`** — *IA / Machine Learning.* Hace: recomienda **técnica** de ML, **métricas**
y **modelo** según el problema/tipo de dato; catálogo de modelos en **SQLite**. No hace: no programa,
no entrena, no responde fuera de IA/DS. Deriva: biología → `agente_bioinformatica`.

**`agente_mlbioinformatica`** — *IA/DS aplicada a bioinformática.* Hace: técnica/métricas/modelo de ML
para **datos biológicos** (secuencias, expresión génica, estructuras, variantes); catálogo SQLite;
partición sin fuga por homología. No hace: no entrena ni ejecuta; no interpreta la biología de fondo.
Deriva: biología de fondo → `agente_bioinformatica`.

**`agente_bioinformatica`** — *Bioinformática.* Hace: explica conceptos (BLAST/e-value, FASTA/FASTQ,
UniProt/NCBI), compara herramientas/BD con criterios, diseña **pipelines** paso a paso. No hace: no
ejecuta análisis/scripts, no consulta BD en vivo, no da consejo médico, no responde ML. Deriva: ML →
`agente_mlbioinformatica`.

**`agente_reiki`** — *Reiki (bienestar complementario).* Hace: cinco **principios (Gokai)**, **posiciones
de manos**, **símbolos**, **niveles**; **RAG** sobre documentos de Reiki. No hace: no da consejo médico
ni diagnósticos. Deriva: salud → profesional. **RAG: de emulación local → Redis cloud (§6).**

**`agente_cocinachilena`** — *Recetario chileno con costeo.* Hace: lista recetas chilenas, muestra
ingredientes y **costea** (por ingrediente, total y por persona, en **CLP**) desde SQLite. No hace: no
responde fuera de cocina.

**`agente_meteorologia`** — *Pronóstico del clima REAL de ciudades de Chile (con historial y
verificación).* **Cambio de T2:** deja de ser estático (en T1 eran diccionarios fijos/ficticios) y pasa
a **consulta REAL** vía **Open-Meteo** (gratis, **sin API key**, JSON por lat/lon).
- Hace: pronóstico **de hoy** y de los **próximos 7 días** para **ciudades de Chile** (catálogo
  configurable de ciudades chilenas con sus coordenadas, p. ej. Santiago, Concepción, Valdivia,
  Antofagasta, La Serena, Puerto Montt… ampliable); temperaturas (°C), condiciones, etc. **En español y
  hora de Santiago (`America/Santiago`).**
- **Persistencia en SQLite (nuevo):**
  - **Guarda los pronósticos DIARIAMENTE** (snapshot por ciudad y día, con la fecha de emisión y la
    fecha pronosticada), para poder **consultarlos hacia atrás**.
  - **Guarda también el resultado REAL/observado** (vía Open-Meteo *archive/observado*), para poder
    **comparar lo pronosticado con lo real**.
  - Un **job diario** (systemd timer o scheduler) toma el snapshot de pronósticos y, con el desfase
    correspondiente, registra los observados.
- Herramientas: `pronostico_hoy(ciudad)`, `pronostico_semana(ciudad)` (ambas REALES),
  `historial_pronostico(ciudad, fecha)` (lo que se pronosticó para esa fecha) y
  `comparar_pronostico_vs_real(ciudad, fecha)` (pronosticado vs observado, con la diferencia).
- No hace: no responde fuera de meteorología; para una ciudad sin coordenadas en el catálogo lo dice en
  una frase (y se puede sumar). Degrada con mensaje claro si Open-Meteo no responde (usa lo guardado en
  SQLite como respaldo cuando aplique).

**`agente_viajes`** — *Búsqueda de viajes.* Hace: **vuelos, hoteles y actividades** (SCL, LIM, BOG, EZE)
con precios en CLP. No hace: no gestiona pagos ni seguros.

**`agente_administrador`** — *Administrador / recepción del sistema de agentes (NUEVO).*
- Hace: **conoce las habilidades y características de TODOS los demás agentes** a su cargo y entrega
  **información general, amable y en español** de qué hace cada uno: qué agentes hay, qué puede cada
  uno, qué NO hace, y **a quién conviene preguntarle** según la necesidad del usuario. Da la bienvenida
  y orienta.
- Fuente de verdad: lee el **catálogo/fichas** (`src/fichas.py` + el catálogo del coordinador), **no
  inventa** capacidades; si un agente cambia su ficha, el administrador lo refleja.
- Herramientas: `listar_agentes()` (todos, con una línea de qué hacen) y `describir_agente(nombre)`
  (detalle de uno: funcionalidad, qué hace, qué no hace, cuándo conviene).
- No hace: no responde la consulta especializada él mismo (eso es de cada agente); **orienta y deriva**.
  Para una tarea concreta, indica el agente adecuado (y el coordinador lo enruta).
- **Cuándo se elige:** preguntas **meta/orientación** — "¿qué agentes hay?", "¿qué pueden hacer?",
  "¿con quién hablo para…?", "ayuda", saludo/bienvenida. (Antes esto caía en "ninguno/sin agente"; ahora
  lo atiende el administrador, amablemente.)
- Tono: cordial, claro, en **español de Chile**.

## 4.1 Idioma y zona horaria (obligatorio)

- **TODO en español** (español de Chile): respuestas de los agentes, UI del frontend web, mensajes de la
  API y de error, correos despachados, documentación, README y evidencias.
- **Zona horaria: `America/Santiago` (Santiago de Chile).** Todas las fechas/horas que ve el usuario y
  las referencias temporales de los agentes (p. ej. el **"hoy"** del pronóstico de `agente_meteorologia`,
  los **timestamps** de despachos de correo y de evidencias, las horas que muestra el monitor) van en
  **hora de Santiago** (usar `zoneinfo("America/Santiago")`), **no UTC**. El VPS corre en UTC: convertir
  al mostrar. Los logs internos pueden quedar en UTC pero **rotulándolo**; lo visible al usuario va en
  Santiago.

## 4.2 Presentación y formato de las salidas (obligatorio)

- Las respuestas deben verse **decentes y bien trabajadas**, no texto plano amontonado: usar
  **Markdown/HTML** con **títulos, listas, tablas cuando aplique, texto alineado y énfasis**
  (**negrita**/*cursiva*) donde corresponda — p. ej. resaltar cifras, **unidades** (CLP, °C), nombres
  de agente y pasos de un pipeline. En el **frontend web** se renderiza Markdown; en la **API** se
  devuelve el texto formateado (y, si aporta, una versión estructurada). **Formatear NO altera**
  cifras/unidades/condiciones (fidelidad).

## 5. Infraestructura NUEVA (separada y aislada del Taller 1)

- **Dominios nuevos** (otro link, distinto del T1):
  - App pública (**FastAPI + frontend web de chat**): **`tarea2curso2.etmk.cl`** (reemplaza a
    `coordinador.etmk.cl`).
  - Monitor/backoffice: **`monitortarea2curso2.etmk.cl`**. **Repropósito respecto del T1:** en el T1 el
    monitor trazaba el **puente A2A** (tráfico entrante de los compañeros); en T2 **no hay puente ni
    agentes remotos** (todo local), así que el monitor se **redefine** como **backoffice de operación y
    seguridad**: baneos de **fail2ban**, **log de accesos a FastAPI** (quién/cuándo, 200 vs 401 sin
    exponer la API_KEY), **bitácora de despachos de correo** (§7) e **historial de conversación** (§6).
    Con login propio; no expone agentes.
  - **Los agentes (`langgraph`) NO tienen subdominio** (solo 127.0.0.1).
- **Correo de despacho:** buzón nuevo **`tarea2curso2@etmk.cl`** (lo creo yo en ISPConfig; secreto en
  EnvironmentFile).
- **Servicios systemd NUEVOS** sin colisión (p. ej. `t2c2-langgraph`, `t2c2-api`, `t2c2-web`,
  `t2c2-monitor`, `t2c2-fichas`), `User=web1`, `Restart=always`, `enabled`, PATH absoluto de `uv`,
  `EnvironmentFile`.
- **Publicación:** Website ISPConfig por subdominio + Let's Encrypt + *Redirect* proxy a
  `127.0.0.1:<puerto>`, con **force-HTTPS ANTES del proxy**.
- **Puertos LIBRES** (confirmar en §12): el T1 usa 2024/8790/8793/8794; elegir nuevos sin colisión con
  nada en uso en la VPS.
- **No tocar ni romper** los 5 servicios `agente-*` del T1 ni ningún otro servicio ya en marcha en la VPS.

## 6. Memoria y datos (decisiones nuevas de T2)

- **RAG / memoria semántica → Redis EN LA NUBE.** Transformar la emulación local
  (`InMemoryVectorStore`) a `RedisVectorStore` apuntando a un **Redis cloud**; la **URL me la entregará
  el usuario** → implementar cuando llegue. Verificar que soporta **RediSearch** (lo exige
  `langchain-redis`). Mantener el backend local solo como fallback de desarrollo (`RAG_BACKEND=local|redis`).
- **Memoria de LARGO PLAZO → SQLite.** Persistir: (a) **historial de conversación** por usuario/sesión;
  (b) **destinatarios registrados** (§7); (c) **bitácora de despachos**; (d) **pronósticos del clima
  diarios** y (e) **observados reales** (de `agente_meteorologia`, para consulta histórica y
  comparación pronóstico-vs-real). Un **job diario** (systemd timer / scheduler) alimenta (d) y (e).
  Esquema versionado (DDL), datos NO versionados. Rutas/archivo por env; sin rutas absolutas.

## 7. Destinatario autogestionado (interfaz de configuración)

El usuario que quiere **recibir los mensajes** (correo y/o canal avanzado) **se registra en una interfaz
de configuración** de la app (no hardcodeado): ingresa correo (y/o teléfono/handle), queda en **SQLite**,
y el despacho usa esa lista como **allowlist**. Alta, baja, estado, validación, idempotencia. Nunca
enviar fuera de la allowlist.

## 8. Seguridad y acceso (obligatorio por rúbrica + arquitectura §2)

- **Gateway FastAPI con `API_KEY`** (§2): toda invocación de agentes exige API_KEY válida; **demostrar
  acceso PERMITIDO y RECHAZADO** (200 vs 401) **sin** mostrar la API_KEY real.
- **Control de acceso del frontend web**: login/Basic Auth propio; el browser no ve la API_KEY (BFF).
- **Secretos fuera** de frontend, repo, ZIP y capturas. **`.env.example`** con nombres y **valores
  ficticios** (incluye `API_KEY`, `GOOGLE_API_KEY`, `REDIS_URL`, `SMTP_*`, tokens del canal). El
  evaluador usa sus propias credenciales.
- **Acciones con efecto real** (correo y el audio del avatar por voz, §3): **cuentas y destinatarios de
  prueba**; controlar envíos y **costos**; documentar cómo **evitar envíos accidentales** y **detener**
  procesos.
- Portar los **guardrails** del T1: entrada (inyección/jailbreak), salida, **respuesta de agente = dato
  (nunca instrucción)**, allow-list de agentes, autorización por capacidad. Entradas inválidas / fallas
  del proveedor / límites → **mensajes claros**, nunca presentados como éxito.

## 9. Reproducibilidad LOCAL (obligatorio por rúbrica)

- Funciona al **clonar/descomprimir en OTRA carpeta**: **sin rutas absolutas**, sin archivos ocultos no
  entregados. **Excluir** `.venv`, `node_modules`, cachés, `*.sqlite`, credenciales, sesiones.
- Configurar **puertos, direcciones y secretos** por env. Declarar **dependencias externas** (Gemini,
  Redis cloud, el canal avanzado requieren internet/servicios).
- Un evaluador debe **repetir una consulta completa** desde el README (incluye levantar langgraph +
  FastAPI + el frontend/canal, con la API_KEY).

## 10. Evidencias reales (obligatorio por rúbrica)

Capturas de **ejecución LOCAL propia**. Por cada caso, **tabla**: Entorno y fecha (**LOCAL**+fecha),
Solicitud, Resultado esperado, Resultado obtenido, Observaciones. Debe verse: la **solicitud** y la
**respuesta/entrega efectiva** en cada canal (web, correo recibido, mensaje, avatar); el **log** que
relaciona solicitud→**FastAPI**→agente (+A2A); la **prueba de acceso** (con API_KEY = 200, sin/`API_KEY`
inválida = 401, sin exponer la clave). Avatar por voz (§3): **audio/video** o enlace. Ocultar
secretos/datos; distinguir **probado / pendiente / simulado**; no rotular LOCAL como producción.

## 11. Estructura del proyecto (COPIA de `tarea_1_curso_2`, adaptada)

```
tarea_2_curso_2/
├── README.md                     # integrantes/aportes, opción, instalar/probar/detener, límites
├── AGENTS.md / CLAUDE.md         # puntero del repo
├── CONVENCIONES.md               # encabezado de archivos + registro de prompts
├── .env.example                  # API_KEY, GOOGLE_API_KEY, REDIS_URL, SMTP_*, tokens del canal (ficticios)
├── .gitignore                    # .env, .venv, logs/, *.sqlite, node_modules, cachés
├── .python-version · pyproject.toml · requirements.txt · uv.lock
├── langgraph.json                # registra los 8 grafos agente_<funcionalidad> (incl. agente_administrador)
├── src/
│   ├── fichas.py                 # name+description por grafo (renombrados)
│   │
│   │   # ── ESTRUCTURA ESTÁNDAR DE CADA AGENTE (igual que en T1; NO dejar un solo .py) ──
│   │   # Todo agente es un PAQUETE con, como mínimo:
│   │   #   __init__.py · graph.py (construye el StateGraph) · herramientas.py (las tools)
│   │   #   · prompts.py (system/instrucciones)
│   │   # y además su(s) módulo(s) de datos cuando aplique (bd_*.py SQLite, rag.py, etc.).
│   │
│   ├── agente_machinelearning/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── herramientas.py       # recomendar_tecnica, metricas_recomendadas, elegir_modelo, consultar_modelos
│   │   ├── prompts.py
│   │   └── bd_modelos.py         # catálogo de modelos (SQLite)
│   ├── agente_mlbioinformatica/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── herramientas.py       # mismas 4 tools, catálogos biológicos
│   │   ├── prompts.py
│   │   └── bd_modelos.py         # catálogo (SQLite)
│   ├── agente_bioinformatica/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── herramientas.py       # consultar_mis_apuntes
│   │   └── prompts.py
│   ├── agente_reiki/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── herramientas.py       # principios_reiki, posiciones_manos, info_simbolo, buscar_reiki
│   │   ├── prompts.py
│   │   └── rag.py                # RAG → Redis cloud (RedisVectorStore; fallback local)
│   ├── agente_cocinachilena/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── herramientas.py       # listar_recetas, ver_receta, costear_receta
│   │   ├── prompts.py
│   │   └── bd_recetas.py         # recetas + costeo (SQLite)
│   ├── agente_meteorologia/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── herramientas.py       # pronostico_hoy, pronostico_semana, historial_pronostico, comparar_pronostico_vs_real
│   │   ├── prompts.py
│   │   ├── openmeteo.py          # cliente de la API real Open-Meteo (sin key) + catálogo de ciudades de Chile
│   │   └── bd_clima.py           # SQLite: pronósticos diarios + observados reales
│   ├── agente_viajes/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── herramientas.py       # buscar_vuelos, buscar_hoteles, buscar_actividades
│   │   └── prompts.py
│   ├── agente_administrador/     # NUEVO
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── herramientas.py       # listar_agentes, describir_agente (lee el catálogo/fichas)
│   │   └── prompts.py
│   ├── coordinador/              # graph.py (supervisor) · catalogo.py · a2a.py · guardrails.py · auth.py · prompts.py
│   ├── api/                      # NUEVO: FastAPI (app.py, dependencia API_KEY, rutas /consulta /salud /agentes)
│   ├── memoria/                  # NUEVO: SQLite (esquema, historial, destinatarios, despachos)
│   └── canales/                  # NUEVO: web (BFF), correo, y el canal avanzado elegido (voz/avatar)
├── tools/
│   ├── coordinador_web.py        # frontend web de chat (adaptado: habla con FastAPI, BFF con API_KEY)
│   ├── monitor_web.py            # backoffice repropuesto: baneos fail2ban + accesos FastAPI + despachos + historial
│   ├── configurar_fichas.py      # aplica fichas (vigilante en systemd)
│   ├── aplicar_encabezados.py · empaquetar_entrega.py · exportar_pdf.py · guardar_evidencias.py …
├── data/                         # datos de los agentes (reiki/*, catálogos semilla)
├── tests/                        # pytest (ruteo, guardrails, API+API_KEY, acceso, fidelidad)
├── deploy/                       # systemd/*.service (t2c2-*), README, *.env.example, BITACORA
├── evidencias/                   # capturas LOCALES + tablas del §10
├── prompts_ejecutados/           # NN-slug.md (estándar del grupo)
├── respuestas/                   # NN-slug.md (salida completa de cada prompt)
└── entrega/                      # documento-entrega, LEEME, REPOS.txt, zip
```

## 12. Consideraciones arquitectónicas ya resueltas (heredadas del T1 — mantener)

- **A2A nativo de LangGraph:** cada agente es un grafo en `langgraph.json`, publicado por `langgraph
  dev` (solo 127.0.0.1); `assistant_id` vía `POST /assistants/search`; Agent Card en
  `/.well-known/agent-card.json?assistant_id=…`; mensajes en `/a2a/<id>`. **`contextId` = UUID**.
- **Coordinador/supervisor (StateGraph):** `guardia_entrada → enrutar (Gemini, salida estructurada
  `Decision{agente,motivo}`) → consultar | sin_agente → guardia_salida`. Estado: `messages, elegido,
  motivo, respuesta, origen, bloqueado, ruta`. Normaliza el nombre elegido.
- **Catálogo desde entorno** (`A2A_GRAFOS_LOCALES`); **en T2 todos LOCALES** (sin `URLS_AGENTES`).
- **Guardrails:** entrada, salida, **respuesta del agente = DATO** (`[Nombre] …`, nunca se ejecuta),
  allow-list, autorización por capacidad.
- **Fidelidad:** no se alteran cifras/unidades/condiciones; pedir datos faltantes antes de concluir.
- **Modelo:** Gemini (`gemini-3.5-flash-lite`) vía `langchain-google-genai`; `GOOGLE_API_KEY` solo en
  `.env`.
- **Fichas (Agent Card):** `name`+`description` por grafo (`src/fichas.py`), aplicadas con `PATCH
  /assistants/<id>` (`configurar_fichas.py`); `langgraph dev` recarga en caliente y las BORRA →
  servicio **vigilante** (`--vigilar`) que las re-aplica.
- **RAG (Reiki):** `RedisVectorStore` (requiere **RediSearch**) o `InMemoryVectorStore`; embeddings
  Gemini (`models/gemini-embedding-001`); índice persistido. **En T2 → Redis cloud.**
- **Despliegue VPS:** `systemd` (`enabled`, `Restart=always`, `ExecStartPre` espera a langgraph),
  **Apache reverse proxy + Let's Encrypt**, **force-HTTPS antes del proxy**, **secretos en `/etc/*.env`**,
  **`sys.path` incluye el raíz**, **PATH absoluto de `uv`** (SSH no interactivo).
- **Seguridad del servidor:** MySQL local, firewall acotado, FTP off, Dovecot TLS, **fail2ban** (jail de
  escaneos que registra baneos en el **monitor repropuesto**, §5), kernel/sysctl/SSH endurecidos.
- **Puente A2A del T1 → NO se porta a T2.** En el T1 había un `puente_a2a` + servicio `agente-puente` +
  su monitor para el **tráfico A2A entrante de compañeros**. En T2 **todos los agentes son locales (sin
  remotos)**, así que **no hay puente**; el monitor se **reaprovecha** como backoffice de operación y
  seguridad (§5).
- **Correo:** SPF/DKIM/DMARC **PASS**; buzón dedicado; **nunca auto-envío** desde respuestas de agentes;
  allowlist.
- **Empaquetado/reproducibilidad:** `empaquetar_entrega.py`, encabezados idempotentes
  (`aplicar_encabezados.py`), export PDF.

## 13. Estándar del grupo (seguir SIEMPRE)

- **Encabezado de grupo** en todo archivo que admita comentarios: Archivo, Objetivo, `Grupo del curso:
  Fabio Durán - Gustavo Reyes - Ezequiel Muñoz`, `Creación` y `Última modificación` (`yyyymmdd HHMM`).
  En frontmatter YAML va DENTRO como comentarios. Lo mantiene `tools/aplicar_encabezados.py`.
- **Registro de prompts:** cada prompt → `prompts_ejecutados/NN-slug.md` y su salida completa →
  `respuestas/NN-slug.md` (mismo número, desde **01** en este repo). La respuesta guarda archivos
  tocados + salida real + estado + pendientes.
- **Commits** en español, terminando con `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`;
  **push tras cada paso**. Rama `main`.

## 14. Restricciones duras

1. **EVALÚA EL ESPACIO/RECURSOS DE LA VPS ANTES DE CREAR NADA ALLÁ** (RAM, disco, puertos). El VPS es
   chico (**≈3.8 GB RAM, sin swap, 2 CPU**) y ya corre los 5 servicios del T1 (entre otros). **No romper
   nada.** Si no cabe, avísame con alternativas.
2. **No incluir secretos reales** en repo/ZIP/capturas. Cuentas de prueba para acciones reales.
3. **No modificar producción automáticamente ante un fallo:** informar y pedir aprobación.
4. Redis cloud: la URL llega después. SQLite para largo plazo. La **`API_KEY`** la define el usuario en
   el `.env`.

## 15. Decisiones abiertas (plantéamelas en el plan)

- **Integración avanzada (opción 3): YA DECIDIDA** → **avatar conversacional por VOZ en el sitio, por
  etapas** (A = voz con Web Speech API, base obligatoria; B = avatar 2D condicional a que A funcione;
  C = avatar realista con lip-sync, opcional de pago). Ver §3. *(No re-preguntar cuál; sí plantear el
  plan de la Etapa A.)*
- **Nombres finales** de los agentes (confirmar §4).
- **Puertos y nombres de servicios** systemd nuevos.
- (Pendiente del usuario) **URL del Redis cloud** y **`API_KEY`** (vía privada). El canal avanzado
  decidido (avatar por **voz**, Etapas A/B) es **gratis y sin credenciales**; solo la **Etapa C**
  (avatar realista de pago) requeriría la **key del SaaS de avatar**, y únicamente si se aborda.

## 16. Primeros pasos (en orden, con validación)

1. **Evaluar la VPS** (RAM/disco/puertos) → decir si cabe y proponer puertos/servicios. *(No crear nada.)*
2. **Crear el repo `tarea_2_curso_2`** (estructura §11): copiar los agentes **renombrados**
   `agente_<funcionalidad>` (TODO local), coordinador, guardrails, `langgraph.json`, `fichas.py`,
   convenciones, `.env.example` (con `API_KEY`), `.gitignore`, encabezados, `prompts_ejecutados/` y
   `respuestas/`.
3. **Backend FastAPI (§2)**: endpoints + **dependencia que valida `API_KEY`** + wrapper del coordinador.
4. **Plan de las 3 implementaciones** (FastAPI, web+correo, avanzada). La opción 3 **ya está decidida**
   (avatar por voz, §3): entregar el **plan de la Etapa A** (voz con Web Speech API, endpoints FastAPI,
   UI, permisos/errores) y dejar B/C consignadas como siguientes/opcionales.
5. **Esquema SQLite** (historial + destinatarios + despachos) y **punto de enchufe del Redis cloud**.
6. Entregarme el plan para **validarlo antes de ejecutar**. **No desplegar ni tocar la VPS sin OK.**

---

**Primer pedido al arrancar:** «Lee `PROMPT_INICIAL_TAREA2.md`. (1) Evalúa recursos de la VPS; (2)
propón la estructura del repo `tarea_2_curso_2` con los agentes renombrados `agente_<funcionalidad>`
TODO local; (3) dame el plan de las 3 implementaciones sobre el **gateway FastAPI protegido por
`API_KEY`**; la integración avanzada **ya está decidida** (avatar por VOZ, §3) → entrégame el **plan de
la Etapa A** (voz con Web Speech API) y deja B/C consignadas; (4) el esquema SQLite + enchufe del Redis
cloud. No crees nada en la VPS ni despliegues: espero tu plan para validarlo.»
