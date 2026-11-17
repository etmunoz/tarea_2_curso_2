<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_011.md`  
> **Objetivo:** 011 · Configuración web de secretos (GOOGLE_API_KEY, etc.) + aviso por la web cuando se acaban los tokens/cuota de Gemini  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1852 · **Última modificación:** 20261117 1852
<!--/encabezado-grupo-->

# 011 · Config web de claves + aviso de cuota de Gemini

**Pedido del usuario (verbatim):**

> «deja la API de Gemini que se pueda ingresar también alternativamente en una configuración en modo web»
> «y lo otro que indique por la web cuando se acaben los tokens de la clave de gemini.»

(Además, en esta sesión: validar la `GOOGLE_API_KEY` (OK) y **enviar un correo real de prueba** a
etmunoz@gmail.com — recibido con ruta + gráfico del grafo.)

**Alcance:**
1. **Ingreso de secretos por web (alternativo al `.env`):** almacén `src/config` (SQLite) + una página
   `/config` en el monitor para cargar `GOOGLE_API_KEY` (y opcional `API_KEY`, `SMTP_PASS`). Un
   `bootstrap` vuelca esos ajustes al entorno **sin pisar** lo que ya venga del `.env` (el `.env` manda).
   Cableado en los 8 agentes + coordinador + gateway.
2. **Aviso de cuota/tokens de Gemini:** el gateway detecta el error de cuota (429/`RESOURCE_EXHAUSTED`)
   al invocar a los agentes, devuelve un mensaje claro (visible en chat y voz) y **marca el estado**; el
   monitor (panel y `/config`) muestra un **banner** con el estado de la clave; endpoint `GET /estado`.

**Criterio de verificación:** guardar una clave por `/config` y leerla del almacén; `es_cuota` clasifica
el error; el monitor muestra el banner. Todo sin exponer valores.

**Restricción:** publicar directo en la VPS (web6); servicios solo transitorios para la prueba.
