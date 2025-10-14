"""Der Datenwürfel: Dimensionen aussen, Kennzahlen innen."""

DIMENSIONS = ("Projekt", "Quartal", "Jahr", "Risikoart")
MEASURES = ("Risiko-Score", "Strategischer Fit", "Quartalsbudget")

_RAW = (
    ("P1 Kundenportal", "Q4", "2025", "Technisch", 4, 8, 220),
    ("P1 Kundenportal", "Q4", "2025", "Organisatorisch", 3, 8, 220),
    ("P1 Kundenportal", "Q4", "2025", "Markt", 2, 8, 220),
    ("P1 Kundenportal", "Q3", "2025", "Technisch", 5, 8, 250),
    ("P1 Kundenportal", "Q3", "2025", "Organisatorisch", 4, 8, 250),
    ("P1 Kundenportal", "Q3", "2025", "Markt", 3, 8, 250),
    ("P2 KI-Prognose", "Q4", "2025", "Technisch", 7, 9, 300),
    ("P2 KI-Prognose", "Q4", "2025", "Organisatorisch", 6, 9, 300),
    ("P2 KI-Prognose", "Q4", "2025", "Markt", 5, 9, 300),
    ("P2 KI-Prognose", "Q3", "2025", "Technisch", 8, 9, 340),
    ("P2 KI-Prognose", "Q3", "2025", "Organisatorisch", 7, 9, 340),
    ("P2 KI-Prognose", "Q3", "2025", "Markt", 6, 9, 340),
    ("P3 ERP-Migration", "Q4", "2025", "Technisch", 6, 6, 500),
    ("P3 ERP-Migration", "Q4", "2025", "Organisatorisch", 8, 6, 500),
    ("P3 ERP-Migration", "Q4", "2025", "Markt", 2, 6, 500),
    ("P3 ERP-Migration", "Q3", "2025", "Technisch", 7, 6, 520),
    ("P3 ERP-Migration", "Q3", "2025", "Organisatorisch", 9, 6, 520),
    ("P3 ERP-Migration", "Q3", "2025", "Markt", 3, 6, 520),
    ("P4 Neue Fassade", "Q4", "2025", "Technisch", 3, 7, 180),
    ("P4 Neue Fassade", "Q4", "2025", "Organisatorisch", 4, 7, 180),
    ("P4 Neue Fassade", "Q4", "2025", "Markt", 3, 7, 180),
    ("P5 IoT Produkt", "Q4", "2025", "Technisch", 9, 8, 600),
    ("P5 IoT Produkt", "Q4", "2025", "Organisatorisch", 7, 8, 600),
    ("P5 IoT Produkt", "Q4", "2025", "Markt", 8, 9, 600),
)

PROJECTS = tuple(
    dict(zip(DIMENSIONS + MEASURES, row)) for row in _RAW)


def build(rows, dimensions=DIMENSIONS, measures=MEASURES):
    """Baut aus einer Tabelle einen Würfel.

    Der Würfel selbst speichert die Zeilen unverändert; was ihn zum Würfel
    macht, ist die Trennung zwischen Achsen und Inhalt. Die Achsen sind die
    qualitativen Dimensionen, der Inhalt die quantitativen Kennzahlen.

    Args:
        rows: die Zeilen als Abbildungen.
        dimensions: die Namen der Achsen.
        measures: die Namen der Kennzahlen.

    Returns:
        Abbildung mit ``rows``, ``dimensions``, ``measures`` und den
        Ausprägungen je Dimension.

    Raises:
        ValueError: bei einer leeren Tabelle oder einer fehlenden Spalte.
    """
    if not rows:
        raise ValueError("leere Tabelle")
    for row in rows:
        for name in tuple(dimensions) + tuple(measures):
            if name not in row:
                raise ValueError("Spalte fehlt: %s" % name)
    members = {name: sorted({row[name] for row in rows})
               for name in dimensions}
    return {"rows": list(rows), "dimensions": list(dimensions),
            "measures": list(measures), "members": members}


def _check_selection(built, selection):
    """Prüft, dass eine Auswahl nur bekannte Dimensionen nennt.

    Raises:
        ValueError: bei einer unbekannten Dimension.
    """
    for name in selection:
        if name not in built["dimensions"]:
            raise ValueError("unbekannte Dimension: %s" % name)


def cell(built, selection):
    """Nennt die Zeilen, die zu einer Auswahl gehören.

    Args:
        built: der Würfel.
        selection: Abbildung von der Dimension auf die gewünschte
            Ausprägung; nicht genannte Dimensionen bleiben offen.

    Returns:
        Liste der passenden Zeilen.

    Raises:
        ValueError: bei einer unbekannten Dimension.
    """
    _check_selection(built, selection)
    return [row for row in built["rows"]
            if all(row[name] == value for name, value in selection.items())]


def density(built):
    """Misst, wie voll der Würfel ist.

    Das Kreuzprodukt der Dimensionen gibt die Zahl der möglichen Zellen,
    die Tabelle die der belegten. Reale Würfel sind fast immer dünn
    besetzt, und die leeren Zellen sind kein Fehler: sie bedeuten, dass es
    die Kombination nicht gab.

    Returns:
        Abbildung mit ``possible``, ``filled`` und ``density``.
    """
    possible = 1
    for name in built["dimensions"]:
        possible *= len(built["members"][name])
    filled = len({tuple(row[name] for name in built["dimensions"])
                  for row in built["rows"]})
    return {"possible": possible, "filled": filled,
            "density": filled / possible,
            "empty": possible - filled}


def where_the_data_comes_from():
    """Nennt die Quelle der Zahlen.

    Die Tabelle ist die Projektcontrolling-Tabelle aus Zettel 5: fünf
    Projekte, je Quartal und Risikoart eine Zeile, mit dem Risikowert, dem
    strategischen Fit und dem Quartalsbudget.
    """
    return {"source": "Zettel 5, Projektcontrolling",
            "rows": len(PROJECTS),
            "grain": "ein Projekt, ein Quartal, eine Risikoart",
            "note": "die Zeilen wurden unverändert übernommen"}
