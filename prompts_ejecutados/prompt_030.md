<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_030.md`  
> **Objetivo:** 030 · Cocina chilena: recomendación por restricción + estimación nutricional  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1210 · **Última modificación:** 20261118 1210
<!--/encabezado-grupo-->

# 030 · Cocina chilena (restricciones + nutrición)

**Pedido del usuario (verbatim):**

> Mejora **#4** acordada: «Cocina chilena (nutrición + más recetas + recomendaciones por restricción:
> vegetariano/sin gluten/presupuesto)».

**Alcance:**
1. **`bd_recetas.py`:** clasificación **derivada de los ingredientes** (no etiquetada a mano):
   `CARNICOS`, `ANIMALES`, `CON_GLUTEN`; tabla `KCAL` aproximada por ingrediente. Funciones:
   - `clasificar(nombre)` → {vegetariano, vegano, sin_gluten}.
   - `recetas_por_restriccion(restriccion)` → vegetariano/vegano/sin gluten/económica (costo/persona).
   - `info_nutricional(nombre, personas)` → kcal total y por persona (ESTIMACIÓN, con disclaimer).
2. **`herramientas.py`:** tools `recomendar_recetas(restriccion)` e `info_nutricional(nombre)`.
3. **`prompts.py`:** reglas para usar las tools nuevas; aclara que las kcal son estimación y que no da
   consejo dietético/médico.
4. **`src/fichas.py`:** ficha de cocina ampliada (restricciones + nutrición) para el ruteo.
5. **`tests/test_bd_recetas.py`:** +4 pruebas (clasificar, vegana, nutrición, restricción desconocida).

**Restricción:** nada inventado en lo verificable (restricciones se derivan de los ingredientes; precios
y kcal son estimaciones simuladas y así se declaran). Sin consejo dietético ni médico.
