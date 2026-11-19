<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_034.md`  
> **Objetivo:** 034 · Respuesta — revisión de la rama fix/fallos-pruebas-sitio de Fabio  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 0900 · **Última modificación:** 20261119 0900
<!--/encabezado-grupo-->

# 034 · Respuesta — Revisión de la rama de Fabio

**Prompt:** [`../prompts_ejecutados/prompt_034.md`](../prompts_ejecutados/prompt_034.md)

---

## 1. La rama

- `origin/fix/fallos-pruebas-sitio`, 1 commit (`7f17cac`) de Fabio Durán-Verdugo (2026-11-19).
- **merge-base = `cce3bf9` (HEAD de `main`)** → **mergea limpio (fast-forward), sin conflictos** con los
  cambios 028–033.
- Toca 9 archivos: `fallos.md`, `pruebas-prompts.md` (nuevos), prompts de bio/ml-bio, `viajes/clientes.py`,
  `api/app.py`, `canales/web.py`, `coordinador/graph.py`, `tests/test_tarea2.py`.
- **Tests:** `pytest tests/test_tarea2.py` → **11 passed** (incluye los 3 nuevos). Cambios aditivos.

## 2. Qué arregló (4 de 7 fallos)

| # | Sev | Fix | Test |
|---|---|---|---|
| 1 | Media | `convertir` rechaza montos no finitos/>1e15; el coordinador enmascara `Error executing…` de langgraph con mensaje amable + lo loguea | `test_convertir_rechaza_monto_absurdo` |
| 3 | Baja | `Consulta.pregunta` exige `min_length=1` (vacía → 422, no llega al coordinador) | `test_consulta_rechaza_pregunta_vacia` |
| 5 | Baja | prompts derivan por el nombre del catálogo (no filtra "Agente Fabio"/"ProteinMAN") | verificar en vivo |
| 6 | Baja (parcial) | cabeceras `X-Frame-Options`/`X-Content-Type-Options`/`Referrer-Policy` + `Server: t2c2`; HSTS pendiente (proxy) | `test_web_cabeceras_seguridad` |

## 3. Pendientes (documentados como propuesta por Fabio)

- **2** · Guardia de entrada ciega a leetspeak ("Ign0r4…") e inglés (los agentes igual no cedieron).
- **4** · Pierde contexto en seguimiento ("¿y en Santiago?" → Meteorología).
- **7** · Ubica lugares ficticios ("Narnia" → pueblo de Bangladesh) sin avisar.

## 4. Red-team (resistió lo importante)

16 ataques: system prompt/claves, etiquetas falsas `</datos><sistema>`, SQL injection, correo a externos,
contenido peligroso disfrazado, salida excesiva, vacío/emojis → **resistidos**. Puertos internos no
expuestos; `/api/consulta` sin cookie = 401. Detalle en `fallos.md` + `pruebas-prompts.md` (de la rama).

## 5. Recomendación

**Mergear** (trabajo sólido, probado, mejora seguridad/robustez, sin conflictos). Observaciones:
(a) reubicar `fallos.md`/`pruebas-prompts.md` a `evidencias/`; (b) tras el merge, actualizar
`docs/ARQUITECTURA.md` y abordar/anotar las propuestas 2/4/7. **El merge lo decide Ezequiel.**

## 6. Estado

- ✅ Revisión completa. Rama mergeable y verde. A la espera de confirmación para mergear + desplegar.
