<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_010.md`  
> **Objetivo:** 010 · Borrador de /etc/t2c2.env (secretos de app pre-generados) + checklist de activación; intentar reusar el .env del T1  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1815 · **Última modificación:** 20261117 1815
<!--/encabezado-grupo-->

# 010 · Borrador de /etc/t2c2.env + checklist de activación

**Pedido del usuario (verbatim):**

> «Prepara el /etc/t2c2.env borrador y el checklist»
> «copia desde .env de la tarea 1 curso 2, lo que puedas de ahí.»

**Alcance:**
1. Crear un **borrador de `/etc/t2c2.env`** en el home de web6 (`~/t2c2.env.borrador`, `chmod 600`) con
   todo lo no-secreto ya rellenado y las **claves de la app (`API_KEY`, `WEB_PASS`, `MONITOR_PASS`)
   generadas fuertes**; dejar como placeholders solo lo externo (`GOOGLE_API_KEY`, `SMTP_PASS`).
2. Escribir un **checklist de activación** (`deploy/CHECKLIST-ACTIVACION.md`): swap, secretos, servicios,
   verificación 200/401, publicación con proxy, prueba end-to-end y detención.
3. **Reusar lo posible del `.env` del T1** (sobre todo `GOOGLE_API_KEY`).

**Restricción:** sin sudo (no escribo en /etc); el borrador queda en el home para que el usuario lo
instale. No exponer valores de secretos.
