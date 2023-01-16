"""Konsumentenverhalten: das SOR-Modell und die Kaufentscheidung."""

TYPES = {
    "extensiv": {"involvement": "hoch", "information": "viel",
                 "example": "ein Auto", "duration": "Wochen"},
    "limitiert": {"involvement": "mittel", "information": "auf wenige "
                                                          "Marken begrenzt",
                  "example": "ein Fernseher", "duration": "Tage"},
    "habitualisiert": {"involvement": "gering", "information": "keine",
                       "example": "Kaffee", "duration": "Sekunden"},
    "impulsiv": {"involvement": "gering", "information": "keine",
                 "example": "Süssigkeiten an der Kasse",
                 "duration": "sofort"},
}


def types():
    """Nennt die vier Arten von Kaufentscheidungen."""
    return dict(TYPES)


def describe(kind):
    """Beschreibt eine Art.

    Raises:
        ValueError: bei einer unbekannten Art.
    """
    if kind not in TYPES:
        raise ValueError("unbekannte Art")
    return dict(TYPES[kind])


def sor():
    """Erklärt das Modell, mit dem die Vorlesung arbeitet.

    Ein Reiz trifft auf den Konsumenten, in ihm laufen Vorgänge ab, und
    heraus kommt eine Reaktion. Das S-R-Modell lässt die Mitte weg und
    behandelt den Menschen als schwarzen Kasten; das S-O-R-Modell öffnet
    ihn und beschreibt, was drinnen geschieht.

    Die Vorgänge in der Mitte teilt man in aktivierende, die antreiben,
    und kognitive, die verarbeiten. Ohne sie erklärt man Verhalten mit
    Korrelationen und weiss nicht, warum eine Massnahme das nächste Mal
    nicht wirkt.
    """
    return {"S": "Stimulus, der Reiz von aussen",
            "O": "Organismus, was im Konsumenten geschieht",
            "R": "Response, die beobachtbare Reaktion",
            "activating": ["Emotion", "Motivation", "Einstellung"],
            "cognitive": ["Wahrnehmung", "Lernen", "Gedächtnis"],
            "S-R leaves out": "die Mitte, und damit die Erklärung"}


def classify(involvement, repeated, planned):
    """Ordnet eine Kaufentscheidung ein.

    Raises:
        ValueError: bei einem unzulässigen Beteiligungsgrad.
    """
    if involvement not in ("hoch", "mittel", "gering"):
        raise ValueError("unzulässiger Beteiligungsgrad")
    if involvement == "hoch":
        return "extensiv"
    if involvement == "mittel":
        return "limitiert"
    if repeated:
        return "habitualisiert"
    if not planned:
        return "impulsiv"
    return "limitiert"


def dissonance(expectation, experience):
    """Misst die Nachkaufdissonanz.

    Nach einer wichtigen Entscheidung sucht der Käufer Bestätigung und
    meidet Widerspruch; deshalb liest er Werbung für das Produkt, das er
    schon gekauft hat. Für den Anbieter folgt daraus, dass die
    Kommunikation nach dem Kauf nicht endet: sie ist dort billiger als
    vorher und wirkt auf die Weiterempfehlung.

    Args:
        expectation: was erwartet wurde, eins bis sieben.
        experience: was erlebt wurde, eins bis sieben.

    Returns:
        Abbildung mit der Abweichung und der Folge.

    Raises:
        ValueError: bei einem Wert ausserhalb der Skala.
    """
    for value in (expectation, experience):
        if not 1 <= value <= 7:
            raise ValueError("Wert ausserhalb der Skala von 1 bis 7")
    gap = experience - expectation
    if gap > 0:
        result = "Begeisterung, hohe Weiterempfehlung"
    elif gap == 0:
        result = "Zufriedenheit, keine besondere Wirkung"
    else:
        result = "Unzufriedenheit, Dissonanz, Beschwerde oder Abwanderung"
    return {"gap": gap, "result": result,
            "note": "gemessen wird gegen die Erwartung, nicht gegen eine "
                    "objektive Qualität",
            "consequence": "zu hohe Versprechen erzeugen Unzufriedenheit "
                           "bei gleichbleibendem Produkt"}


def why_the_expectation_is_the_lever():
    """Nennt die unangenehme Folge aus der Definition der Zufriedenheit.

    Zufriedenheit ist Erlebtes minus Erwartetem. Wer die Erwartung senkt,
    steigert die Zufriedenheit, ohne das Produkt zu verbessern; wer sie
    in der Werbung hebt, senkt sie. Das ist der Grund, warum eine
    erfolgreiche Kampagne die Beschwerdequote steigen lassen kann, und
    warum beide Zahlen zusammen gelesen werden müssen.
    """
    return {"satisfaction": "Erlebtes minus Erwartetes",
            "lower the promise": "Zufriedenheit steigt ohne besseres "
                                 "Produkt",
            "raise the promise": "Zufriedenheit sinkt bei gleichem "
                                 "Produkt",
            "watch together": ["Kampagnenerfolg", "Beschwerdequote"]}
