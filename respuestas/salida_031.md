<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_031.md`  
> **Objetivo:** 031 · Respuesta — fichas de todos los agentes enriquecidas  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1215 · **Última modificación:** 20261118 1215
<!--/encabezado-grupo-->

# 031 · Respuesta — Fichas de todos

**Prompt:** [`../prompts_ejecutados/prompt_031.md`](../prompts_ejecutados/prompt_031.md)

---

## 1. Qué se hizo

Se revisaron las 8 fichas (`src/fichas.py`) y se aplicaron en vivo con `tools/configurar_fichas.py`
(las 8 `✓`). Cambios:

| Agente | Cambio en la ficha |
|---|---|
| reiki | terapias complementarias por objetivo |
| bioinformatica | consulta UniProt EN VIVO |
| mlbioinformatica | arma PIPELINES de bio-ML de punta a punta |
| cocinachilena | restricciones (veg/vegano/sin gluten/económica) + nutrición aprox |
| machinelearning | ML/DS general (tabular); deriva bio-ML a mlbioinformatica |
| viajes | agrega actividades; datos de demostración |
| meteorologia, administrador | sin cambios (ya correctas) |

## 2. Por qué importa

Las fichas son lo que lee el **supervisor** para enrutar (`card_conocida` → descripción, caché 120 s en
`t2c2-api`). Una ficha pobre rompe el ruteo (caso reiki/cefalea, registro 027). Con esto el ruteo entre
agentes parecidos (machinelearning vs mlbioinformatica; bioinformatica) queda bien separado.

## 3. Estado

- ✅ 8 fichas revisadas y aplicadas en vivo. Bitácora **031**.
- La verificación de ruteo end-to-end va junto con las mejoras 029/030 (tras el reinicio).
