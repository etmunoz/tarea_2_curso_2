<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_013.md`  
> **Objetivo:** 013 · Respuesta — app publicada por HTTPS con proxy y verificada públicamente; monitor pendiente de su proxy  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1910 · **Última modificación:** 20261117 1919
<!--/encabezado-grupo-->

# 013 · Respuesta — Publicación con proxy + verificación pública

**Prompt:** [`../prompts_ejecutados/prompt_013.md`](../prompts_ejecutados/prompt_013.md)

---

## 1. DNS (aclaración)

`etmk.cl` lo resuelve un proveedor externo (`ns1/ns2.mydnsservice.com`) con **wildcard**
`*.etmk.cl → 69.197.134.192`. Verificado por DNS público (8.8.8.8): `tarea2curso2.etmk.cl` y
`monitortarea2curso2.etmk.cl` resuelven. **No hubo que crear registros DNS.** El error inicial
"Safari no encuentra el servidor" fue **caché local** del Mac (se resolvió al refrescar el DNS).

## 2. App publicada — `tarea2curso2.etmk.cl` → :8797 ✅

El usuario creó/configuró el Website con **SSL + Let's Encrypt** y las **directivas de proxy**
(force-HTTPS + exclusión de `/.well-known/` + `ProxyPass` a `127.0.0.1:8797`). **Verificación pública
desde la VPS:**

```
http  → 301 → https://tarea2curso2.etmk.cl/      (force-HTTPS OK)
https sin login → 401                             (Basic Auth del BFF)
https con login → 200                             (entrega el chat)
   contenido: "Sistema de agentes", "Hablar por voz", "api/consulta"
```

→ **La app está en producción por HTTPS**, con login propio (WEB_USER/WEB_PASS) y la API_KEY
server-side (el navegador nunca la ve). Chat en `/` y voz en `/voz`.

## 3. Monitor publicado — `monitortarea2curso2.etmk.cl` → :8798 ✅

El usuario configuró el Website con SSL + Let's Encrypt + las directivas de proxy a `127.0.0.1:8798`.
**Verificación pública desde la VPS:**

```
http  → 301 → https://monitortarea2curso2.etmk.cl/   (force-HTTPS OK)
https sin login → 401                                 (Basic Auth del monitor)
https con login → 200                                 (nuestro monitor)
   contenido: "Monitor de operacion", "Accesos", "Clave Gemini"
```

→ **El monitor está en producción por HTTPS**, con login propio (MONITOR_USER/MONITOR_PASS).

## 4. Estado — PUBLICACIÓN COMPLETA ✅

- ✅ **App** `https://tarea2curso2.etmk.cl/` (chat + voz) verificada end-to-end por HTTPS.
- ✅ **Monitor** `https://monitortarea2curso2.etmk.cl/` verificado por HTTPS.
- ✅ Ambos con **force-HTTPS** (`http→301→https`) y **login** (401 sin credenciales, 200 con ellas).
- ✅ Backend verificado (registro 012): consultas reales ruteando a los agentes; correo real (011).

Las **3 implementaciones** quedan **en producción y verificadas**: FastAPI (API_KEY), web de chat +
correo, y voz (Etapa A) — todas accesibles por sus subdominios públicos.

## 5. Próximos pasos

1. **Evidencias de rúbrica** por la web: capturas de chat, voz, correo recibido, y el 200/401
   (acceso permitido/rechazado) en el monitor.
2. Opcional: **RAG → Redis cloud** (cuando llegue la URL); **Etapa B** (avatar 2D).
