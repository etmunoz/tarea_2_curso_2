<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_045.md`  
> **Objetivo:** Solicitud de script asíncrono para descubrir las tools del MCP Meteosource.  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261122 0000 · **Última modificación:** 20261122 0000
<!--/encabezado-grupo-->

# Prompt 045

Crear `scripts/descubre_mcp.py` reutilizando exclusivamente
`src/integraciones/mcp_langchain.py` y `ClienteMCP.conectar_meteosource()`.

El script debe:

- Ser asíncrono y ejecutarse con `asyncio.run`.
- Descubrir las herramientas mediante `list_tools()`.
- Mostrar una tabla ordenada por nombre con nombre, primera línea de descripción y argumentos con tipo.
- Leer la configuración MCP del entorno sin exponer el token.
- Manejar una URL no disponible sin stack trace.
- Incluir una prueba offline del formato de salida.
