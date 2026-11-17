<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_013.md`  
> **Objetivo:** 013 · Publicación con proxy (ISPConfig) de los subdominios y verificación pública por HTTPS  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1910 · **Última modificación:** 20261117 1910
<!--/encabezado-grupo-->

# 013 · Publicación con proxy + verificación pública

**Pedido del usuario (verbatim):**

> «nos falta configurar los proxy»
> «dame el paso a paso de … publicar con proxy»

**Alcance:**
- Publicar los backends locales por **subdominio con proxy inverso** en ISPConfig (Apache), con
  **Let's Encrypt** y **force-HTTPS antes del proxy**, excluyendo `/.well-known/` para no romper el
  certificado:
  - `tarea2curso2.etmk.cl` → `http://127.0.0.1:8797/` (chat + voz, BFF)
  - `monitortarea2curso2.etmk.cl` → `http://127.0.0.1:8798/` (monitor)
- **Verificar desde fuera** que `http→301→https`, que `https` exige login (401) y que con login entrega
  el contenido (200).

**Notas de diagnóstico de la sesión:**
- El DNS de `etmk.cl` lo sirve un proveedor externo (`ns1/ns2.mydnsservice.com`) con **wildcard**
  `*.etmk.cl → 69.197.134.192`; **no hubo que tocar DNS**. El "Safari no encuentra el servidor" inicial
  fue **caché local** del equipo del usuario.
- Las directivas de Apache van como se detalló (force-HTTPS + `ProxyPass /.well-known !` + `ProxyPass /`).

**Restricción:** la configuración en ISPConfig la hace el usuario (sudo/panel); la verificación la hago
yo desde la VPS contra las URLs públicas.
