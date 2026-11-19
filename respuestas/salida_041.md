<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_041.md`  
> **Objetivo:** 041 · Respuesta — pruebas de mezcla de dominios en producción  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 · **Última modificación:** 20261119
<!--/encabezado-grupo-->

# 041 · Respuesta — Pruebas de mezcla de dominios

**Prompt:** [`../prompts_ejecutados/prompt_041.md`](../prompts_ejecutados/prompt_041.md) · **Detalle:**
[`../evidencias/pruebas-mezcla.md`](../evidencias/pruebas-mezcla.md)

16 consultas en producción: **12 ✅ y 4 ⚠️**, sin errores ni caídas.

**Se cumplen:**
- El supervisor elige un solo agente.
- El administrador sugiere agentes y no los invoca.
- Las guardias bloquean la inyección directa y la inyección con etiquetas.
- `ruta` viene cortada por turno.
- El contexto se mantiene entre turnos.
- No se confirman premisas falsas (reiki y cáncer).
- Bioinformática y Meteorología entregan datos reales.

**Fallan:**
- Viajes **inventa precios** (de un plato y de una sesión de reiki).
- Los especialistas **no derivan** al agente correcto cuando una parte queda fuera de su dominio.

## Arreglos aplicados en el repo local (solo prompts; sin desplegar todavía)

- `src/agente_viajes/prompts.py`: prohíbe estimar precios que no vengan de una herramienta, incluidos los
  rangos «aproximados»; el costo de recetas se deriva a Cocina Chilena.
- `src/agente_{cocinachilena,reiki,bioinformatica,mlbioinformatica,meteorologia,viajes}/prompts.py`:
  cuando una parte queda fuera de su dominio, el agente nombra a cuál del catálogo preguntarle.
- `src/coordinador/prompts.py`: el supervisor elige por la intención de la pregunta, no por un tema
  nombrado de pasada (caso «métrica de ML para el sabor de una cazuela»).

Falta desplegar en la VPS y repetir la batería para confirmarlo en vivo.
