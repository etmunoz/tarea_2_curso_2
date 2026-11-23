<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_066.md`
> **Objetivo:** 066 · Contraste de la entrega contra el enunciado oficial (gap analysis)
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
> **Creación:** 20261123 1800 · **Última modificación:** 20261123 1800
<!--/encabezado-grupo-->

# 066 · Contraste contra lo solicitado — ¿cómo estamos para la entrega?

**Prompt:** [`../prompts_ejecutados/prompt_066.md`](../prompts_ejecutados/prompt_066.md) ·
**Fuente:** `taller_implementacion_agentes_tarea_2_curso_2.pdf` (leído íntegro, 4 páginas).

**Leyenda:** ✅ cumplido y con evidencia · 🟡 hecho pero evidencia/documentación por reforzar ·
❌ falta.

---

## Veredicto en una línea

**Implementación: muy sólida** (entregamos las 3 opciones, no solo una). **Documentación: al día.**
**La brecha real está en las EVIDENCIAS visuales de ejecución LOCAL** (capturas de los canales y una
muestra de voz) y en un detalle de encuadre: casi toda la evidencia está rotulada **VPS/público**,
cuando la **entrega obligatoria es LOCAL** (la nube es el +1). Eso es lo que hay que cerrar antes de
enviar.

---

## 01 · El encargo (elegir al menos una)

| Requisito | Estado | Evidencia / dónde |
|---|---|---|
| Servicio FastAPI con acceso protegido | ✅ | `src/api/app.py`; 200/401 (EVIDENCIAS casos 1–2) |
| A2A y **fidelidad** (datos/cálculos/unidades/supuestos) | ✅ | coordinador supervisor; respuesta remota = **dato** (guardrails); caso 3 (clima real sin alterar cifras) |
| Un canal de atención (web chat propio) | ✅ | `src/canales/web.py`; caso 5 |
| Integración avanzada (voz Etapa A: STT→TTS) | 🟡 | `/voz`; caso 7 — **falta la muestra de audio/video** |
| Entrega obligatoria **local**; nube = +1 | 🟡 | local reproducible en README; evidencia actual es VPS (ver brecha B) |
| Declarar opción elegida / problema / reutilización | ✅ | README → "Opción elegida" (agregado en este registro) |

Entregamos **las 3** implementaciones → excede el "al menos una".

## 02 · Construcción y seguridad

| Requisito | Estado | Evidencia / dónde |
|---|---|---|
| Recorrido completo (solicitud→agente→resultado visible) | ✅ | casos 3–5; `ruta` por turno |
| Varios agentes sin alterar cifras/unidades/condiciones | ✅ | supervisor + guardrail A2A (respuesta = dato, no se reescriben cifras) |
| Pedir datos faltantes antes de concluir | 🟡 | los agentes lo hacen por prompt; **sin caso dedicado** en evidencias |
| Entradas inválidas / fallas del proveedor / límites → mensajes claros (no como éxito) | ✅ | guardia_entrada; "agente no disponible"; aviso de cuota Gemini; `pruebas-*` |
| Control de acceso validado en servidor (clave/token o usuarios) + permitido/rechazado | ✅ | `API_KEY` (401/200) + login multiusuario; casos 1–2, 8 |
| Secretos fuera de frontend/repo/zip/capturas | ✅ | `.gitignore`; `/etc/t2c2.env`; almacén de config; token MCP/`PG_DSN` nunca en repo |
| `.env.example` con nombres y valores ficticios | ✅ | `.env.example`, `deploy/t2c2.env.example` |
| Documentar cómo configurar cuentas/permisos de prueba (el evaluador usa sus credenciales) | 🟡 | README/deploy explican `GOOGLE_API_KEY`/`API_KEY`/login; **conviene una "Guía del evaluador" explícita** |
| Acciones con efectos reales (correo): destinatarios de prueba, control de envíos, cómo evitar accidentes y cómo **detener** | ✅ | correo **solo allowlist**, nunca auto-envío; `systemctl stop` documentado |
| Declarar dependencias externas (internet, Gemini, etc.) | ✅ | README "Límites"; `deploy/README-T2.md` egress |

## 03 · Evidencias reales (aquí está el foco)

| Requisito | Estado | Evidencia / dónde |
|---|---|---|
| Tabla por caso: Entorno+fecha / Solicitud / Esperado / Obtenido / Observaciones | ✅ | `EVIDENCIAS.md` §Tabla de casos (10 casos) |
| Capturas de ejecución que muestren **pedido → ejecución → resultado** | ❌ | solo hay **1 imagen** (`redis_reiki_indice.png`); faltan capturas de chat/correo/monitor |
| Respuesta/entrega en el canal (respuesta web, **correo recibido**, interfaz) | ❌ | casos 5, 6, 8 marcados *(captura)* — pendientes |
| Registro de ejecución que relacione solicitud↔agente↔A2A (ocultando sensibles) | ✅ | `EVIDENCIAS.md` §Evidencia técnica (rutas y respuestas reales) |
| Prueba de control de acceso: autorizado + rechazado, sin mostrar la clave | 🟡 | está en texto (401/200); **falta la captura** |
| Si voz/avatar: **muestra de audio/video** o enlace accesible | ❌ | caso 7 *(audio/video)* — pendiente; "una imagen de la interfaz no basta" |
| Evidencia honesta: datos de prueba, ocultar secretos, distinguir probado/pendiente/simulado, no rotular local como producción | 🟡 | se distingue bien; **pero la evidencia dice "VPS/público"**, y lo obligatorio es LOCAL |

## 04 · Entrega y evaluación

| Requisito | Estado | Evidencia / dónde |
|---|---|---|
| GitHub con acceso docente (privado OK si se concede) o ZIP | 🟡 | repo privado `etmunoz/tarea_2_curso_2`; **falta invitar al evaluador** |
| Código completo + versiones/dependencias + config de ejemplo sin secretos + evidencias | ✅ | `requirements.txt`, `pyproject.toml`, `.env.example`, `evidencias/` |
| README con **integrantes y aportes**, opción elegida, preparación, instalar, iniciar/probar/detener, límites | ✅ | README (integrantes/aportes y opción elegida agregados en este registro) |
| Instrucciones que funcionen al clonar en otra carpeta; sin rutas absolutas; excluir `.venv`/cachés/credenciales | ✅ | README usa rutas relativas; `.gitignore` excluye `.venv`/`*.sqlite`/`logs/` |
| Preparación para despliegue futuro (puertos/direcciones/secretos, qué conservar, servicios externos) | ✅ | `deploy/README-T2.md`, `docs/ARQUITECTURA.md` |
| +1 nube: URL + acceso + funciona sin el PC del estudiante + evidencias del entorno remoto | 🟡 | desplegado en `https://tarea2curso2.etmk.cl/`; sirve para el +1 **si** se entrega acceso + evidencias remotas |

---

## Brechas priorizadas (qué falta para "necesaria y suficiente")

**P1 — bloqueantes de la rúbrica de evidencias (las hace el usuario, en LOCAL):**
- **B-A · Capturas de los canales (LOCAL).** Levantar local (README) y capturar, con fecha y rótulo
  "LOCAL":
  1. Chat web: la **pregunta y la respuesta** en pantalla (`http://127.0.0.1:8797/`).
  2. **Correo recibido** (bandeja) con la ruta + gráfico del grafo al pie.
  3. Acceso **401 y 200** (terminal o panel del monitor) **sin** mostrar la API_KEY.
  4. Monitor: panel de accesos 200/401.
- **B-B · Muestra de voz (LOCAL).** Un **audio o video corto** de `/voz`: se habla, el sistema
  responde y **se escucha** el TTS. (La rúbrica es explícita: una imagen no prueba que se oyó.)
- **B-C · Rótulo LOCAL.** Repetir los casos 1–7 en local y rotularlos **LOCAL** (lo actual es VPS).
  Dejar el VPS como evidencia del **+1** (entorno remoto), no como la entrega base.

**P2 — acceso y encuadre (rápido):**
- **B-D · Acceso del evaluador al repo privado** (invitar al docente en GitHub) — o preparar ZIP.
- **B-E · +1 nube:** si se opta, entregar URL + credencial de prueba (por vía privada) + un par de
  capturas del entorno remoto rotuladas como tal.

**P3 — refuerzos menores (opcionales, suman calidad):**
- **B-F · Caso "pide datos faltantes"**: un ejemplo donde el agente pide un dato antes de concluir.
- **B-G · Guía del evaluador**: media carilla con "clonar → `uv sync` → `.env` → levantar → probar 401/200
  → una consulta", para reproducir sin fricción. (Hoy está disperso en README/deploy.)

## Lo que YA se cerró en este registro (documentación)

- README: **Integrantes y aportes** + **Opción elegida / problema / reutilización** (lo exige §04).
- Esta matriz de contraste como checklist de pre-entrega.

## Estado

- Implementación ✅, documentación ✅. **Pendiente para "suficiente": las evidencias visuales LOCALES
  (P1).** Esta salida es la lista de verificación de pre-entrega. Bitácora **066**, Anexo **17**.
