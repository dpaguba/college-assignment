"""Bell-LaPadula und Biba: zwei Regelwerke mit entgegengesetztem Ziel."""

MODELS = ("bell lapadula", "biba")


def goal(model):
    """Nennt, was ein Modell schützen soll.

    Raises:
        ValueError: bei einem unbekannten Modell.
    """
    if model not in MODELS:
        raise ValueError("unbekanntes Modell")
    return "secrecy" if model == "bell lapadula" else "integrity"


def permitted(model, operation, subject, obj):
    """Entscheidet eine Anfrage nach einem der beiden Modelle.

    Die Stufen sind wie in der Übung gezählt: 0 ist die höchste, 3 die
    niedrigste. Bell-LaPadula verbietet das Lesen von oben und das
    Schreiben nach oben; Biba verbietet genau das Umgekehrte.

    Args:
        model: ``bell lapadula`` oder ``biba``.
        operation: ``read`` oder ``write``.
        subject: Stufe des Zugreifenden.
        obj: Stufe des Objekts.

    Raises:
        ValueError: bei unbekanntem Modell oder unbekannter Operation.
    """
    if model not in MODELS:
        raise ValueError("unbekanntes Modell")
    if operation not in ("read", "write"):
        raise ValueError("unbekannte Operation")
    if model == "bell lapadula":
        if operation == "read":
            return subject <= obj
        return subject >= obj
    if operation == "read":
        return subject >= obj
    return subject <= obj


def rules():
    """Nennt die Regeln unter ihren üblichen Namen."""
    return {"bell lapadula": {"simple security": "no read up",
                              "star property": "no write down"},
            "biba": {"simple integrity": "no read down",
                     "star property": "no write up"}}


def exercise_table():
    """Wertet die sechs Anfragen aus Aufgabe 1.3 aus.

    Returns:
        Abbildung von (Operation, Subjektstufe, Objektstufe) auf die
        Antworten beider Modelle und ihrer Verbindung.
    """
    requests = [("read", 0, 0), ("read", 1, 3), ("write", 0, 2),
                ("write", 1, 1), ("write", 3, 2), ("read", 3, 2)]
    table = {}
    for operation, subject, obj in requests:
        first = permitted("bell lapadula", operation, subject, obj)
        second = permitted("biba", operation, subject, obj)
        table[(operation, subject, obj)] = {"bell lapadula": first,
                                            "biba": second,
                                            "both": first and second}
    return table


def combined_report(levels=4):
    """Prüft, was von den Zugriffen übrig bleibt, wenn beide Modelle gelten.

    Bell-LaPadula erlaubt das Lesen nach unten und das Schreiben nach
    oben, Biba genau umgekehrt; zusammen bleibt nur die eigene Stufe.

    Returns:
        Abbildung mit der Zahl der erlaubten Zugriffe über Stufen hinweg
        und dem Befund.
    """
    across = 0
    within = 0
    for operation in ("read", "write"):
        for subject in range(levels):
            for obj in range(levels):
                if not (permitted("bell lapadula", operation, subject, obj)
                        and permitted("biba", operation, subject, obj)):
                    continue
                if subject == obj:
                    within += 1
                else:
                    across += 1
    return {"cross level requests permitted": across,
            "same level requests permitted": within,
            "only within one level": across == 0}


def why_not_both():
    """Erklärt, warum die Verbindung beider Modelle unbrauchbar ist.

    Beide Modelle verfolgen einander ergänzende Ziele; zugleich angewandt
    verbieten sie jeden Austausch zwischen Stufen, so dass Daten nur noch
    innerhalb einer Stufe fliessen können.
    """
    return {"secrecy": "no read up, no write down",
            "integrity": "no read down, no write up",
            "together": "no flow between levels at all"}
