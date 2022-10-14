"""Der BPM-Lebenszyklus und was jede Phase an die nächste weitergibt."""

PHASES = ("Prozessidentifikation", "Prozesserhebung", "Prozessanalyse",
          "Prozessverbesserung", "Prozessimplementierung",
          "Prozessüberwachung")

OUTPUTS = {
    "Prozessidentifikation": "Prozessarchitektur",
    "Prozesserhebung": "Istprozessmodell",
    "Prozessanalyse": "Verständnis der Schwächen",
    "Prozessverbesserung": "Sollprozessmodell",
    "Prozessimplementierung": "Prozessausführung",
    "Prozessüberwachung": "Kennzahlen",
}


def phases():
    """Nennt die Phasen in der Reihenfolge des Zyklus.

    Die Identifikation steht als Schritt null davor: sie sagt, welcher
    Prozess überhaupt betrachtet wird, und wird nicht für jeden Durchlauf
    wiederholt.
    """
    return list(PHASES)


def output_of(phase):
    """Nennt, was eine Phase hervorbringt.

    Raises:
        ValueError: bei einer unbekannten Phase.
    """
    if phase not in OUTPUTS:
        raise ValueError("unbekannte Phase")
    return OUTPUTS[phase]


def handovers():
    """Listet die Übergaben zwischen den Phasen.

    Der Zyklus schliesst sich: die Kennzahlen aus der Überwachung sind der
    Anlass, den Prozess erneut zu erheben. Deshalb zeigt die letzte
    Übergabe auf die Erhebung und nicht auf die Identifikation.

    Returns:
        Liste von Abbildungen mit ``from``, ``produces`` und ``to``.
    """
    steps = []
    for index, phase in enumerate(PHASES):
        if index + 1 < len(PHASES):
            follower = PHASES[index + 1]
        else:
            follower = PHASES[1]
        steps.append({"from": phase, "produces": OUTPUTS[phase],
                      "to": follower})
    return steps


def effort_of_identification(maturity):
    """Schätzt den Aufwand der Identifikation über den Reifegrad.

    Gefragt wird, ob es schon Initiativen gab, ob die Geschäftsprozesse
    ganz oder teilweise definiert sind und ob eine Dokumentation vorliegt.
    Je mehr davon vorhanden ist, desto weniger bleibt zu tun.

    Args:
        maturity: Zahl der erfüllten Punkte, null bis drei.

    Returns:
        Abbildung mit dem Aufwand und den offenen Fragen.

    Raises:
        ValueError: bei einem Reifegrad ausserhalb von null bis drei.
    """
    questions = ["frühere Initiativen", "definierte Geschäftsprozesse",
                 "vorhandene Dokumentation"]
    if not 0 <= maturity <= len(questions):
        raise ValueError("Reifegrad liegt ausserhalb von 0 bis 3")
    return {"effort": len(questions) - maturity,
            "open": questions[maturity:],
            "note": "die Identifikation ist in der Regel problemgetrieben"}


def is_problem_driven():
    """Sagt, woher der Anstoss für den Zyklus kommt.

    Ein Unternehmen beginnt selten mit dem Zyklus, weil es ihn schön
    findet, sondern weil etwas nicht funktioniert; die Identifikation
    sucht dann die Prozesse, die für das Problem ursächlich sind.
    """
    return {"driven by": "a problem",
            "first question": "which processes cause it",
            "result": "Prozessarchitektur"}
