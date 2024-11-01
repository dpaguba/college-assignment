"""Die drei Arten des maschinellen Lernens."""

TYPES = {
    "supervised": {
        "labels": True,
        "data": "Eingabevektoren mit ihren Zielvektoren",
        "goal": "ein Modell, das die Eingabe auf die Ausgabe abbildet, "
                "auch für neue Eingaben",
        "tasks": ["Klassifizierung", "Regression"]},
    "unsupervised": {
        "labels": False,
        "data": "nur die Eingaben",
        "goal": "Struktur in den Daten finden, ohne zu wissen, wonach",
        "tasks": ["Clustering", "Dimensionsreduktion",
                  "Ausreissererkennung"]},
    "reinforcement": {
        "labels": False,
        "data": "kein fester Datensatz, sondern eine Umgebung",
        "goal": "eine Strategie, die die Belohnung über die Zeit maximiert",
        "tasks": ["Steuerung", "Spiele", "Regelung"]},
}

_NUMBER_MARKERS = ("preis", "euro", "wie viel", "wie hoch", "menge",
                   "temperatur", "umsatz")


def types():
    """Nennt die drei Arten."""
    return ["supervised", "unsupervised", "reinforcement"]


def describe(kind):
    """Beschreibt eine Art.

    Raises:
        ValueError: bei einer unbekannten Art.
    """
    if kind not in TYPES:
        raise ValueError("unbekannte Lernart")
    return dict(TYPES[kind])


def task(question):
    """Trennt Klassifizierung von Regression.

    Beide sind überwachtes Lernen; sie unterscheiden sich nur darin, was
    vorhergesagt wird. Eine diskrete Kategorie ist Klassifizierung, ein
    kontinuierlicher Wert Regression.
    """
    lowered = str(question).lower()
    if any(marker in lowered for marker in _NUMBER_MARKERS):
        return "Regression"
    return "Klassifizierung"


def spam_filter():
    """Beantwortet die Frage des Merkblatts zum Spamfilter.

    Der Filter bekommt die Nachrichten als Eingabe: Absender, Betreff,
    Text, Kopfzeilen. Die Label sind die Entscheidungen, die Menschen
    getroffen haben, meist durch das Verschieben in den Spamordner. Das
    macht es zu überwachtem Lernen mit zwei Klassen.
    """
    return {"type": "supervised", "task": "Klassifizierung",
            "input": "Absender, Betreff, Text, Kopfzeilen",
            "label": "die Einordnung durch den Empfänger",
            "where the labels come from": "der Spamordner",
            "catch": "die Label sind selbst fehlerhaft, weil Menschen "
                     "unterschiedlich einsortieren"}


def which_one_to_use():
    """Nennt die Frage, an der die Wahl hängt.

    Gibt es beschriftete Beispiele, ist überwachtes Lernen möglich; gibt
    es keine und soll auch keine erstellt werden, bleibt unüberwachtes;
    und wenn es keinen Datensatz gibt, sondern eine Umgebung, in der
    Handlungen Folgen haben, ist es bestärkendes Lernen.
    """
    return {"labelled examples exist": "supervised",
            "no labels, only data": "unsupervised",
            "no data, but an environment with consequences":
                "reinforcement",
            "first question": "wer beschriftet, und wie zuverlässig"}
