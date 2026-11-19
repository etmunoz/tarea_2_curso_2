<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_039.md`  
> **Objetivo:** 039 · Confirmar el nombre la primera vez + health check post-hardening  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1205 · **Última modificación:** 20261119 1205
<!--/encabezado-grupo-->

# 039 · Confirmación de nombre + health check

**Pedidos del usuario (verbatim):**

> «Déjalo así, pero que confirme el nombre la primera vez»
> «chequea que todos los servicios que hemos ido creando estén funcionando ok, puesto que por los
> ataque que está teniendo la máquina he tenido que hacer hardening»

**Alcance:**
1. **Confirmación de nombre** (`src/agente_administrador/prompts.py`): si no hay `nombre` guardado, el
   administrador usa el login como nombre tentativo pero lo **confirma una sola vez** («¿Te llamo Fabio o
   prefieres otro nombre?») y recién ahí lo guarda; si ya está guardado, no vuelve a preguntar.
2. **Health check post-hardening**: se verificó que todo sigue operativo tras el endurecimiento de la
   máquina (ver `evidencias/EVIDENCIAS.md`, Anexo 12): servicios, puertos internos, público/HSTS, egress
   a externos y end-to-end por los 6 agentes. **Sin romper nada.**

**Restricción:** cambio de prompt menor (no toca memoria ni seguridad). El health check es verificación
(no cambia código).
