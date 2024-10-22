"""Die vier Stufen der Business Analytics."""

LEVELS = ("descriptive", "diagnostic", "predictive", "prescriptive")

QUESTIONS = {
    "descriptive": "was ist passiert",
    "diagnostic": "warum ist es passiert",
    "predictive": "was wird passieren",
    "prescriptive": "was sollen wir tun",
}

EFFORT = {
    "descriptive": {"effort": 1, "value": 1,
                    "needs": "Berichte über vorhandene Daten"},
    "diagnostic": {"effort": 2, "value": 2,
                   "needs": "Zusammenhänge, Vergleiche, Ursachensuche"},
    "predictive": {"effort": 3, "value": 3,
                   "needs": "ein Modell und Daten aus der Vergangenheit"},
    "prescriptive": {"effort": 4, "value": 4,
                     "needs": "ein Modell, Ziele und Handlungsspielraum"},
}

_MARKERS = (
    ("prescriptive", ("sollen wir", "welche massnahme", "welchen preis",
                      "empfehlung", "optimal")),
    ("predictive", ("wird", "prognose", "vorhersage", "nächsten monat",
                    "künftig")),
    ("diagnostic", ("warum", "woran liegt", "ursache", "weshalb")),
    ("descriptive", ("wie viele", "wie viel", "wie hoch", "letzten monat",
                     "im letzten", "gesamt")),
)


def levels():
    """Nennt die vier Stufen in aufsteigender Reihenfolge."""
    return list(LEVELS)


def question(level):
    """Nennt die Frage, die eine Stufe beantwortet.

    Raises:
        ValueError: bei einer unbekannten Stufe.
    """
    if level not in QUESTIONS:
        raise ValueError("unbekannte Stufe")
    return QUESTIONS[level]


def effort():
    """Stellt Aufwand und Nutzen je Stufe gegenüber.

    Beides steigt zusammen, und das ist der Grund, warum die meisten
    Unternehmen auf der ersten Stufe stehen bleiben: sie liefert sofort
    etwas, die vierte verlangt ein Modell, Ziele und die Freiheit, danach
    zu handeln.
    """
    return {name: dict(row) for name, row in EFFORT.items()}


def classify(text):
    """Ordnet eine Frage einer Stufe zu.

    Die Zuordnung geht über Signalwörter und ist damit grob; sie zeigt
    aber, woran die Stufen sich unterscheiden. Eine Frage nach einer Zahl
    ist beschreibend, eine nach einem Grund erklärend, eine nach der
    Zukunft vorhersagend, eine nach einer Handlung vorschreibend.

    Raises:
        ValueError: wenn kein Signalwort passt.
    """
    lowered = str(text).lower()
    for level, markers in _MARKERS:
        if any(marker in lowered for marker in markers):
            return level
    raise ValueError("die Frage lässt sich keiner Stufe zuordnen")


def where_most_companies_stand():
    """Nennt den Befund, den die Vorlesung an die Stufen hängt.

    Der Aufwand steigt schneller als die Bereitschaft, ihn zu tragen. Die
    erste Stufe braucht nur die Daten, die ohnehin anfallen; die letzte
    braucht ein Modell, an das jemand glaubt, und die Bereitschaft, den
    Vorschlag auch umzusetzen. Ohne die zweite Bedingung bleibt die
    vierte Stufe ein Bericht, den niemand liest.
    """
    return {"most reach": "descriptive und diagnostic",
            "blocker of predictive": "es fehlt das Modell und die Daten",
            "blocker of prescriptive": "es fehlt die Bereitschaft, dem "
                                       "Vorschlag zu folgen",
            "consequence": "eine Empfehlung ohne Handlungsspielraum ist "
                           "ein Bericht"}
