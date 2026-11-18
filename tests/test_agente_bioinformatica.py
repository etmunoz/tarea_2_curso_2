# --8<-- encabezado-grupo
# Archivo: tests/test_agente_bioinformatica.py
# Objetivo: Pruebas del agente de bioinformática: apuntes + parseo de UniProt (sin red) + degradación.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261118 1120
# Última modificación: 20261118 1120
# --8<-- fin-encabezado-grupo

"""Pruebas del agente de bioinformática. El parseo de UniProt se prueba con un JSON de ejemplo
(sin internet); la consulta en vivo no se prueba aquí (requiere red)."""
from src.agente_bioinformatica import uniprot
from src.agente_bioinformatica.herramientas import consultar_mis_apuntes, consultar_proteina

# Fragmento representativo de una entrada de UniProt (recortado).
_ENTRADA = {
    "primaryAccession": "P04637",
    "proteinDescription": {"recommendedName": {"fullName": {"value": "Cellular tumor antigen p53"}}},
    "genes": [{"geneName": {"value": "TP53"}}],
    "organism": {"scientificName": "Homo sapiens"},
    "sequence": {"length": 393},
    "comments": [{"commentType": "FUNCTION", "texts": [{"value": "Acts as a tumor suppressor."}]}],
}


def test_parsear_entrada_uniprot():
    """Prueba: parsea accession, gen, organismo, longitud, función y URL."""
    d = uniprot._parsear(_ENTRADA)
    assert d["accession"] == "P04637" and d["gen"] == "TP53"
    assert d["organismo"] == "Homo sapiens" and d["longitud"] == 393
    assert "tumor" in d["funcion"].lower()
    assert d["url"] == "https://www.uniprot.org/uniprotkb/P04637"


def test_regex_accession():
    """Prueba: reconoce un accession válido y descarta un símbolo de gen."""
    assert uniprot._RE_ACCESSION.match("P04637")
    assert not uniprot._RE_ACCESSION.match("TP53")


def test_consultar_proteina_degrada(monkeypatch):
    """Prueba: si UniProt no responde, la herramienta devuelve una nota (no rompe)."""
    def _falla(_consulta):
        raise TimeoutError("sin red")

    monkeypatch.setattr(uniprot, "buscar", _falla)
    r = consultar_proteina.invoke({"consulta": "TP53"})
    assert isinstance(r, dict) and "nota" in r


def test_consultar_proteina_sin_resultado(monkeypatch):
    """Prueba: si UniProt no encuentra nada, devuelve nota orientadora."""
    monkeypatch.setattr(uniprot, "buscar", lambda _c: None)
    r = consultar_proteina.invoke({"consulta": "xyzxyz"})
    assert "nota" in r and "No encontré" in r["nota"]


def test_apuntes_siguen_ok():
    """Prueba: los apuntes siguen respondiendo."""
    r = consultar_mis_apuntes.invoke({"tema": "conceptos"})
    assert "BLAST" in r or "alineamiento" in r.lower()
