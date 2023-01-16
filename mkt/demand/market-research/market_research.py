"""Marketingforschung: Verfahren, Skalen und die üblichen Fehler."""

METHODS = {
    "Befragung": {"gets": "Meinungen, Absichten, Begründungen",
                  "risk": "gesagt ist nicht getan"},
    "Beobachtung": {"gets": "tatsächliches Verhalten",
                    "risk": "das Warum bleibt offen"},
    "Experiment": {"gets": "eine Ursache-Wirkungs-Aussage",
                   "risk": "künstliche Lage, teuer"},
    "Panel": {"gets": "Veränderung über die Zeit bei denselben Personen",
              "risk": "Panelsterblichkeit und Gewöhnung"},
}

SCALES = {
    "nominal": {"allows": "Gleichheit", "example": "Geschlecht, Marke",
                "mean": False},
    "ordinal": {"allows": "Rangfolge", "example": "Schulnote, Rangliste",
                "mean": False},
    "intervall": {"allows": "Abstände", "example": "Temperatur in Celsius",
                  "mean": True},
    "ratio": {"allows": "Verhältnisse und einen echten Nullpunkt",
              "example": "Umsatz, Alter", "mean": True},
}


def methods():
    """Nennt die Erhebungsverfahren mit ihrem Ertrag und ihrem Risiko."""
    return {name: dict(row) for name, row in METHODS.items()}


def scales():
    """Nennt die vier Skalenniveaus."""
    return {name: dict(row) for name, row in SCALES.items()}


def mean_allowed(scale):
    """Sagt, ob ein Mittelwert auf dieser Skala sinnvoll ist.

    Auf einer Ordinalskala ist er es nicht: der Abstand zwischen den
    Rängen ist unbekannt, also hat die Summe keine Bedeutung. Der
    Mittelwert von Schulnoten wird trotzdem überall gebildet, und die
    Vorlesung nennt ihn als Beispiel für einen Fehler, der sich
    eingebürgert hat.

    Raises:
        ValueError: bei einem unbekannten Skalenniveau.
    """
    if scale not in SCALES:
        raise ValueError("unbekanntes Skalenniveau")
    return SCALES[scale]["mean"]


def sample_error(size, share=0.5, confidence=1.96):
    """Der Stichprobenfehler bei einem Anteil.

    Er fällt mit der Wurzel der Stichprobengrösse: für die halbe
    Fehlerbreite braucht es die vierfache Stichprobe. Und er hängt nicht
    von der Grundgesamtheit ab, solange sie gross gegen die Stichprobe
    ist; das überrascht regelmässig und ist der Grund, warum tausend
    Befragte für ein Land genügen.

    Raises:
        ValueError: bei einer nicht positiven Grösse oder einem Anteil
            ausserhalb von null bis eins.
    """
    if size < 1:
        raise ValueError("die Stichprobe muss positiv sein")
    if not 0 <= share <= 1:
        raise ValueError("Anteil ausserhalb von 0 bis 1")
    return confidence * (share * (1 - share) / size) ** 0.5


def needed_size(margin, share=0.5, confidence=1.96):
    """Die Stichprobe, die für eine gewünschte Fehlerbreite nötig ist.

    Raises:
        ValueError: bei einer nicht positiven Fehlerbreite.
    """
    if margin <= 0:
        raise ValueError("die Fehlerbreite muss positiv sein")
    return int((confidence ** 2 * share * (1 - share)) / margin ** 2) + 1


def the_square_root_law(sizes=(250, 1000, 4000, 16000)):
    """Zeigt, wie langsam der Fehler mit der Stichprobe fällt.

    Returns:
        Abbildung von der Grösse auf die Fehlerbreite.
    """
    return {size: round(sample_error(size) * 100, 3) for size in sizes}


def common_mistakes():
    """Nennt die Fehler, die die Vorlesung aufzählt.

    Eine Frage, die die Antwort schon enthält; eine Skala ohne Mitte oder
    mit zu vielen Stufen; eine Stichprobe, die sich selbst auswählt; und
    die Verwechslung von Absicht und Verhalten. Der letzte ist der
    teuerste: Befragte sagen zuverlässig, dass sie ein neues Produkt
    kaufen würden, und tun es dann nicht.
    """
    return ["die Frage enthält die Antwort",
            "die Skala hat keine Mitte oder zu viele Stufen",
            "die Stichprobe wählt sich selbst aus",
            "Absicht wird für Verhalten gehalten",
            "der letzte kostet am meisten"]
