<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_008.md`  
> **Objetivo:** 008 · Monitor/backoffice repropuesto (t2c2-monitor, :8798): accesos al gateway, despachos, destinatarios e historial  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1629 · **Última modificación:** 20261117 1629
<!--/encabezado-grupo-->

# 008 · Monitor/backoffice repropuesto (:8798)

**Pedido del usuario (verbatim):**

> «dale con el registro 008»

(Continuación del plan: el monitor que quedó pendiente en el registro 007.)

**Alcance:**
- El monitor del T1 trazaba el **puente A2A** (tráfico de compañeros), inexistente en T2. Se
  **repropone** como **backoffice de operación** que muestra lo que web6 sí puede leer:
  - **Accesos al gateway FastAPI** (permitidos vs rechazados, 200/401) — para la evidencia de seguridad.
  - **Bitácora de despachos** de correo.
  - **Allowlist de destinatarios**.
  - **Historial de conversación** reciente.
- Para alimentarlo, agregar al gateway un **middleware de logging de accesos** (tabla `accesos` en
  `src/memoria`, sin guardar la clave; solo si venía o no).
- Crear el **unit `t2c2-monitor.service`** (:8798) y añadir `MONITOR_*` al env.
- Los **baneos de fail2ban** requieren administrador → quedan como **hook del servidor**, documentado.

**Criterio de verificación:** generar accesos reales (200/401) contra el gateway y comprobar que el
monitor los muestra (resumen + tabla). Todo sin secretos (stdlib + FastAPI, sin Gemini).

**Restricción:** publicar directo en la VPS (web6); servicios solo transitorios para la prueba; sin
tocar otros proyectos.
