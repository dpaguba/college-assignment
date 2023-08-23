"""Welche Aufgaben sich automatisieren lassen."""

CRITERIA = ("regelbasiert", "strukturierte Eingabe", "hohe Frequenz",
            "stabiler Ablauf", "geringe Ausnahmequote")

TASKS = {
    "Rechnungen aus einem Postfach in das ERP übertragen":
        (True, True, True, True, True),
    "Stammdaten zwischen zwei Systemen abgleichen":
        (True, True, True, True, False),
    "einen Kreditantrag abschliessend beurteilen":
        (False, False, False, True, False),
    "eine Beschwerde beantworten":
        (False, False, True, False, False),
    "einen Monatsbericht zusammenstellen":
        (True, True, False, True, True),
}


def criteria():
    """Nennt die fünf Kriterien."""
    return list(CRITERIA)


def score(answers):
    """Zählt, wie viele Kriterien eine Aufgabe erfüllt.

    Raises:
        ValueError: bei einer falschen Zahl von Antworten.
    """
    if len(answers) != len(CRITERIA):
        raise ValueError("je Kriterium eine Antwort")
    return sum(1 for answer in answers if answer)


def assess(task):
    """Beurteilt eine Aufgabe aus der Liste.

    Raises:
        ValueError: bei einer unbekannten Aufgabe.
    """
    if task not in TASKS:
        raise ValueError("unbekannte Aufgabe")
    answers = TASKS[task]
    points = score(answers)
    if points == len(CRITERIA):
        verdict = "geeignet"
    elif points >= 3:
        verdict = "teilweise geeignet"
    else:
        verdict = "ungeeignet"
    return {"task": task, "score": points, "verdict": verdict,
            "missing": [name for name, answer in zip(CRITERIA, answers)
                        if not answer]}


def ranking():
    """Ordnet die Aufgaben nach ihrer Eignung.

    Returns:
        Liste aus Aufgabe und Punktzahl, absteigend.
    """
    return sorted(((task, score(answers))
                   for task, answers in TASKS.items()),
                  key=lambda row: (-row[1], row[0]))


def the_exception_rate_decides():
    """Nennt das Kriterium, das in der Praxis entscheidet.

    Ein Ablauf mit fünf Prozent Ausnahmen lohnt sich; einer mit dreissig
    Prozent nicht, weil dann fast jeder dritte Fall doch von Hand
    bearbeitet wird und der Roboter obendrein gewartet werden muss. Die
    Rechnung geht nicht über die Zahl der Fälle, sondern über die Zahl
    der Fälle, die durchlaufen.

    Returns:
        Abbildung mit dem Beispiel.
    """
    return {"at five percent exceptions": "der Roboter erledigt 95 von 100",
            "at thirty percent": "er erledigt 70 und die Ausnahme kostet "
                                 "mehr als vorher, weil sie nun aus einem "
                                 "halb bearbeiteten Zustand kommt",
            "the number to ask for": "die Ausnahmequote, nicht das "
                                     "Fallvolumen",
            "second question": "wie oft ändert sich das System darunter"}


def why_judgement_does_not_automate():
    """Sagt, was an einer Beurteilung nicht regelbasiert ist.

    Eine Regel bildet Fälle auf Antworten ab. Eine Beurteilung wägt
    Gründe, die einander widersprechen, und das Ergebnis muss vertretbar
    sein, nicht nur richtig. Wer sie in Regeln fasst, hat nicht die
    Beurteilung automatisiert, sondern eine bestimmte Beurteilung
    festgeschrieben, und die Änderung braucht dann einen Entwickler
    statt eines Gesprächs.
    """
    return {"rule": "bildet Fälle auf Antworten ab",
            "judgement": "wägt Gründe, die einander widersprechen",
            "what automation does to it": "schreibt eine bestimmte "
                                          "Abwägung fest",
            "cost": "die Änderung braucht dann einen Entwickler"}
