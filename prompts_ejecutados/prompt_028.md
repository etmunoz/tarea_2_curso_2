<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_028.md`  
> **Objetivo:** 028 · Agente de Bioinformática REAL: consulta UniProt en vivo  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1130 · **Última modificación:** 20261118 1130
<!--/encabezado-grupo-->

# 028 · Bioinformática real (UniProt en vivo)

**Pedido del usuario (verbatim):**

> «trabajemos en el resto de los agentes, qué sugieres de mejorar» → se acordaron 4 mejoras;
> esta es la **#1**: «Bioinformática real (UniProt)».

**Alcance:**
1. **`src/agente_bioinformatica/uniprot.py`** (nuevo): cliente REST de UniProt con stdlib (urllib),
   sin API key. `buscar(consulta)` acepta accession (P04637) o nombre/gen (TP53); para símbolos de
   gen usa `gene_exact` con **humano (9606) por defecto** y fallback a cualquier organismo; parseo
   (`_parsear`) separado de la red para testear sin internet.
2. **`herramientas.py`**: herramienta `consultar_proteina(consulta)` (UniProt en vivo) + se conserva
   `consultar_mis_apuntes`. Degrada con nota si la base no responde o no encuentra.
3. **`prompts.py`**: RF-08 (consulta en vivo, cita accession+URL, dato de la herramienta no de memoria);
   RNF-04 ajustado (ahora puede consultar UniProt; sigue sin ejecutar scripts).
4. **`src/fichas.py`**: descripción del `agente_bioinformatica` actualizada (consulta UniProt en vivo)
   para que el supervisor rutee las consultas de proteínas/genes.
5. **`tests/test_agente_bioinformatica.py`** (nuevo): parseo, regex de accession y degradación.

**Restricción:** datos reales desde UniProt (fuente citable), nunca inventados; sin consejo médico.
