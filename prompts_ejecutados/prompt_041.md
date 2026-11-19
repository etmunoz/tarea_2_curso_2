<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_041.md`  
> **Objetivo:** 041 · Pruebas en producción mezclando dominios de agentes  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 · **Última modificación:** 20261119
<!--/encabezado-grupo-->

# 041 · Pruebas de mezcla de dominios en producción

**Pedido del usuario (verbatim):**

> «El commit ya fue realizado y ya está aplicado el merge y está aplicado en el máster. Ve al sitio en
> producción y aplica pruebas sobre las reglas. Prueba mezclar el conceptos de los agentes, por ejemplo
> dame el tiempo de la proteina C0SPC1 para la venta de una pose de reiki. Haz este tipo de pruebas»

**Alcance:** solo verificación (no cambia código). 16 consultas a `POST /api/consulta` en
`https://tarea2curso2.etmk.cl/` con el usuario `fabio`: 12 en sesiones nuevas (una por prompt) y 1
sesión de 4 turnos. Resultados en [`../respuestas/salida_041.md`](../respuestas/salida_041.md) y detalle en
[`../evidencias/pruebas-mezcla.md`](../evidencias/pruebas-mezcla.md).
