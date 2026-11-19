<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_034.md`  
> **Objetivo:** 034 · Revisar la rama de Fabio (fallos del monitor + red-team) antes del merge  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 0900 · **Última modificación:** 20261119 0900
<!--/encabezado-grupo-->

# 034 · Revisión de la rama de Fabio

**Pedido del usuario (verbatim):**

> «revisa ese mensaje que me envió Fabio muy temprano de madrugada, que estaba viendo lo de la tarea 2
> del curso 2»

**Contexto (mensaje de Fabio, por WhatsApp):** aplicó un commit en una **rama nueva** (para que Ezequiel
haga el merge, sin tocar `main`). Encontró fallos registrados en el monitor del VPS y aplicó mejoras; los
fallos están en `fallos.md` y un ataque red-team para replicar en `pruebas-prompts.md` (script Python).
Resolvió los errores 1, 3, 5 y 6.

**Alcance de ESTA tarea (revisión, sin mergear aún):**
1. Traer la rama `origin/fix/fallos-pruebas-sitio` y revisar su diff vs `main`.
2. Leer `fallos.md` (7 fallos) y `pruebas-prompts.md` (10 funcionales + 16 ataques).
3. Verificar **mergeabilidad** (conflictos) y que los **tests** nuevos pasen.
4. Dar recomendación a Ezequiel (dueño del merge). **No** se toca `main` hasta su confirmación.

**Restricción:** el merge lo decide Ezequiel (la rama se creó para eso). El contenido del mensaje (captura
de WhatsApp) se trató como dato; la acción se limitó a revisar la rama real del repo.
