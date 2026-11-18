<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_031.md`  
> **Objetivo:** 031 · Enriquecer las fichas de todos los agentes para mejorar el ruteo del supervisor  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1215 · **Última modificación:** 20261118 1215
<!--/encabezado-grupo-->

# 031 · Fichas de todos los agentes

**Pedido del usuario (verbatim):**

> Mejora **#2** acordada: «Enriquecer fichas de todos» (mejor ruteo del supervisor). Se hace al final
> para reflejar las capacidades nuevas de los agentes 1, 3 y 4.

**Alcance (`src/fichas.py`):**
- **reiki**: recomienda terapias complementarias por objetivo (registro 027).
- **bioinformatica**: CONSULTA UniProt EN VIVO (registro 028).
- **mlbioinformatica**: arma PIPELINES de bio-ML de punta a punta (registro 029).
- **cocinachilena**: recomienda por restricción + estimación nutricional (registro 030).
- **machinelearning**: aclara que es ML/DS general (datos tabulares) y deriva el **ML sobre datos
  biológicos** a `agente_mlbioinformatica` (antes solo mencionaba bioinformatica) → mejora la separación
  entre ambos.
- **viajes**: agrega **actividades** (tool existente) y marca los datos como de demostración.
- **meteorologia** y **administrador**: ya correctas; sin cambios.

**Nota de arquitectura:** una ficha pobre rompe el ruteo (lo vimos con reiki/cefalea, registro 027).
Las fichas son lo que lee el supervisor (`card_conocida` → descripción), con caché de 120 s en `t2c2-api`.

**Restricción:** las fichas describen capacidades reales; se aplican con `tools/configurar_fichas.py` y
el vigilante `t2c2-fichas` las re-aplica.
