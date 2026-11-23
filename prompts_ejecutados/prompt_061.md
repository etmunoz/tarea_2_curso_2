<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_061.md`  
> **Objetivo:** Eliminar metadatos signature de las respuestas HTTP de FastAPI.  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261122 0000 · **Última modificación:** 20261122 0000
<!--/encabezado-grupo-->

# Prompt 061

Corregir la respuesta de `POST /consulta` para que no entregue `extras: signature`, aplique la
limpieza antes de abandonar el servidor y sea legible directamente con `curl`.
