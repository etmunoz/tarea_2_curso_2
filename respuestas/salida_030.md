<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_030.md`  
> **Objetivo:** 030 · Respuesta — Cocina chilena con restricciones y estimación nutricional  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1210 · **Última modificación:** 20261118 1210
<!--/encabezado-grupo-->

# 030 · Respuesta — Cocina (restricciones + nutrición)

**Prompt:** [`../prompts_ejecutados/prompt_030.md`](../prompts_ejecutados/prompt_030.md)

---

## 1. Qué se hizo

- `recomendar_recetas(restriccion)`: vegetariano / vegano / sin gluten / económica, **derivado de los
  ingredientes**, ordenado por costo por persona.
- `info_nutricional(nombre)`: kcal total y por persona (estimación aproximada, con disclaimer).
- Prompt + ficha + 4 tests nuevos (**9 passed** en `test_bd_recetas.py`).

## 2. Verificación (funciones, VPS)

- **Vegetarianas**: Pebre, Arroz graneado, Mote con huesillo, Sopaipillas, Leche asada, Ensalada chilena…
  (excluye correctamente las que llevan carne/pescado).
- **Económicas (≤1500/persona)**: Pebre (211), Arroz graneado (298), Mote con huesillo (372),
  Sopaipillas (403).
- **Nutrición Cazuela de vacuno (4p)**: ~1879 kcal total, ~470 kcal/persona + nota de estimación.

## 3. Verificación en vivo (gateway, tras reiniciar)

- **"recetas vegetarianas y económicas"** → Agente de Cocina Chilena: Pebre $211, Arroz graneado $298…
  (tool `recomendar_recetas`, ordenado por costo por persona).
- **"calorías del pastel de choclo por persona"** → Agente de Cocina Chilena: ~686 kcal/persona con
  nota de estimación aproximada (tool `info_nutricional`).

## 4. Estado

- ✅ Código + prompt + ficha + tests; desplegado y **verificado en producción**. Bitácora **030**.
