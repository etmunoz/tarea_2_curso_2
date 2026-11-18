# --8<-- encabezado-grupo
# Archivo: src/agente_cocinachilena/bd_recetas.py
# Objetivo: Base de conocimiento (SQLite) de recetas chilenas clásicas + costeo.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# Creación: 20261110 2013
# Última modificación: 20261111 2049
# --8<-- fin-encabezado-grupo

"""Base de conocimiento (SQLite) de recetas chilenas clásicas + costeo.

Idea clave (pedido del usuario): los **precios se guardan en función de la unidad que
usa la receta**, así NO hay que convertir: el costo por ingrediente es una simple
multiplicación `cantidad × precio_unitario`. Para costear una receta para N personas
se escala la cantidad por `N / porciones_base`.

Tablas:
  recetas(nombre, porciones_base, descripcion)
  ingredientes(nombre, unidad, precio_clp)        -- precio por 1 <unidad> (sin conversión)
  receta_items(receta, ingrediente, cantidad)      -- cantidad en la unidad del ingrediente

La BD se crea y puebla sola la primera vez. Ruta: `data/recetas_cl.sqlite`
(configurable con `BD_RECETAS`). Precios en CLP, aproximados/simulados.
"""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
BD_PATH = Path(os.environ.get("BD_RECETAS", RAIZ / "data" / "recetas_cl.sqlite"))

# ingrediente -> (unidad usada en las recetas, precio CLP por 1 unidad)
INGREDIENTES: dict[str, tuple[str, float]] = {
    "harina": ("g", 1.1), "carne molida": ("g", 8.0), "posta de vacuno": ("g", 9.0),
    "trutro de pollo": ("g", 4.5), "longaniza": ("g", 7.0), "congrio": ("g", 12.0),
    "cebolla": ("unidad", 300.0), "ajo": ("diente", 50.0), "huevo": ("unidad", 200.0),
    "aceite": ("ml", 3.0), "aceitunas": ("unidad", 80.0), "pasas": ("g", 6.0),
    "choclo": ("unidad", 500.0), "albahaca": ("g", 20.0), "zapallo": ("g", 1.5),
    "porotos": ("g", 3.0), "papa": ("g", 1.2), "zanahoria": ("unidad", 200.0),
    "tomate": ("unidad", 350.0), "ají verde": ("unidad", 150.0), "cilantro": ("g", 15.0),
    "pan de completo": ("unidad", 250.0), "vienesa": ("unidad", 300.0), "palta": ("unidad", 800.0),
    "mayonesa": ("g", 5.0), "arroz": ("g", 1.5), "lentejas": ("g", 2.5),
    "pancutras": ("g", 2.0), "leche": ("ml", 1.2), "azúcar": ("g", 1.3),
    "huesillo": ("unidad", 120.0), "mote": ("g", 3.0), "comino": ("g", 30.0),
    "vino tinto": ("ml", 2.0), "manteca": ("g", 4.0), "polvos de hornear": ("g", 20.0),
    "poroto verde": ("g", 3.0),
}

# nombre -> (porciones_base, descripcion, [(ingrediente, cantidad), ...])
RECETAS: dict[str, tuple[int, str, list[tuple[str, float]]]] = {
    "Empanadas de pino": (6, "Empanadas al horno rellenas de pino (carne, cebolla, huevo, aceituna).",
        [("harina", 500), ("carne molida", 300), ("cebolla", 3), ("huevo", 3), ("aceitunas", 6), ("pasas", 30), ("comino", 5), ("aceite", 50)]),
    "Pastel de choclo": (4, "Pastel de choclo con pino de carne y pollo.",
        [("choclo", 6), ("carne molida", 400), ("trutro de pollo", 300), ("cebolla", 2), ("huevo", 3), ("albahaca", 10), ("azúcar", 20)]),
    "Cazuela de vacuno": (4, "Cazuela con posta, papa, zapallo y choclo.",
        [("posta de vacuno", 500), ("papa", 600), ("zapallo", 400), ("choclo", 2), ("zanahoria", 2), ("arroz", 60), ("cilantro", 15)]),
    "Porotos granados": (4, "Porotos con mazamorra de choclo y zapallo.",
        [("porotos", 500), ("zapallo", 300), ("choclo", 2), ("cebolla", 1), ("albahaca", 10)]),
    "Charquicán": (4, "Guiso de carne con papa y zapallo, con huevo frito.",
        [("posta de vacuno", 300), ("papa", 500), ("zapallo", 400), ("cebolla", 1), ("choclo", 1), ("huevo", 4)]),
    "Humitas": (6, "Humitas de choclo molido cocidas en sus hojas.",
        [("choclo", 8), ("cebolla", 1), ("albahaca", 10), ("manteca", 50)]),
    "Sopaipillas": (6, "Sopaipillas de zapallo fritas.",
        [("harina", 500), ("zapallo", 300), ("manteca", 80), ("polvos de hornear", 10), ("aceite", 300)]),
    "Completo italiano": (4, "Completo con palta, tomate y mayonesa (colores de la bandera italiana).",
        [("pan de completo", 4), ("vienesa", 4), ("palta", 2), ("tomate", 2), ("mayonesa", 100)]),
    "Chorrillana": (4, "Papas fritas con carne, cebolla y huevo.",
        [("papa", 800), ("posta de vacuno", 400), ("cebolla", 2), ("huevo", 4), ("aceite", 200)]),
    "Pebre": (8, "Salsa fresca de tomate, cebolla, cilantro y ají.",
        [("tomate", 2), ("cebolla", 1), ("cilantro", 20), ("ají verde", 2), ("aceite", 30)]),
    "Ensalada chilena": (4, "Tomate y cebolla pluma con cilantro.",
        [("tomate", 4), ("cebolla", 2), ("cilantro", 15), ("aceite", 20)]),
    "Caldillo de congrio": (4, "Caldillo de congrio con papa y verduras.",
        [("congrio", 600), ("papa", 400), ("cebolla", 2), ("zanahoria", 1), ("tomate", 2), ("vino tinto", 100)]),
    "Lentejas": (4, "Guiso de lentejas con longaniza.",
        [("lentejas", 400), ("longaniza", 200), ("cebolla", 1), ("zanahoria", 1), ("papa", 300)]),
    "Carbonada": (4, "Sopa-guiso de carne en cubos con verduras y arroz.",
        [("posta de vacuno", 300), ("papa", 400), ("zapallo", 300), ("choclo", 1), ("zanahoria", 1), ("arroz", 50), ("poroto verde", 150)]),
    "Pantrucas": (4, "Sopa con láminas de masa (pancutras) y carne.",
        [("pancutras", 300), ("posta de vacuno", 200), ("cebolla", 1), ("zanahoria", 1), ("huevo", 2), ("cilantro", 10)]),
    "Ajiaco": (4, "Sopa de carne con papas en rodajas y huevo.",
        [("posta de vacuno", 300), ("papa", 500), ("cebolla", 2), ("huevo", 4), ("ají verde", 1), ("comino", 5)]),
    "Mote con huesillo": (6, "Bebida de mote de trigo con huesillos y jugo dulce.",
        [("mote", 200), ("huesillo", 12), ("azúcar", 150)]),
    "Leche asada": (6, "Postre horneado de leche, huevo y azúcar.",
        [("leche", 1000), ("huevo", 6), ("azúcar", 200)]),
    "Arroz graneado": (4, "Arroz graneado a la chilena con cebolla y zanahoria.",
        [("arroz", 400), ("cebolla", 1), ("aceite", 30), ("zanahoria", 1)]),
    "Tomaticán": (4, "Guiso de carne con tomate, cebolla y choclo.",
        [("posta de vacuno", 300), ("tomate", 4), ("cebolla", 2), ("choclo", 1), ("huevo", 2)]),
}


def _conectar() -> sqlite3.Connection:
    """Objetivo: abrir la conexión SQLite con filas tipo dict.
    Entradas: ninguna. Salida: sqlite3.Connection."""
    con = sqlite3.connect(BD_PATH)
    con.row_factory = sqlite3.Row
    return con


def asegurar_bd(forzar: bool = False) -> Path:
    """Objetivo: crear y poblar la BD de recetas si no existe (o si `forzar`).
    Entradas: forzar (bool) para recrearla. Salida: Path — ruta del archivo .sqlite."""
    BD_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = _conectar()
    try:
        if forzar:
            for t in ("recetas", "ingredientes", "receta_items"):
                con.execute(f"DROP TABLE IF EXISTS {t}")
        con.execute("CREATE TABLE IF NOT EXISTS recetas (nombre TEXT, porciones_base INTEGER, descripcion TEXT)")
        con.execute("CREATE TABLE IF NOT EXISTS ingredientes (nombre TEXT, unidad TEXT, precio_clp REAL)")
        con.execute("CREATE TABLE IF NOT EXISTS receta_items (receta TEXT, ingrediente TEXT, cantidad REAL)")
        if forzar or con.execute("SELECT COUNT(*) FROM recetas").fetchone()[0] == 0:
            con.execute("DELETE FROM recetas")
            con.execute("DELETE FROM ingredientes")
            con.execute("DELETE FROM receta_items")
            con.executemany("INSERT INTO ingredientes VALUES (?,?,?)",
                            [(n, u, p) for n, (u, p) in INGREDIENTES.items()])
            for nombre, (porciones, desc, items) in RECETAS.items():
                con.execute("INSERT INTO recetas VALUES (?,?,?)", (nombre, porciones, desc))
                con.executemany("INSERT INTO receta_items VALUES (?,?,?)",
                                [(nombre, ing, cant) for ing, cant in items])
            con.commit()
    finally:
        con.close()
    return BD_PATH


def listar_recetas() -> list[dict]:
    """Objetivo: listar las recetas disponibles.
    Entradas: ninguna. Salida: list[dict] — {nombre, porciones_base, descripcion}."""
    asegurar_bd()
    con = _conectar()
    try:
        return [dict(r) for r in con.execute("SELECT nombre, porciones_base, descripcion FROM recetas").fetchall()]
    finally:
        con.close()


def _buscar_receta(con: sqlite3.Connection, nombre: str) -> sqlite3.Row | None:
    """Objetivo: buscar una receta por nombre exacto o parcial.
    Entradas: con (Connection), nombre (str). Salida: sqlite3.Row | None."""
    row = con.execute("SELECT * FROM recetas WHERE nombre = ?", (nombre,)).fetchone()
    if row:
        return row
    return con.execute("SELECT * FROM recetas WHERE nombre LIKE ?", (f"%{nombre}%",)).fetchone()


def ver_receta(nombre: str) -> dict:
    """Objetivo: devolver una receta con sus ingredientes (cantidad y unidad).
    Entradas: nombre (str) exacto o parcial. Salida: dict — {nombre, porciones_base,
    descripcion, ingredientes:[...]} o {nota} si no existe."""
    asegurar_bd()
    con = _conectar()
    try:
        r = _buscar_receta(con, nombre)
        if not r:
            return {"nota": f"No tengo la receta «{nombre}»."}
        items = con.execute(
            "SELECT i.ingrediente, i.cantidad, g.unidad FROM receta_items i "
            "JOIN ingredientes g ON g.nombre = i.ingrediente WHERE i.receta = ?", (r["nombre"],)).fetchall()
        return {"nombre": r["nombre"], "porciones_base": r["porciones_base"], "descripcion": r["descripcion"],
                "ingredientes": [{"ingrediente": it["ingrediente"], "cantidad": it["cantidad"], "unidad": it["unidad"]} for it in items]}
    finally:
        con.close()


def costear_receta(nombre: str, personas: int = 4) -> dict:
    """Costo de producir una receta para `personas` (por defecto 4): costo por ingrediente
    (cantidad escalada × precio por su unidad), costo total y por persona, en CLP."""
    asegurar_bd()
    con = _conectar()
    try:
        r = _buscar_receta(con, nombre)
        if not r:
            return {"nota": f"No tengo la receta «{nombre}». Usa listar_recetas para ver las disponibles."}
        base = r["porciones_base"] or personas
        factor = personas / base
        filas = con.execute(
            "SELECT i.ingrediente, i.cantidad, g.unidad, g.precio_clp FROM receta_items i "
            "JOIN ingredientes g ON g.nombre = i.ingrediente WHERE i.receta = ?", (r["nombre"],)).fetchall()
        detalle, total = [], 0.0
        for f in filas:
            cant = f["cantidad"] * factor
            costo = cant * f["precio_clp"]            # sin conversión: solo multiplicación
            total += costo
            detalle.append({"ingrediente": f["ingrediente"], "cantidad": round(cant, 2), "unidad": f["unidad"],
                            "precio_unitario_clp": f["precio_clp"], "costo_clp": round(costo)})
        return {"receta": r["nombre"], "personas": personas, "porciones_base": base,
                "detalle": detalle, "total_clp": round(total), "por_persona_clp": round(total / personas)}
    finally:
        con.close()


# ── restricciones y nutrición (derivadas de los ingredientes; estimación, no asesoría) ──────────
# Clasificación de ingredientes (no etiquetada a mano en cada receta: se infiere de estos conjuntos).
CARNICOS = {"carne molida", "posta de vacuno", "trutro de pollo", "longaniza", "congrio", "vienesa"}
ANIMALES = CARNICOS | {"huevo", "leche", "mayonesa", "manteca"}
CON_GLUTEN = {"harina", "pan de completo", "pancutras", "vienesa"}
# kcal aproximadas por 1 unidad del ingrediente (según su unidad: g, ml, unidad, diente). Estimación.
KCAL: dict[str, float] = {
    "harina": 3.6, "carne molida": 2.5, "posta de vacuno": 1.4, "trutro de pollo": 2.1,
    "longaniza": 3.0, "congrio": 1.0, "cebolla": 40, "ajo": 4, "huevo": 78, "aceite": 8.8,
    "aceitunas": 5, "pasas": 3.0, "choclo": 120, "albahaca": 0.2, "zapallo": 0.4, "porotos": 3.3,
    "papa": 0.8, "zanahoria": 40, "tomate": 20, "ají verde": 15, "cilantro": 0.2,
    "pan de completo": 180, "vienesa": 150, "palta": 240, "mayonesa": 6.8, "arroz": 3.6,
    "lentejas": 3.5, "pancutras": 2.8, "leche": 0.6, "azúcar": 4.0, "huesillo": 90, "mote": 3.6,
    "comino": 3.8, "vino tinto": 0.85, "manteca": 9.0, "polvos de hornear": 0.5, "poroto verde": 0.3,
}


def _resolver(nombre: str) -> str | None:
    """Objetivo: resolver el nombre (exacto o parcial, sin distinguir mayúsculas) a una clave de RECETAS."""
    if nombre in RECETAS:
        return nombre
    n = nombre.lower().strip()
    return next((k for k in RECETAS if n in k.lower()), None)


def clasificar(nombre: str) -> dict:
    """Objetivo: marcar si una receta es vegetariana, vegana y/o sin gluten (según sus ingredientes)."""
    real = _resolver(nombre)
    if not real:
        return {"nota": f"No tengo la receta «{nombre}»."}
    ings = {ing for ing, _ in RECETAS[real][2]}
    return {"receta": real, "vegetariano": not (ings & CARNICOS),
            "vegano": not (ings & ANIMALES), "sin_gluten": not (ings & CON_GLUTEN)}


def info_nutricional(nombre: str, personas: int = 4) -> dict:
    """Objetivo: estimación nutricional APROXIMADA (kcal) de una receta para `personas`."""
    real = _resolver(nombre)
    if not real:
        return {"nota": f"No tengo la receta «{nombre}». Usa listar_recetas para ver las disponibles."}
    porciones, _desc, items = RECETAS[real]
    factor = personas / (porciones or personas)
    total = sum(KCAL.get(ing, 0) * cant * factor for ing, cant in items)
    return {"receta": real, "personas": personas, "kcal_total_aprox": round(total),
            "kcal_por_persona_aprox": round(total / personas),
            "nota": "Estimación aproximada a partir de valores tipo; no es asesoría nutricional."}


def recetas_por_restriccion(restriccion: str, personas: int = 4, umbral_clp: int = 1500) -> dict:
    """Objetivo: recetas que cumplen una restricción: 'vegetariano', 'vegano', 'sin gluten' o
    'economica' (costo por persona <= umbral_clp). Salida: {restriccion, recetas:[...]} o {nota}."""
    r = restriccion.lower().strip()
    es_veg = "vegetarian" in r
    es_vegano = "vegan" in r
    es_sg = "gluten" in r
    es_eco = any(k in r for k in ("econom", "barat", "presupuesto"))
    if not (es_veg or es_vegano or es_sg or es_eco):
        return {"nota": "Restricciones que manejo: vegetariano, vegano, sin gluten, económica."}
    salida = []
    for nombre in RECETAS:
        c = clasificar(nombre)
        if es_vegano and not c["vegano"]:
            continue
        if es_veg and not c["vegetariano"]:
            continue
        if es_sg and not c["sin_gluten"]:
            continue
        por_persona = costear_receta(nombre, personas)["por_persona_clp"]
        if es_eco and por_persona > umbral_clp:
            continue
        salida.append({"receta": nombre, "por_persona_clp": por_persona})
    salida.sort(key=lambda x: x["por_persona_clp"])
    if not salida:
        return {"restriccion": r, "recetas": [], "nota": "No encontré recetas que cumplan esa restricción."}
    return {"restriccion": r, "personas": personas, "recetas": salida}
