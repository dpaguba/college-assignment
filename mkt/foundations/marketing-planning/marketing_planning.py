"""Der Planungsprozess von der Lage bis zur Kontrolle."""

STEPS = ("Situationsanalyse", "Zielbildung", "Strategie",
         "Marketing-Mix", "Umsetzung", "Kontrolle")


def steps():
    """Nennt die Schritte in ihrer Reihenfolge."""
    return list(STEPS)


def swot(strengths, weaknesses, opportunities, threats):
    """Ordnet eine Lage in die vier Felder und leitet Stossrichtungen ab.

    Die Matrix ist erst dann etwas wert, wenn aus den Feldern
    Kombinationen werden: Stärken auf Chancen ansetzen, Schwächen bei
    Chancen abbauen, Stärken gegen Gefahren stellen, und bei Schwächen
    und Gefahren zugleich den Rückzug prüfen. Eine SWOT ohne diesen
    Schritt ist eine Liste.

    Raises:
        ValueError: wenn ein Feld leer ist.
    """
    for field in (strengths, weaknesses, opportunities, threats):
        if not field:
            raise ValueError("jedes Feld braucht mindestens einen Eintrag")
    return {"SO": "Stärken nutzen, um Chancen zu ergreifen",
            "WO": "Schwächen abbauen, um Chancen zu ermöglichen",
            "ST": "Stärken einsetzen, um Gefahren abzuwehren",
            "WT": "Rückzug oder Absicherung prüfen",
            "fields": {"S": list(strengths), "W": list(weaknesses),
                       "O": list(opportunities), "T": list(threats)}}


def smart(goal):
    """Prüft ein Ziel gegen die fünf Anforderungen.

    Raises:
        ValueError: wenn eine Angabe fehlt.
    """
    required = ("specific", "measurable", "attainable", "relevant",
                "timed")
    missing = [name for name in required if name not in goal]
    if missing:
        raise ValueError("es fehlen: %s" % ", ".join(missing))
    failed = [name for name in required if not goal[name]]
    return {"is smart": not failed, "missing": failed,
            "why it matters": "ohne Messbarkeit und Frist gibt es keine "
                              "Kontrolle, und der letzte Schritt entfällt"}


def goal_hierarchy():
    """Nennt die Ebenen, auf denen Ziele stehen.

    Oberziele sind wirtschaftlich und messbar am Ergebnis: Umsatz,
    Marktanteil, Deckungsbeitrag. Darunter stehen psychografische Ziele:
    Bekanntheit, Image, Zufriedenheit. Sie sind Mittel und werden oft mit
    Zwecken verwechselt, weil sie leichter zu erreichen und angenehmer zu
    berichten sind.
    """
    return {"ökonomisch": ["Umsatz", "Marktanteil", "Deckungsbeitrag",
                           "Gewinn"],
            "psychografisch": ["Bekanntheit", "Image", "Einstellung",
                               "Zufriedenheit"],
            "relation": "die psychografischen sind Mittel für die "
                        "ökonomischen",
            "common mistake": "das Mittel berichten und den Zweck nicht "
                              "messen"}


def control_closes_the_loop(planned, achieved):
    """Vergleicht Plan und Ergebnis und benennt die Abweichung.

    Die Kontrolle ist der Schritt, der aus einer Planung ein Verfahren
    macht. Ohne sie ist der Plan eine Absichtserklärung, und die nächste
    Planung beginnt wieder bei null statt bei dem, was das letzte Mal
    nicht funktioniert hat.

    Raises:
        ValueError: bei einem nicht positiven Plan.
    """
    if planned <= 0:
        raise ValueError("der Planwert muss positiv sein")
    deviation = achieved - planned
    return {"planned": planned, "achieved": achieved,
            "deviation": deviation, "share": deviation / planned,
            "next question": "lag es am Ziel, an der Massnahme oder an "
                             "der Lage"}
