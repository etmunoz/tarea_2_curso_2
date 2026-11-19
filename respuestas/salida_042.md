<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_042.md`  
> **Objetivo:** 042 · Respuesta — merge de la rama de Fabio + verificación en vivo  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1300 · **Última modificación:** 20261119 1300
<!--/encabezado-grupo-->

# 042 · Respuesta — Merge registro 041 + verificación

**Prompt:** [`../prompts_ejecutados/prompt_042.md`](../prompts_ejecutados/prompt_042.md)

---

## 1. Merge

- Rama `fix/prompts-mezcla-dominios` (registro 041 de Fabio) → **mergeada a `main`** (`9b6f88e`),
  fast-forward desde `163ca09`, **sin conflictos**. Solo prompts (6 agentes + coordinador).
- **162 tests** verdes; desplegada y reiniciada (`t2c2-langgraph` + `t2c2-api`).

## 2. Verificación en vivo (los 4 casos ⚠️ de Fabio)

| # | Resultado |
|---|---|
| 2 | viajes: «no tengo el dato del costo… te sugiero Cocina Chilena» — **no inventa** + deriva |
| 7 | viajes: «no tengo el costo de una sesión de reiki… acudir al agente de Reiki» + clima real de Cusco |
| 6 | cocina: da la receta y deriva el clima a **Meteorología** |
| 5 | «métrica de ML para el sabor de una cazuela» → rutea a **Machine Learning** (por intención) |

Detalle: `evidencias/pruebas-mezcla.md` (sección de verificación post-merge).

## 3. Estado

- ✅ Mezcla de dominios resuelta en producción: viajes no inventa precios; especialistas derivan;
  supervisor rutea por intención. Bitácora **000–042**. Todo commiteado y pusheado.
