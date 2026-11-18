<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_019.md`  
> **Objetivo:** 019 · Formatear las salidas del chat (render Markdown), que se veían en crudo  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2102 · **Última modificación:** 20261117 2102
<!--/encabezado-grupo-->

# 019 · Formateo Markdown de las salidas

**Pedido del usuario (verbatim):**

> «lo que te falta de lo que conversamos inicialmente es el formateo de salida, esta como de las chacras»

**Contexto:** el chat mostraba el **Markdown en crudo** (`**negrita**`, `* viñetas`) en vez de
renderizarlo — justo lo que pedía el §4.2 (salidas bien formateadas).

**Alcance:** renderizar Markdown en las burbujas del chat (en el navegador): **negritas/itálicas**,
**listas** (viñetas y numeradas), **títulos**, **código**, saltos de línea — con estilos acordes al
diseño. Se aplica a la respuesta del agente (el mensaje del usuario queda como texto).

**Restricción:** solo `src/canales/web.py` (frontend); el reinicio de `t2c2-web` lo hace el usuario.
