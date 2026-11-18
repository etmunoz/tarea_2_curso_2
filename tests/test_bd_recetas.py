# --8<-- encabezado-grupo
# Archivo: tests/test_bd_recetas.py
# Objetivo: Pruebas de la BD de recetas chilenas y el costeo. Sin API key ni servidor.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261110 2013
# Última modificación: 20261111 2049
# --8<-- fin-encabezado-grupo

"""Pruebas de la BD de recetas chilenas y el costeo. Sin API key ni servidor."""
from src.agente_cocinachilena import bd_recetas
from src.agente_cocinachilena.herramientas import costear_receta, listar_recetas, ver_receta


def test_hay_unas_20_recetas():
    """Prueba: hay unas 20 recetas."""
    bd_recetas.asegurar_bd(forzar=True)
    assert len(listar_recetas.invoke({})) >= 20


def test_ver_receta_trae_ingredientes_con_unidad():
    """Prueba: ver receta trae ingredientes con unidad."""
    r = ver_receta.invoke({"nombre": "Pastel de choclo"})
    assert r["nombre"] == "Pastel de choclo"
    assert all({"ingrediente", "cantidad", "unidad"} <= set(i) for i in r["ingredientes"])


def test_costeo_para_4_personas():
    """Prueba: costeo para 4 personas."""
    r = costear_receta.invoke({"nombre": "Pastel de choclo", "personas": 4})
    # el total es la suma de los costos por ingrediente
    assert r["total_clp"] == round(sum(d["costo_clp"] for d in r["detalle"]))
    assert r["por_persona_clp"] == round(r["total_clp"] / 4)


def test_escala_por_personas():
    """Prueba: escala por personas."""
    base = costear_receta.invoke({"nombre": "Cazuela de vacuno", "personas": 4})["total_clp"]
    doble = costear_receta.invoke({"nombre": "Cazuela de vacuno", "personas": 8})["total_clp"]
    assert abs(doble - 2 * base) <= 2  # el doble de personas ≈ el doble de costo


def test_receta_desconocida():
    """Prueba: receta desconocida."""
    assert "nota" in costear_receta.invoke({"nombre": "sushi"})


def test_clasificar_vegetariano():
    """Prueba: Pebre es vegetariano/vegano/sin gluten; Chorrillana no es vegetariana."""
    from src.agente_cocinachilena import bd_recetas
    assert bd_recetas.clasificar("Pebre")["vegetariano"] is True
    assert bd_recetas.clasificar("Chorrillana")["vegetariano"] is False


def test_recetas_por_restriccion_vegana():
    """Prueba: la recomendación vegana no incluye recetas con carne/huevo/leche."""
    from src.agente_cocinachilena import bd_recetas
    r = bd_recetas.recetas_por_restriccion("vegano")
    nombres = {x["receta"] for x in r["recetas"]}
    assert nombres and "Chorrillana" not in nombres and "Leche asada" not in nombres


def test_info_nutricional_aprox():
    """Prueba: la estimación nutricional entrega kcal por persona y la nota de 'aprox'."""
    from src.agente_cocinachilena import bd_recetas
    r = bd_recetas.info_nutricional("Cazuela de vacuno", personas=4)
    assert r["kcal_por_persona_aprox"] > 0 and "aproximada" in r["nota"].lower()


def test_restriccion_desconocida():
    """Prueba: una restricción no soportada devuelve nota con las válidas."""
    from src.agente_cocinachilena import bd_recetas
    r = bd_recetas.recetas_por_restriccion("kosher")
    assert "nota" in r and "vegetariano" in r["nota"]
