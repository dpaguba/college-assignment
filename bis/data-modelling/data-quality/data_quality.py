"""Datenqualität, geprüft an der Projekttabelle aus Zettel 5."""

DIMENSIONS = {
    "completeness": "sind alle erwarteten Werte da",
    "consistency": "widersprechen sich zwei Angaben derselben Sache",
    "accuracy": "stimmt der Wert mit der Wirklichkeit überein",
    "timeliness": "ist der Wert aktuell genug für seine Verwendung",
    "uniqueness": "steht dieselbe Sache nur einmal in den Daten",
}

PROJECT_ROWS = (
    ("P1 Kundenportal", "Q4", "Technisch", 4, 8, 220),
    ("P1 Kundenportal", "Q4", "Organisatorisch", 3, 8, 220),
    ("P1 Kundenportal", "Q4", "Markt", 2, 8, 220),
    ("P1 Kundenportal", "Q3", "Technisch", 5, 8, 250),
    ("P1 Kundenportal", "Q3", "Organisatorisch", 4, 8, 250),
    ("P1 Kundenportal", "Q3", "Markt", 3, 8, 250),
    ("P2 KI-Prognose", "Q4", "Technisch", 7, 9, 300),
    ("P2 KI-Prognose", "Q4", "Organisatorisch", 6, 9, 300),
    ("P2 KI-Prognose", "Q4", "Markt", 5, 9, 300),
    ("P2 KI-Prognose", "Q3", "Technisch", 8, 9, 340),
    ("P2 KI-Prognose", "Q3", "Organisatorisch", 7, 9, 340),
    ("P2 KI-Prognose", "Q3", "Markt", 6, 9, 340),
    ("P3 ERP-Migration", "Q4", "Technisch", 6, 6, 500),
    ("P3 ERP-Migration", "Q4", "Organisatorisch", 8, 6, 500),
    ("P3 ERP-Migration", "Q4", "Markt", 2, 6, 500),
    ("P3 ERP-Migration", "Q3", "Technisch", 7, 6, 520),
    ("P3 ERP-Migration", "Q3", "Organisatorisch", 9, 6, 520),
    ("P3 ERP-Migration", "Q3", "Markt", 3, 6, 520),
    ("P4 Neue Fassade", "Q4", "Technisch", 3, 7, 180),
    ("P4 Neue Fassade", "Q4", "Organisatorisch", 4, 7, 180),
    ("P4 Neue Fassade", "Q4", "Markt", 3, 7, 180),
    ("P5 IoT Produkt", "Q4", "Technisch", 9, 8, 600),
    ("P5 IoT Produkt", "Q4", "Organisatorisch", 7, 8, 600),
    ("P5 IoT Produkt", "Q4", "Markt", 8, 9, 600),
)

COLUMNS = ("Projekt", "Quartal", "Risikoart", "Risiko-Score",
           "Strategischer Fit", "Quartalsbudget")

ROWS = tuple(dict(zip(COLUMNS, row)) for row in PROJECT_ROWS)


def dimensions():
    """Nennt die Dimensionen der Datenqualität."""
    return dict(DIMENSIONS)


def determines(rows, source, target):
    """Prüft eine funktionale Abhängigkeit zwischen zwei Spalten.

    Die Abhängigkeit gilt, wenn zu jedem Wert der einen Spalte nur ein
    Wert der anderen vorkommt. Sie ist das Werkzeug, mit dem sich
    Widersprüche in einer Tabelle finden lassen, ohne die Wirklichkeit zu
    kennen: die Tabelle widerspricht sich selbst.

    Raises:
        ValueError: bei einer leeren Tabelle oder einer unbekannten
            Spalte.
    """
    if not rows:
        raise ValueError("leere Tabelle")
    for name in (source, target):
        if name not in rows[0]:
            raise ValueError("unbekannte Spalte: %s" % name)
    seen = {}
    for row in rows:
        key = row[source]
        if key in seen and seen[key] != row[target]:
            return False
        seen[key] = row[target]
    return True


def violations_of(rows, source, target):
    """Nennt die Werte, bei denen eine Abhängigkeit bricht.

    Raises:
        ValueError: bei einer leeren Tabelle oder einer unbekannten
            Spalte.
    """
    if not rows:
        raise ValueError("leere Tabelle")
    for name in (source, target):
        if name not in rows[0]:
            raise ValueError("unbekannte Spalte: %s" % name)
    values = {}
    for row in rows:
        values.setdefault(row[source], set()).add(row[target])
    return sorted(key for key, found in values.items() if len(found) > 1)


def check_projects():
    """Prüft die Projekttabelle auf Widersprüche und Lücken.

    Der strategische Fit ist eine Eigenschaft des Projektes und darf
    innerhalb eines Projektes nicht von der Risikoart abhängen. In der
    Tabelle tut er das bei genau einem Projekt: P5 IoT Produkt steht mit
    8 in den Zeilen Technisch und Organisatorisch und mit 9 in der Zeile
    Markt. Welcher Wert stimmt, sagen die Daten nicht; dass sie sich
    widersprechen, sagen sie.

    Ausserdem ist die Tabelle unvollständig: drei Projekte haben beide
    Quartale, zwei nur das vierte.

    Returns:
        Abbildung mit den Befunden.
    """
    quarters = {}
    for row in ROWS:
        quarters.setdefault(row["Projekt"], set()).add(row["Quartal"])
    complete = max(len(found) for found in quarters.values())
    return {"projects": sorted(quarters),
            "inconsistent": violations_of(ROWS, "Projekt",
                                          "Strategischer Fit"),
            "missing quarters": sorted(name for name, found
                                       in quarters.items()
                                       if len(found) < complete),
            "rows": len(ROWS),
            "budget depends on": ["Projekt", "Quartal"],
            "note": "welcher der beiden Werte stimmt, sagen die Daten nicht"}


def what_to_do_with_a_contradiction():
    """Nennt die Reihenfolge, in der ein Widerspruch behandelt wird.

    Zuerst festhalten, dass er da ist, und nicht stillschweigend einen der
    beiden Werte nehmen. Dann die Quelle fragen, welcher gilt. Und erst
    danach die Regel als Prüfung in das System einbauen, damit derselbe
    Widerspruch nicht wieder entsteht.
    """
    return ["record it, do not silently pick one",
            "ask the source which value holds",
            "then add the rule as a constraint",
            "a correction without the constraint comes back next quarter"]
