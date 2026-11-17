<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_007.md`  
> **Objetivo:** 007 · Units systemd t2c2-* + guía de publicación con proxy, listos para activar con administrator  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1624 · **Última modificación:** 20261117 1624
<!--/encabezado-grupo-->

# 007 · Servicios systemd t2c2-* + guía de publicación

**Pedido del usuario (verbatim):**

> «dale con el registro 007»

(Continuación del plan: dejar el despliegue listo para activar.)

**Alcance:**
- Crear los **units systemd `t2c2-*`** (como `User=web6`, aislados de web1/web5), con puertos nuevos
  en 127.0.0.1: `t2c2-langgraph` (:2025), `t2c2-fichas` (vigilante), `t2c2-api` (:8796),
  `t2c2-web` (:8797).
- Crear la **plantilla del EnvironmentFile** `/etc/t2c2.env` (valores ficticios).
- Escribir la **guía de despliegue y publicación** (`deploy/README-T2.md`): instalación con `sudo`,
  orden de arranque, verificación 200/401, y **publicación por subdominio con proxy** (sin tocar DNS) +
  **force-HTTPS antes del proxy** + Let's Encrypt.
- **Validar la sintaxis** de los units (`systemd-analyze verify`).

**Restricción:** yo **no tengo sudo**; dejo todo como **archivos listos** para que el usuario los active
con `administrator`. El `t2c2-monitor` (:8798) queda **pendiente** de construir su backoffice repropuesto
(registro aparte). Publicar directo en la VPS (web6), sin tocar otros proyectos.
