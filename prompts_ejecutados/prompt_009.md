<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_009.md`  
> **Objetivo:** 009 · Reproducibilidad: README.md del repo + suite de pruebas T2 sin secretos (pytest)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1811 · **Última modificación:** 20261117 1811
<!--/encabezado-grupo-->

# 009 · README + suite de pruebas T2

**Pedido del usuario (verbatim):**

> «dale con el registro 009»

(Continuación del plan: cerrar reproducibilidad §9 y pruebas, que no dependen de secretos.)

**Alcance:**
1. **`README.md`** del repo (reemplaza el copiado del T1): qué es, las 3 implementaciones, arquitectura,
   requisitos, **instalar / levantar / probar / detener**, seguridad y límites (rúbrica §9).
2. **`tests/test_tarea2.py`**: suite **determinista, sin GOOGLE_API_KEY ni red**, que valida las piezas
   nuevas: validación de `API_KEY`, memoria SQLite (allowlist/despachos/accesos/historial), catálogo de
   ciudades y mapeo WMO, persistencia de clima, fichas (8 agentes), herramientas del `agente_administrador`
   y composición/allowlist del correo.

**Criterio de verificación:** `pytest` de la suite nueva en verde.

**Restricción:** publicar directo en la VPS (web6); sin tocar otros proyectos.
