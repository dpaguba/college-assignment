"""Das Prozessportfolio: welcher Prozess zuerst verbessert wird."""

CRITERIA = ("importance", "need", "ability")

MEANING = {
    "importance": "strategische Bedeutung, beurteilt durch Führungskräfte",
    "need": "Verbesserungswürdigkeit, die Differenz zwischen Ziel- und "
            "Ist-Kennzahlen",
    "ability": "Verbesserungsfähigkeit, beurteilt durch die "
               "Prozessverantwortlichen",
}

THRESHOLD_IMPORTANCE = 0.5
THRESHOLD_NEED = 0.25

UNIVERSITY = (
    {"process": "Studienprogramme entwickeln und verwalten",
     "importance": 0.90, "need": 0.10, "ability": 0.40},
    {"process": "Studienprogramme vermarkten",
     "importance": 0.75, "need": 0.20, "ability": 0.60},
    {"process": "Kurse ansetzen",
     "importance": 0.95, "need": 0.85, "ability": 0.50},
    {"process": "Kurse durchführen",
     "importance": 0.95, "need": 0.30, "ability": 0.30},
    {"process": "Studierendenberatung verwalten",
     "importance": 0.85, "need": 0.50, "ability": 0.40},
    {"process": "Räume verwalten",
     "importance": 0.35, "need": 0.75, "ability": 0.70},
)


def criteria():
    """Nennt die drei Kriterien mit ihrer Bedeutung."""
    return dict(MEANING)


def score(row):
    """Bewertet einen Prozess als Produkt der drei Kriterien.

    Das Produkt und nicht die Summe, weil die Kriterien einander nicht
    ersetzen: ein Prozess, der sich nicht verbessern lässt, bringt auch
    dann nichts, wenn er strategisch wichtig ist und viel im Argen liegt.
    Eine Summe würde die Null in einem Kriterium durch die anderen
    ausgleichen.

    Args:
        row: Abbildung mit ``importance``, ``need`` und ``ability``.

    Returns:
        Der Wert zwischen null und eins.

    Raises:
        ValueError: bei einem Wert ausserhalb von null bis eins.
    """
    product = 1.0
    for criterion in CRITERIA:
        value = row[criterion]
        if not 0.0 <= value <= 1.0:
            raise ValueError("Bewertung liegt ausserhalb von 0 bis 1")
        product *= value
    return product


def in_focus(row):
    """Sagt, ob ein Prozess im Auswahlfokus liegt.

    Der Fokus ist das Feld links oben: hohe strategische Bedeutung und
    hohe Verbesserungswürdigkeit. Die Verbesserungsfähigkeit entscheidet
    innerhalb des Feldes über die Reihenfolge, nicht über den Eintritt.
    """
    return (row["importance"] >= THRESHOLD_IMPORTANCE
            and row["need"] >= THRESHOLD_NEED)


def select(rows):
    """Wählt die Prozesse des Fokus und ordnet sie nach ihrer Bewertung.

    Returns:
        Liste der Zeilen, um ``score`` ergänzt, absteigend sortiert.
    """
    chosen = [dict(row, score=score(row)) for row in rows if in_focus(row)]
    return sorted(chosen, key=lambda row: -row["score"])


def quadrant(row):
    """Benennt das Feld, in dem ein Prozess liegt."""
    high_importance = row["importance"] >= THRESHOLD_IMPORTANCE
    high_need = row["need"] >= THRESHOLD_NEED
    if high_importance and high_need:
        return "Auswahlfokus"
    if high_importance:
        return "wichtig, aber in Ordnung"
    if high_need:
        return "verbesserungswürdig, aber nebensächlich"
    return "weder noch"


def why_visualise():
    """Nennt, wozu die Darstellung dient.

    Die Zahlen der drei Kriterien stehen sonst in einer Tabelle
    nebeneinander und lassen sich schlecht vergleichen. Im Bild fällt das
    Feld links oben ins Auge, und die Farbe der Blase trägt das dritte
    Kriterium mit, ohne eine dritte Achse zu brauchen.
    """
    return {"axes": ["strategische Bedeutung", "Verbesserungswürdigkeit"],
            "colour": "Verbesserungsfähigkeit",
            "reads off": "wo sich Verbesserung lohnt und wo sie möglich ist"}
