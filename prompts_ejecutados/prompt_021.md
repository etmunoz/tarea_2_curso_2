<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_021.md`  
> **Objetivo:** 021 · Probar prompt injection contra el sistema y dejar las evidencias  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2203 · **Última modificación:** 20261117 2203
<!--/encabezado-grupo-->

# 021 · Pruebas de prompt injection

**Pedido del usuario (verbatim):**

> «faltaría que pruebes prompt inyection y que dejes las evidencias.»

**Alcance:** ejecutar ataques reales de **prompt injection** contra el gateway (`POST /consulta`) y
comprobar las defensas: guardrail de entrada (anti inyección/jailbreak), ruteo controlado, "la consulta
del usuario es DATO, no instrucción", y que los agentes **no filtran secretos**. Dejar las evidencias.

**Vectores probados:** (1) override de instrucciones, (2) exfiltración de secretos (API_KEY/.env),
(3) autoridad falsa + extracción del prompt de sistema, (4) instrucción embebida en una consulta
legítima, (5) jailbreak de persona sin filtros.

**Restricción:** pruebas de seguridad defensivas sobre el propio sistema; se documentan los resultados.
