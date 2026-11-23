<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_068.md`
> **Objetivo:** 068 · Arreglo de ruteo — el seguimiento no debe quedarse en un agente que no puede responder
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
> **Creación:** 20261123 1945 · **Última modificación:** 20261123 1945
<!--/encabezado-grupo-->

# 068 · Seguimiento inteligente (re-ruteo cuando cambia el dominio)

**Pedido del usuario (verbatim):**

> «[chat] que clima hace en santiago de Chile → Agente de Meteorología. y en Santiago de Compostela? →
> [Agente de Meteorología] Eso queda fuera de mi área… solo Chile… te sugiero el Agente de Viajes. Por
> qué no lo rutea de inmediato?» … «repara en la VPS lo que haya que reparar para que no pase lo mismo,
> y siempre, prompt, salida y evidencias»

**Diagnóstico:** el coordinador tenía un **atajo determinista** en `enrutar`: si la pregunta era corta
(≤6 palabras) y empezaba como seguimiento (`^¿?\s*y\s+\w`, p. ej. «y en…»), **reutilizaba el agente del
turno anterior sin volver a rutear**. Además el `SYSTEM_SUPERVISOR` reforzaba «mantén el mismo agente»
en seguimientos. Resultado: «y en Santiago de Compostela?» (ciudad de España) se quedaba en
`agente_meteorologia` (solo Chile), que no puede responder y deriva a Viajes. Afecta local y VPS (mismo
código).

**Arreglo (dos capas):**
1. `src/coordinador/graph.py::enrutar`: el agente previo pasa a ser una **PISTA** para el supervisor
   (en un bloque `<pista>`), no un atajo que saltee el ruteo. El supervisor siempre decide.
2. `src/coordinador/prompts.py::SYSTEM_SUPERVISOR`: la regla de seguimiento ahora dice mantener el mismo
   agente **por defecto**, PERO cambiar si el nuevo lugar/entidad/tema corresponde a otro agente; «la
   continuidad nunca debe mandar la pregunta a un agente que no puede responderla».

**Criterio de aceptación:**
- «clima en Santiago de Chile» → Meteorología; «y en Santiago de Compostela?» → **meteo_mcp**.
- Continuidad intacta: «clima en Valdivia» → Meteorología; «¿y mañana?» / «¿y en Concepción?» → Meteorología.

**Alcance:** arreglo en local (verificado), **deploy al VPS** + verificación en vivo, tests del
coordinador en verde, y bitácora (prompt/salida/evidencias).
