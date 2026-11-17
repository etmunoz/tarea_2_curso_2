<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_003.md`  
> **Objetivo:** 003 · Hacer REAL el agente_meteorologia (Open-Meteo + SQLite), reemplazando los datos estáticos del T1  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1534 · **Última modificación:** 20261117 1534
<!--/encabezado-grupo-->

# 003 · agente_meteorologia REAL (Open-Meteo + SQLite)

**Pedido del usuario (verbatim):**

> «dale con lo que evalúes más razonable»
> «recuerda siempre dejando traza completísima en prompt_ y salida_»

**Evaluación (por qué este paso):** de las tareas pendientes, hacer REAL el `agente_meteorologia` es la
de mayor valor de rúbrica (en el T1 el clima era 100% estático, diccionarios fijos) y, además, la única
que se puede **probar end-to-end sin secretos**: Open-Meteo es gratis y sin API key, y SQLite es stdlib.
FastAPI/coordinador requieren `GOOGLE_API_KEY` (Gemini) para una prueba real, que aún no tenemos.

**Alcance:**
- Reemplazar los datos estáticos por **consulta REAL** a Open-Meteo para **ciudades de Chile**: hoy + 7
  días (temperaturas °C, condición, precipitación), en `America/Santiago`.
- **Persistir en SQLite**: pronósticos diarios (snapshot) y observados reales, para **historial** y
  **comparación pronóstico-vs-real**.
- Mantener el patrón del proyecto (`create_agent`, `HERRAMIENTAS`, `SYSTEM_METEOROLOGO`) y la
  **estructura de paquete** (módulos de datos aparte).
- **Dejar traza completa** en este registro.

**Restricción:** publicar directo en la VPS (web6), sin tocar otros proyectos, sin iniciar servicios
pesados.
