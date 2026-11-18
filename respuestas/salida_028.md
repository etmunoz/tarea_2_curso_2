<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_028.md`  
> **Objetivo:** 028 · Respuesta — Bioinformática real con UniProt en vivo  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1130 · **Última modificación:** 20261118 1130
<!--/encabezado-grupo-->

# 028 · Respuesta — Bioinformática real (UniProt)

**Prompt:** [`../prompts_ejecutados/prompt_028.md`](../prompts_ejecutados/prompt_028.md)

---

## 1. Qué se hizo

- Cliente **UniProt** real (stdlib) y herramienta `consultar_proteina` (accession o gen → accession,
  nombre, gen, organismo, longitud, función, URL). Humano por defecto para símbolos de gen.
- Prompt (RF-08 / RNF-04) y **ficha** actualizados; `consultar_mis_apuntes` se conserva.
- Pruebas nuevas (parseo sin red, regex de accession, degradación): **5 passed**.

## 2. Verificación (cliente en vivo, VPS)

| Consulta | Resultado |
|---|---|
| `TP53` | P04637 · gen TP53 · Homo sapiens · 393 aa |
| `BRCA1` | P38398 · gen BRCA1 · Homo sapiens · 1863 aa |
| `INS` | P01308 · gen INS · Homo sapiens · 110 aa |
| `hemoglobin` | P68871 · gen HBB · Homo sapiens · 147 aa |
| `P38398` (accession) | P38398 · gen BRCA1 · Homo sapiens |

- Se corrigió la relevancia: antes `TP53` (texto libre) traía MDM2; con `gene_exact` + humano por
  defecto trae la proteína correcta.

## 3. Pendiente para activación en vivo

- `sudo systemctl restart t2c2-langgraph` (código nuevo del agente) y `t2c2-fichas` (ficha nueva).
- Verificación por el gateway (consulta de proteína ruteada al Agente de Bioinformática) → evidencias.

## 4. Estado

- ✅ Código + prompt + ficha + tests; desplegado. Bitácora **028**.
