<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_040.md`  
> **Objetivo:** 040 · Respuesta — resumen consolidado de la Tarea 2  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1230 · **Última modificación:** 20261119 1230
<!--/encabezado-grupo-->

# 040 · Resumen de la Tarea 2 · Curso 2

**Prompt:** [`../prompts_ejecutados/prompt_040.md`](../prompts_ejecutados/prompt_040.md)

Sistema **multi-agente A2A** desplegado y en producción en la VPS (`web6`), con gateway único
protegido, canal web multiusuario, correo, monitor y persistencia. Publicado en
`https://tarea2curso2.etmk.cl` (monitor en `https://monitortarea2curso2.etmk.cl`).

---

## 1. Arquitectura (qué hay)

```
[web chat + voz]  →  BFF :8797 (login por sesión)  →  FastAPI :8796 (API_KEY)  →  Coordinador (supervisor)
                                                                                      │ A2A
                                                        langgraph dev :2025  →  8 agentes
Monitor :8798   ·   Memoria/Config/Perfiles SQLite   ·   Redis cloud (RAG)   ·   APIs externas
```

- **Gateway FastAPI** (`t2c2-api`): único acceso a los agentes, protegido por **API_KEY** (401 sin
  clave). Coordinador **supervisor** (`guardia_entrada → enrutar → consultar|sin_agente → guardia_salida`)
  con guardrails de entrada/salida y ruteo por turno.
- **8 agentes A2A** (`t2c2-langgraph`): machinelearning, mlbioinformatica, bioinformatica, reiki,
  cocinachilena, meteorologia, viajes, administrador. Vigilante de fichas (`t2c2-fichas`).
- **BFF web** (`t2c2-web`): chat con diseño del Taller 1, **voz integrada**, **login multiusuario**,
  Markdown. Agrega `X-API-Key`/`X-Usuario` server-side.
- **Monitor** (`t2c2-monitor`): accesos (200/401), despachos, allowlist, eventos de usuario, cuota de
  Gemini y `/config`.
- **Persistencia SQLite**: memoria (conversaciones, destinatarios, despachos, accesos, eventos,
  **perfiles**), config store, usuarios, recetas/clima. **Redis cloud** para el RAG de Reiki.
- Detalle vivo: [`../docs/ARQUITECTURA.md`](../docs/ARQUITECTURA.md) (diagrama técnico + componentes).

## 2. Seguridad

- API_KEY en el gateway; agentes y gateway **solo en 127.0.0.1**; publicación por **proxy + HTTPS**
  (Let's Encrypt) con force-HTTPS y **HSTS**; cabeceras `X-Frame-Options`/`nosniff`/`Referrer-Policy` y
  `Server: t2c2`.
- **Multiusuario** (ezequiel admin; gustavo, fabio, cristobal, jose): PBKDF2+salt, clave inicial única
  con cambio obligatorio, cookie HttpOnly+SameSite=Lax+Secure (8 h), anti-fuerza-bruta; eventos al monitor.
- **Guardrails**: inyección/jailbreak (ES/EN + **leetspeak**), exfiltración de secretos, respuesta de un
  agente tratada como **dato**; correo solo a la **allowlist**.
- **Red-team**: 16 ataques probados; resisten system prompt/claves, etiquetas falsas, SQLi, correo a
  externos, contenido peligroso, etc. (`evidencias/pruebas-prompts.md`, `evidencias/fallos.md`).

## 3. Agentes — estado y fuentes de datos

| Agente | Qué hace | Datos |
|---|---|---|
| meteorologia | clima de **Chile** (hoy/7 días, historial, pronóstico vs real) | **real** Open-Meteo + SQLite |
| reiki | principios, posiciones, símbolos, niveles y **terapias complementarias** por objetivo | **real** RAG Redis + Gemini |
| bioinformatica | proteína/gen (accession, función, longitud, organismo, URL) | **real** UniProt en vivo |
| mlbioinformatica | **pipelines** de ML bio + técnica/métricas/modelo | referencia bio-ML |
| machinelearning | técnica/métricas/modelo de ML general | referencia + SQLite |
| cocinachilena | recetas, costeo CLP, **restricciones** y **nutrición aprox** | reglas + SQLite |
| viajes | destino real (país/moneda/zona horaria), **cambio**, **clima mundial**, Wikipedia | **real** (vuelos/hoteles demo) |
| administrador | recepción «**tarea2curso2**»: saluda por hora de Santiago, recuerda **nombre/idioma/saludo** | perfil SQLite durable |

## 4. Memoria y decisiones

- **Memoria de corto plazo del seguimiento DURABLE** (sobrevive reinicios) vía store SQLite
  (`ultimo_agente` + `agente_previo`); «¿y en Santiago?» mantiene el agente previo.
- **Perfil del usuario** durable: nombre (confirmado la 1ª vez), idioma (español por defecto, otro
  idioma consistente) y forma de saludar (se replica).
- **Decisión ADR-0001**: NO se usa `SqliteSaver` (incompatible con `langgraph 1.2.20`/checkpoint 4.3.1) y
  NO se sube langgraph a 2.x (tocaría todo el runtime A2A). Ver
  [`../docs/decisiones/ADR-0001-memoria-corto-plazo.md`](../docs/decisiones/ADR-0001-memoria-corto-plazo.md).

## 5. Operación

- **Flujo**: editar en el repo local → `deploy/deploy_local_a_vps.sh` (rsync sin secretos) → reiniciar
  `t2c2-*` → commit/push. Secretos en `/etc/t2c2.env` o en el **config store** (sin tocar `/etc`).
- **Egress permitido** documentado (Gemini, Open-Meteo, UniProt, er-api, Wikipedia, Redis) en
  `deploy/README-T2.md` para que el hardening no lo bloquee.
- **Health check post-hardening (2026-11-19): TODO OK** (servicios, puertos, público/HSTS, egress,
  end-to-end). Evidencia: `evidencias/EVIDENCIAS.md` (Anexo 12).

## 6. Hitos de la bitácora (000–039)

- **000–023**: base en VPS (gateway+API_KEY, coordinador, 8 agentes, memoria, monitor, correo, config,
  publicación proxy/HTTPS, multiusuario, diseño T1, voz, RAG Reiki), código al repo, flujo local→VPS.
- **024–025**: RAG Reiki → **Redis cloud**; docs de arquitectura.
- **026–027**: Reiki con **terapias complementarias** + catálogo ampliado (duelo/concentración/cefalea).
- **028–032**: agentes **reales/mejorados** (bioinformática UniProt, ML-bio pipelines, cocina, fichas,
  viajes real).
- **033**: **diagrama arquitectónico técnico vivo** + prompt de mantención.
- **034–035**: **merge de la rama de Fabio** (fallos 1/3/5/6 + red-team) y resolución de **2/4/7**.
- **036**: memoria de corto plazo **durable** + **ADR-0001**.
- **037–039**: **recepción personalizada** (saludo por hora, nombre `tarea2curso2`, nombre/idioma/saludo
  durables, confirmación de nombre), **health check post-hardening** y doc de egress.

## 7. Trazabilidad y pendientes

- Bitácora **000–040** (`prompts_ejecutados/` + `respuestas/`), **Anexos 2–12** de evidencias, ADR-0001,
  diagrama vivo. Todo **commiteado y pusheado** a `main`.
- Backlog: `docs/MEJORAS_FUTURAS.md` (vuelos/hoteles reales con Amadeus; onboarding de correo del
  administrador; índices extra de meteorología; checkpointer nativo si se migra langgraph).

## Estado

- ✅ Sistema **operativo en producción**, seguro, con los 8 agentes verificados y trazabilidad completa.
