"""Die Einteilung der Verfahren für Analysen in Echtzeit."""

CLASSES = {
    "batch": {"latency": "Stunden bis Tage",
              "sees": "alle Daten des Zeitraums",
              "typical": "der nächtliche Lauf"},
    "micro batch": {"latency": "Sekunden bis Minuten",
                    "sees": "ein Fenster",
                    "typical": "alle fünf Minuten neu rechnen"},
    "stream": {"latency": "Millisekunden",
               "sees": "einen Satz nach dem anderen",
               "typical": "die laufende Auswertung eines Ereignisstroms"},
}


def classes():
    """Nennt die drei Klassen von schnell nach langsam."""
    return ["stream", "micro batch", "batch"]


def describe(name):
    """Beschreibt eine Klasse.

    Raises:
        ValueError: bei einer unbekannten Klasse.
    """
    if name not in CLASSES:
        raise ValueError("unbekannte Klasse")
    return dict(CLASSES[name])


def choose(latency_seconds, needs_history=False):
    """Wählt eine Klasse anhand der geforderten Verzögerung.

    Raises:
        ValueError: bei einer negativen Verzögerung.
    """
    if latency_seconds < 0:
        raise ValueError("negative Verzögerung")
    if needs_history and latency_seconds >= 3600:
        return {"class": "batch", "why": "die Rechnung braucht die "
                                         "ganze Geschichte und hat Zeit"}
    if latency_seconds < 1:
        return {"class": "stream", "why": "unter einer Sekunde bleibt nur "
                                          "der Strom"}
    if latency_seconds < 300:
        return {"class": "micro batch",
                "why": "Fenster sind einfacher als ein echter Strom und "
                       "reichen bis in den Minutenbereich"}
    return {"class": "batch", "why": "ab Minuten lohnt der Aufwand des "
                                     "Stroms nicht"}


def freshness_against_completeness():
    """Nennt den Zielkonflikt, um den es geht.

    Wer sofort antwortet, antwortet auf unvollständigen Daten: was noch
    unterwegs ist, fehlt. Wer wartet, bis alles da ist, antwortet spät.
    Dazwischen gibt es keinen freien Mittelweg, sondern nur die
    Entscheidung, wie viel Unvollständigkeit die Antwort verträgt.

    Bei verspätet eintreffenden Sätzen kommt hinzu, dass eine schon
    gegebene Antwort nachträglich falsch wird, und dann ist die Frage,
    ob sie widerrufen werden kann.
    """
    return {"immediate": "unvollständig",
            "complete": "spät",
            "no middle": "die Entscheidung ist, wie viel Lücke die "
                         "Antwort verträgt",
            "late arrivals": "eine gegebene Antwort wird nachträglich "
                             "falsch",
            "the question then": "kann sie widerrufen werden"}


def window_count(duration, window, slide=None):
    """Zählt, in wie vielen Fenstern ein Satz vorkommt.

    Bei überlappenden Fenstern zählt jeder Satz mehrfach, und wer die
    Ergebnisse der Fenster addiert, zählt ihn entsprechend oft. Das ist
    dieselbe Falle wie bei einer nicht additiven Kennzahl, nur über die
    Zeit.

    Args:
        duration: die Länge des Stroms.
        window: die Länge eines Fensters.
        slide: der Abstand zweier Fenster; ohne Angabe gleich der Länge.

    Returns:
        Abbildung mit der Zahl der Fenster und der Mehrfachzählung.

    Raises:
        ValueError: bei nicht positiven Angaben.
    """
    if duration <= 0 or window <= 0:
        raise ValueError("Länge und Fenster müssen positiv sein")
    slide = window if slide is None else slide
    if slide <= 0:
        raise ValueError("der Abstand muss positiv sein")
    windows = int(duration / slide)
    per_record = max(1, int(window / slide))
    return {"windows": windows, "each record appears in": per_record,
            "overlapping": slide < window,
            "warning": "die Summe über überlappende Fenster zählt jeden "
                       "Satz mehrfach"}


def why_the_class_is_a_cost_decision():
    """Sagt, woran die Wahl wirklich hängt.

    Ein Strom ist nicht schwerer zu rechnen als ein Stapel; er ist
    schwerer zu betreiben. Zustand über die Zeit, Wiederanlauf nach
    einem Ausfall, verspätete Sätze und die Frage, ob eine Antwort
    genau einmal gezählt wird, kosten alle Betrieb und keine Rechenzeit.
    Deshalb ist die Wahl der Klasse eine Frage der Kosten und nicht der
    Technik.
    """
    return {"harder about a stream": ["Zustand über die Zeit",
                                      "Wiederanlauf",
                                      "verspätete Sätze",
                                      "genau einmal zählen"],
            "not harder": "die Rechnung selbst",
            "so": "die Wahl ist eine Kostenfrage"}
