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

## 3. Verificación en vivo (gateway, tras reiniciar)

- **"¿Qué función tiene TP53 humana? Accession y URL"** → Agente de Bioinformática:
  *"…actúa como factor de transcripción… Accession: `P04637` · URL: uniprot.org/uniprotkb/P04637"*.
- **"Dame datos de la proteína BRCA1"** → Agente de Bioinformática: P38398, 1863 aa, función oficial.
- Ruteo: `guardia_entrada → supervisor → agente_local → guardia_salida`. Datos **en vivo** de UniProt.

## 4. Estado

- ✅ Código + prompt + ficha + tests; desplegado y **verificado en producción**. Bitácora **028**.
