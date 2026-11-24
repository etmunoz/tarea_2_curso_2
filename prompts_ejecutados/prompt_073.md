<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_073.md`
> **Objetivo:** 073 · Revisar y mergear el PR de Fabio (día de la semana + tests + QA), desplegar y registrar el fix
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
> **Creación:** 20261124 1720 · **Última modificación:** 20261124 1720
<!--/encabezado-grupo-->

# 073 · Merge del PR de Fabio (fix día de la semana) + deploy + registro

> ⚠️ **POSTERIOR A LA ENTREGA.** La entrega ya estaba congelada (ZIP descargado + `main` bloqueada);
> este registro documenta un fix hecho **después**, por trazabilidad. No forma parte del ZIP entregado.

**Pedido del usuario (verbatim):**

> «revisa un PR de Fabio, por favor.» … «desbloquea» … «aplica A, y deja un mensaje del fix en la repo.»

**Contexto:** Fabio dejó la rama `fix/dia-semana-tests` (commit `02c1f85`) con:
- **Fix del día de la semana:** el nombre del día lo calculaba el LLM y a veces erraba (p. ej. «lunes
  24-11-2026» cuando era martes). Se calcula ahora en la herramienta.
- **Suite de tests hermética:** quita `test_consumidor` (importaba `src.consumidor` inexistente),
  arregla `test_interop_a2a`/`test_seguridad_48b` y el fallback que exigía `GOOGLE_API_KEY`.
- **QA integral del sitio en vivo** (`tools/qa_entrega.py` + `evidencias/verificacion-entrega.md`):
  95/96 + E2E 5/5 con las cuentas del evaluador.

**Alcance:** revisar el PR (código + correr la suite), mergear a `main`, desplegar el fix al VPS,
reiniciar los agentes y verificar en vivo que el día de la semana sale correcto; dejar el registro.
`main` estaba bloqueada para la entrega: se desbloquea, se mergea y se vuelve a bloquear.
