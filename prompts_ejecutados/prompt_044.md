<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_044.md`  
> **Objetivo:** Solicitud de implementación del adaptador propio MCP 2.3 hacia LangChain/LangGraph.  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261122 0000 · **Última modificación:** 20261122 0000
<!--/encabezado-grupo-->

# Prompt 044

Implementar un adaptador propio entre el SDK oficial `mcp==2.3.0` y LangChain/LangGraph en
`src/integraciones/mcp_langchain.py`, sin usar `langchain-mcp-adapters`.

Requisitos principales:

- Conexión MCP por STDIO y Streamable HTTP.
- URL desde `MCP_SERVER_METEOSOURCE`.
- Token Bearer obtenido usando `MCP_BEARER_TOKEN_ENV_VAR`.
- Conversión de herramientas MCP a `StructuredTool`.
- Operación asíncrona, manejo de errores y cierre correcto de sesiones.
- Ejemplo de integración con LangGraph.
- Pruebas offline y actualización de la arquitectura.
- Ejecutar `pip check`, las pruebas existentes, las nuevas pruebas y una comprobación de importación.
