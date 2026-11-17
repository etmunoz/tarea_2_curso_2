<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_017.md`  
> **Objetivo:** 017 · Historial persistente del chat + voz integrada en la misma página (no en otra)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1954 · **Última modificación:** 20261117 1954
<!--/encabezado-grupo-->

# 017 · Historial persistente + voz integrada en el chat

**Pedido del usuario (verbatim):**

> «al volver no queda la historia de lo que tenía, se borra, creo que el chat por voz debiese tomar en
> la misma página no irse a otra, no se entiende. revisa ese flujo.»

**Alcance:**
1. **Historial persistente:** el chat no guardaba la conversación (en el T1 sí, en `sessionStorage`). Se
   re-incorpora: `historial` por conversación (`t2_hist_<thread>`), se guarda en cada turno y se
   **restaura al cargar** (re-dibuja las burbujas y el último ruteo). "Nueva conversación" lo limpia.
2. **Voz integrada en la MISMA página:** en vez de una página `/voz` aparte, el micrófono va **dentro
   del chat**: botón 🎤 en la caja de texto (dicta al input con STT `es-CL`) + toggle 🔊 en la cabecera
   para que lea las respuestas (TTS). Se quita el enlace del chat hacia `/voz` (la página `/voz` se
   mantiene servida para evidencia de la Etapa A, pero el flujo principal es en el chat).

**Restricción:** solo cambia `src/canales/web.py` (BFF); el reinicio de `t2c2-web` lo hace el usuario
(sudo).
