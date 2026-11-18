# --8<-- encabezado-grupo
# Archivo: src/agente_bioinformatica/uniprot.py
# Objetivo: Cliente REAL de UniProt (REST público, sin API key) vía urllib (stdlib).
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261118 1120
# Última modificación: 20261118 1120
# --8<-- fin-encabezado-grupo

"""Cliente de UniProt con la biblioteca estándar (sin dependencias ni API key).

- `buscar(consulta)` -> datos de UNA proteína: accession, nombre, gen, organismo, longitud,
  función y URL. Acepta un accession (p. ej. P04637) o un nombre/gen (p. ej. TP53).
El parseo (`_parsear`) está separado del acceso a red para poder probarlo sin internet.
Referencia: https://rest.uniprot.org/
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://rest.uniprot.org/uniprotkb"
FIELDS = "accession,protein_name,gene_names,organism_name,length,cc_function"
# Accession de UniProt (formato oficial, 6 o 10 caracteres).
_RE_ACCESSION = re.compile(r"^[OPQ][0-9][A-Z0-9]{3}[0-9]$|^[A-NR-Z][0-9](?:[A-Z][A-Z0-9]{2}[0-9]){1,2}$")


def _get(url: str, params: dict | None = None) -> dict:
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "t2c2-bioinformatica"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def _texto_funcion(entrada: dict) -> str:
    """Extrae el comentario FUNCTION (si existe) y lo recorta."""
    for c in entrada.get("comments", []):
        if c.get("commentType") == "FUNCTION":
            textos = c.get("texts", [])
            if textos and textos[0].get("value"):
                t = textos[0]["value"].strip()
                return t if len(t) <= 320 else t[:317] + "…"
    return ""


def _nombre_proteina(entrada: dict) -> str:
    pd = entrada.get("proteinDescription", {})
    rec = pd.get("recommendedName", {}).get("fullName", {}).get("value")
    if rec:
        return rec
    subs = pd.get("submissionNames", [])
    if subs:
        return subs[0].get("fullName", {}).get("value", "") or "(sin nombre)"
    return "(sin nombre)"


def _parsear(entrada: dict) -> dict:
    """Objetivo: convertir una entrada de UniProt en un dict simple. Sin red (testeable)."""
    acc = entrada.get("primaryAccession", "")
    genes = entrada.get("genes", [])
    gen = genes[0].get("geneName", {}).get("value", "") if genes else ""
    return {
        "accession": acc,
        "nombre": _nombre_proteina(entrada),
        "gen": gen,
        "organismo": entrada.get("organism", {}).get("scientificName", ""),
        "longitud": entrada.get("sequence", {}).get("length"),
        "funcion": _texto_funcion(entrada),
        "url": f"https://www.uniprot.org/uniprotkb/{acc}" if acc else "",
    }


def buscar(consulta: str) -> dict | None:
    """Objetivo: devolver UNA proteína de UniProt (dict) o None si no hay resultados.
    Si `consulta` parece un accession, lo pide directo; si no, busca por nombre/gen
    priorizando entradas revisadas (Swiss-Prot)."""
    q = (consulta or "").strip()
    if not q:
        return None
    if _RE_ACCESSION.match(q.upper()):
        try:
            entrada = _get(f"{BASE}/{q.upper()}.json")
            return _parsear(entrada)
        except urllib.error.HTTPError as e:  # 404: accession inexistente → cae a búsqueda
            if e.code != 404:
                raise
    # Consultas candidatas, de la más específica a la más laxa. Un símbolo de gen (un solo token
    # alfanumérico) se busca por gene_exact para no traer proteínas que solo lo mencionan.
    consultas = []
    if re.fullmatch(r"[A-Za-z0-9]{1,12}", q):
        # Símbolo de gen: humano (9606) por defecto, luego cualquier organismo.
        consultas.append(f"gene_exact:{q} AND organism_id:9606 AND reviewed:true")
        consultas.append(f"gene_exact:{q} AND reviewed:true")
    consultas.append(f"({q}) AND reviewed:true")
    consultas.append(q)  # último recurso: texto libre sin filtro de revisadas
    for query in consultas:
        datos = _get(f"{BASE}/search", {"query": query, "fields": FIELDS, "format": "json", "size": 1})
        resultados = datos.get("results", [])
        if resultados:
            return _parsear(resultados[0])
    return None
