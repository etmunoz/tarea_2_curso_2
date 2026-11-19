<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_042.md`  
> **Objetivo:** 042 · Merge de la rama de Fabio (mezcla de dominios) + verificación en vivo  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1300 · **Última modificación:** 20261119 1300
<!--/encabezado-grupo-->

# 042 · Merge registro 041 + verificación

**Pedido del usuario (verbatim):**

> «revisa el PR de Fabio que dejó hace poco»
> «avanza con el merge + deploy + verificación en vivo»

**Alcance:**
1. **Revisión** de la rama `fix/prompts-mezcla-dominios` (registro 041 de Fabio): cambios **solo de
   prompts** (6 agentes + coordinador), mergeable (fast-forward desde `163ca09`), sin conflictos.
2. **Merge** a `main` (`9b6f88e`), **deploy** y **restart** (`t2c2-langgraph` + `t2c2-api`).
3. **Verificación en vivo** de los 4 casos ⚠️ que Fabio detectó (ver `evidencias/pruebas-mezcla.md`,
   sección de verificación post-merge).

**Qué corrige el registro 041 (de Fabio):**
- Viajes **ya no inventa precios** (prohíbe estimar precios sin herramienta; deriva costo de recetas a
  Cocina).
- Los **especialistas derivan** al agente correcto cuando una parte queda fuera de su dominio.
- El **supervisor** elige por la **intención**, no por un tema nombrado de pasada.

**Restricción:** solo prompts (sin lógica); 162 tests verdes; verificación en producción.
