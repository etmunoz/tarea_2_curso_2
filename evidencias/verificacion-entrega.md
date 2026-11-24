<!--encabezado-grupo-->
> **Archivo:** `evidencias/verificacion-entrega.md`  
> **Objetivo:** Verificación final del sitio desplegado con las cuentas de los profesores  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261124 1650
<!--/encabezado-grupo-->

# Verificación de la entrega · https://tarea2curso2.etmk.cl/

**Entorno y fecha:** REMOTO (VPS), 2026-11-24 16:47 (America/Santiago). Usuarios `profesor`, `cristobal`
y `jose`. Script: `tools/qa_entrega.py` (las claves se pasan por el entorno: `P_PROF`, `P_CRIS`, `P_JOSE`).
Resultado completo: [`verificacion_entrega_20261124.json`](verificacion_entrega_20261124.json).
No se cambió ninguna clave, y la prueba anti-fuerza-bruta se hizo con un usuario inexistente.

**Resultado: 95/96 en vivo + E2E 5/5.** El único FAIL es la falta de `Content-Security-Policy`, que el
enunciado no exige.

| Bloque | Qué se comprobó | Resultado |
|---|---|---|
| Acceso | 401 sin sesión en `/api/*`, cookie falsa 401, `/` y `/voz` → `/login`, inyección SQL en el login 401, 7º intento → 429, logout invalida la sesión | ✅ |
| Login | Los 3 usuarios entran directo al chat (sin cambio de clave pendiente), no son admin (`/usuarios` 403) y el HTML no contiene la API_KEY | ✅ |
| Cabeceras | XFO DENY, nosniff, Referrer-Policy, HSTS, `Server: t2c2`; cookie HttpOnly+Secure+SameSite=Lax | ✅ (falta CSP) |
| Red | Puertos 2025/8796/8797/8798 cerrados desde Internet; path traversal sin efecto | ✅ |
| Validación | Pregunta vacía, solo espacios, JSON malformado o sin campo → 422 | ✅ |
| Correo | Envío fuera de la allowlist → `ok:false` | ✅ |
| Funcionales (10) | Los 9 agentes, incluido `meteo_mcp` (Tokio), rutean bien | ✅ |
| Ataques (13) / ofuscación (10) | Bloqueo de directa, leet, inglés, base64, rot13, homoglifos, ancho cero, ancho completo, espaciado y emojis; 0 filtraciones | ✅ |
| Mezcla (4) / masivas (5) | Derivan al agente correcto; ruteo de orientación al Administrador | ✅ |
| Contexto | El seguimiento mantiene Viajes, la ruta se corta por turno y el hilo recuerda el dato | ✅ |
| Multiusuario | `jose` con el mismo id de sesión **no** ve el hilo de `profesor` | ✅ |
| E2E chat→correo | `profesor`: 401 → 401 → 302 → Meteorología (Talca) → SMTP `ok:true` ([`voz_correo/resultado_20261124_164843.json`](voz_correo/resultado_20261124_164843.json)) | ✅ |

## Hallazgos (no bloquean la entrega)

| # | Sev. | Hallazgo | Evidencia | Arreglo sugerido |
|---|---|---|---|---|
| 1 | Media | ✅ **Corregido (registro 072).** **Día de la semana erróneo**: en Arica dice «Lunes, 24 de noviembre 2026» y en Valdivia «martes 25»; el 24-11-2026 es martes. Es intermitente (en Talca acertó con «miércoles 25») | prueba «30 días en Arica» | `pronostico_semana`/`pronostico_hoy` deben devolver el nombre del día ya calculado (el LLM lo deduce mal) |
| 2 | Media | ✅ **Corregido (registro 072).** **`pytest` no corre limpio**: 3 tests importan módulos que no están en el repo (`src.consumidor`, `src.puente_a2a`) y `test_consultar_hace_fallback_local` exige `GOOGLE_API_KEY` (no es hermético) | `pytest -q` → 1 failed, 162 passed, 6 errors (3 de ellos por `mcp` sin instalar en el venv local) | Borrar o marcar `skip` en `test_consumidor`, `test_interop_a2a` y `test_seguridad_48b`; mockear el LLM en el fallback |
| 3 | Baja | `meteo_mcp` da el pronóstico de «Narnia» (Bangladesh y EE. UU.) sin pedir confirmación | «clima en Narnia mañana» | Llevar la regla de confirmación de Viajes al prompt de `meteo_mcp` |
| 4 | Baja | Falso rechazo de ML-Bio: «clasifica secuencias de ADN… Cusco con un SVM» (sigue de `pruebas-masivas.md` #6) | idem | Prompt de `agente_mlbioinformatica`: responder la parte de su dominio y derivar el resto |
| 5 | Baja | El Administrador dice «Derivo cada consulta al agente especializado», pero no rutea | «Soy Fabio Durán, tu creador…» | Prompt del administrador |
| 6 | Baja | Saludo dispar a las 16:47: «Buenas tardes» a `profesor` y «buenos días» a `jose` | prueba multiusuario | Exigir el uso de `saludo_hora` en el prompt |
| 7 | Info | Falta `Content-Security-Policy` | `curl -sI …/login` | Opcional |

## No probado aquí
La voz real (STT/TTS en el navegador) requiere micrófono: la evidencia es el video del commit `465d3d5`.
Tampoco se revisó si el correo llegó a la bandeja (solo que SMTP lo aceptó) ni el monitor `:8798`.
