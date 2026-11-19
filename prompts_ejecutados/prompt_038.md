<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_038.md`  
> **Objetivo:** 038 · Perfil: idioma preferido (es por defecto) y forma de saludar del usuario  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1140 · **Última modificación:** 20261119 1140
<!--/encabezado-grupo-->

# 038 · Idioma preferido y forma de saludar

**Pedido del usuario (verbatim):**

> «Agrégale el idioma preferido al perfil, que debiese ser sólo español. Pero el usuario puede que le
> guste conversar en otro idioma, le permites, pero que no confunda. Si le gusta saludar de una forma,
> replicas esa forma de saludar.»

**Alcance:**
1. **Perfil ampliado** (`src/memoria/bd.py`): la tabla `perfiles` suma columnas `idioma` y `saludo`
   (migración tolerante con `ALTER TABLE` para la BD existente). Funciones `guardar_perfil`/
   `obtener_perfil` (actualizan solo los campos provistos); `guardar_nombre`/`obtener_nombre` quedan como
   atajos de compatibilidad.
2. **Herramientas** (`src/agente_administrador/herramientas.py`): `preferencias_usuario(usuario)` →
   {nombre, idioma, saludo}; `recordar_preferencias(usuario, nombre?, idioma?, saludo?)` (reemplazan a
   `nombre_usuario`/`recordar_nombre`).
3. **Prompt**: idioma por defecto **español**; responde en el idioma de la persona de forma
   **consistente** (sin mezclar); si escribe/pide otro idioma, lo usa y lo guarda; ante la duda, español.
   Si la persona saluda con una forma propia («wena», «¡buenas!», «hey»), **replica** ese saludo y lo
   guarda, combinándolo con la franja horaria.
4. **Tests**: nombre/idioma/saludo guardados y recuperados por separado.

**Restricción:** español por defecto; el idioma alternativo se mantiene consistente y durable (perfil
SQLite, coherente con ADR-0001). No mezclar idiomas en una misma respuesta.
