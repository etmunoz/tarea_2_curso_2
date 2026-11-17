<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_010.md`  
> **Objetivo:** 010 · Respuesta — borrador de /etc/t2c2.env + checklist; el .env del T1 no es legible por web6 (aislamiento)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1815 · **Última modificación:** 20261117 1815
<!--/encabezado-grupo-->

# 010 · Respuesta — Borrador de /etc/t2c2.env + checklist

**Prompt:** [`../prompts_ejecutados/prompt_010.md`](../prompts_ejecutados/prompt_010.md)

> ⚠️ **Método:** publicado **directo en la VPS** (web6). Este `.md` es la bitácora. **El borrador con
> secretos vive solo en el home de web6, NO en el repo.**

---

## 1. Borrador de `/etc/t2c2.env`

Creado en `~/t2c2.env.borrador` (permisos `-rw-------`, solo web6), con:
- **No-secreto ya rellenado:** `MODELO`, `A2A_BASE=:2025`, `A2A_GRAFOS_LOCALES` (los 8), `API_BASE`,
  `WEB_HOST/PORT`, `MONITOR_HOST/PORT`, `RAG_BACKEND=local`, `SMTP_HOST/PORT`, `SMTP_USER`, `MAIL_FROM`,
  `WEB_USER=admin`, `MONITOR_USER=monitor`.
- **Claves de la app generadas fuertes** (no se muestran): `API_KEY` (48), `WEB_PASS` (24),
  `MONITOR_PASS` (24).
- **Placeholders por pegar:** `GOOGLE_API_KEY` y `SMTP_PASS` (este último es del buzón
  `tarea2curso2@etmk.cl`, distinto del T1).

## 2. Checklist de activación

`deploy/CHECKLIST-ACTIVACION.md` (83 líneas): **swap** → **secretos en /etc/t2c2.env** → **instalar/
arrancar los 5 servicios en orden** → **verificación 200/401** → **publicación con proxy (sin DNS) +
force-HTTPS** → **prueba end-to-end (evidencias)** → **detener/reiniciar**.

## 3. Reuso del `.env` del T1

- El `.env` del T1 (`/var/www/clients/client1/web1/home/etmkuseragente/tarea_1_curso_2/.env`) es
  **modo 600, dueño web1** → **web6 NO puede leerlo** (es el aislamiento correcto entre proyectos). La
  copia automática **no fue posible**.
- `SMTP_PASS` del T1 **no aplica**: es del buzón `coordinador@etmk.cl`; en T2 el remitente es
  `tarea2curso2@etmk.cl` (su clave es la que se definió al crear ese buzón en ISPConfig).
- **`GOOGLE_API_KEY` sí es reutilizable.** El usuario puede copiarla al borrador (tiene acceso a web1 /
  administrator) con:
  ```bash
  G=$(sudo grep '^GOOGLE_API_KEY=' /var/www/clients/client1/web1/home/etmkuseragente/tarea_1_curso_2/.env | cut -d= -f2-)
  sed -i "s|^GOOGLE_API_KEY=.*|GOOGLE_API_KEY=$G|" /var/www/clients/client1/web6/home/etmkuseretmk2/t2c2.env.borrador
  ```

## 4. Estado y pendientes

- ✅ Borrador y checklist listos. **No se escribió en /etc** (sin sudo); otros proyectos intactos.
- Pendiente del usuario: pegar/copi­ar `GOOGLE_API_KEY`, pegar `SMTP_PASS` del buzón nuevo, y seguir el
  checklist (swap + servicios + publicación).

## 5. Próximo paso

- Con `GOOGLE_API_KEY` + swap + servicios activos: **prueba end-to-end** (texto, voz, correo, 200/401) y
  captura de **evidencias** para la rúbrica (§10 del prompt_000).
