<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_015.md`  
> **Objetivo:** 015 · Portar el diseño web del chat al del Taller 1 (aurora + Chat/Ruteo) y confirmar auto-arranque  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1935 · **Última modificación:** 20261117 1935
<!--/encabezado-grupo-->

# 015 · Rediseño del chat (estilo Taller 1) + auto-arranque

**Pedido del usuario (verbatim):**

> «lo que quiero que veas el diseño web de la tarea 1 y el que hiciste de la tarea 2. necesito lo
> cambies por el de la tarea 1.»
> «no te olvides después de eso, el dejar los servicios que se autolevanten … como lo hicimos con la
> tarea1 si es que la VPS se reinicia por algún motivo.»

**Alcance:**
1. **Rediseñar el frontend del chat** (`src/canales/web.py`, `PAGINA`) con el **diseño "moderno" del
   Taller 1**: fondo *aurora*, dos tarjetas (**Chat** + **Ruteo del coordinador**), **chips** de agentes,
   **tema claro/oscuro**, burbujas con avatar, panel de ruteo con pasos (ruta), botones nuevo/voz/salir.
   Adaptado para hablar con **`/api/consulta`** (BFF → FastAPI con API_KEY server-side) en vez de invocar
   el grafo directo.
2. Agregar **`motivo`** a la respuesta de `/consulta` (para el panel de ruteo).
3. **Confirmar el auto-arranque** de los servicios en caso de reboot (como el T1).

**Restricción:** el reinicio de servicios requiere `sudo` (lo hace el usuario); web6 no puede.
