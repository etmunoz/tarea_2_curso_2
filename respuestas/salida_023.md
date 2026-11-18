<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_023.md`  
> **Objetivo:** 023 · Respuesta — flujo local→VPS establecido, script de deploy, .env local y .env.example completo  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2211 · **Última modificación:** 20261117 2211
<!--/encabezado-grupo-->

# 023 · Respuesta — Flujo local → VPS + .env

**Prompt:** [`../prompts_ejecutados/prompt_023.md`](../prompts_ejecutados/prompt_023.md)

---

## 1. Nuevo flujo de trabajo (desde ahora)

El **repo local es la fuente de verdad**:

1. **Editar** en el repo local.
2. **Desplegar** a la VPS: `bash deploy/deploy_local_a_vps.sh` (rsync `local → web6`, excluye `.env`,
   `*.sqlite`, `logs/`, `.venv`, cachés, `.langgraph_api`, `prompts_ejecutados/`, `respuestas/`).
3. **Reiniciar** en la VPS los servicios afectados (sudo / administrator), p. ej.:
   `sudo systemctl restart t2c2-web t2c2-api t2c2-monitor`.
4. **Commit + push** a GitHub.

Verificado que local y VPS estaban en sync (solo difería `CONVENCIONES.md`); el primer deploy del nuevo
flujo ya corrió correctamente.

## 2. `.env` y `.env.example` locales

- **`.env.example`**: versionado y **completado** con las variables que faltaban (`API_BASE`,
  `WEB_HOST/PORT`, `WEB_USUARIOS`, `WEB_ADMIN`, `CLAVE_INICIAL`, `MONITOR_*`, `CONFIG_DB`, `USUARIOS_DB`).
- **`.env`**: creado localmente desde el example; **gitignored** (nunca se commitea). El usuario completa
  los secretos (GOOGLE_API_KEY, API_KEY, WEB/MONITOR/SMTP, CLAVE_INICIAL) — los puede copiar de
  `/etc/t2c2.env`.

## 3. Estado

- ✅ `deploy/deploy_local_a_vps.sh` creado y probado (deploy OK).
- ✅ `.env` local (gitignored) + `.env.example` completo versionado.
- ✅ Bitácora **000–023** en el repo.

## 4. Nota de seguridad

El `.env` real (con secretos) **nunca** se versiona: lo cubre `.gitignore` (`.env`, `*.sqlite`, `logs/`).
En la VPS, la config real sigue en `/etc/t2c2.env` (EnvironmentFile de los servicios), fuera del repo.
