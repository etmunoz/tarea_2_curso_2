<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_023.md`  
> **Objetivo:** 023 · Cambiar el flujo de trabajo a editar en local y desplegar a la VPS; .env y .env.example locales  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2211 · **Última modificación:** 20261117 2211
<!--/encabezado-grupo-->

# 023 · Flujo local → VPS + .env local

**Pedido del usuario (verbatim):**

> «de aquí en adelante edita en local y despliega a la VPS»
> «el .env y en .env.example deben estar localmente»

**Alcance:**
1. **Nuevo flujo:** el repo **local** es la fuente de verdad. Se edita en local → se **despliega a la
   VPS** (`deploy/deploy_local_a_vps.sh`, rsync sin secretos ni bitácora) → se **reinician** los
   servicios afectados (sudo, lo hace el usuario). Verificado: local y VPS estaban en sync (solo difería
   `CONVENCIONES.md`, que se desplegó).
2. **`.env` local:** creado desde `.env.example` (queda **gitignored**, nunca se commitea); el usuario
   completa los secretos (puede copiarlos de `/etc/t2c2.env`).
3. **`.env.example` completado:** se agregaron las variables que faltaban — `API_BASE`, `WEB_HOST/PORT`,
   **`WEB_USUARIOS`/`WEB_ADMIN`/`CLAVE_INICIAL`**, `MONITOR_HOST/PORT/USER/PASS`, `CONFIG_DB`/`USUARIOS_DB`.

**Restricción:** `.env` real nunca al repo (gitignore); los servicios los reinicia el usuario con sudo.
