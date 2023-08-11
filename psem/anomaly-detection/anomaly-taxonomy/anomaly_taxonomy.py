"""Die Einteilung der Anomalien nach Chandola, Banerjee und Kumar."""

KINDS = {
    "point": "ein einzelner Wert fällt gegenüber allen anderen auf",
    "contextual": "ein Wert fällt nur in seinem Zusammenhang auf, etwa "
                  "zur falschen Jahreszeit",
    "collective": "erst eine Folge von Werten fällt auf, keiner davon "
                  "einzeln",
}

SETTINGS = {
    "supervised": "beschriftete Beispiele für normal und anomal",
    "semi supervised": "beschriftete Beispiele nur für normal",
    "unsupervised": "keine Beschriftungen, die Annahme ist, dass "
                    "Anomalien selten sind",
}


def kinds():
    """Nennt die drei Arten von Anomalien."""
    return dict(KINDS)


def settings():
    """Nennt die drei Ausgangslagen nach der Verfügbarkeit von Labeln."""
    return dict(SETTINGS)


def classify(description):
    """Ordnet eine Beschreibung einer Art zu.

    Raises:
        ValueError: wenn keine Art passt.
    """
    lowered = str(description).lower()
    if any(word in lowered for word in ("folge", "sequenz", "muster",
                                        "über die zeit")):
        return "collective"
    if any(word in lowered for word in ("kontext", "jahreszeit",
                                        "tageszeit", "für diesen")):
        return "contextual"
    if any(word in lowered for word in ("einzeln", "wert", "ausreisser",
                                        "betrag")):
        return "point"
    raise ValueError("die Beschreibung passt zu keiner Art")


def examples():
    """Gibt je Art ein Beispiel aus dem betrieblichen Umfeld."""
    return {"point": "eine Überweisung über hunderttausend Euro auf einem "
                     "Konto mit sonst dreistelligen Beträgen",
            "contextual": "ein Stromverbrauch, der im Januar normal wäre "
                          "und im Juli nicht",
            "collective": "eine Folge kleiner Abbuchungen, von denen "
                          "keine einzeln auffällt"}


def why_the_kind_decides_the_method():
    """Sagt, warum die Einteilung am Anfang steht.

    Ein Verfahren für Punktanomalien sieht eine kontextuelle nicht, weil
    es den Zusammenhang gar nicht kennt, und es sieht eine kollektive
    nicht, weil es jeden Wert einzeln betrachtet. Wer die Art nicht
    bestimmt, wählt das Verfahren zufällig und misst dann, dass es nicht
    funktioniert.
    """
    return {"point": "Schwellen, Abstände, Dichte",
            "contextual": "erst den Kontext modellieren, dann die "
                          "Abweichung darin",
            "collective": "über Folgen arbeiten: Fenster, Modelle der "
                          "Reihenfolge",
            "mistake": "ein Punktverfahren auf eine kollektive Anomalie "
                       "ansetzen und schliessen, es gebe keine"}


def the_hard_part():
    """Nennt, was die Aufgabe in der Praxis schwierig macht.

    Die Grenze zwischen normal und anomal ist selten scharf, das
    Normale ändert sich mit der Zeit, Anomalien sind selten und deshalb
    schlecht beschriftet, und ein Angreifer richtet sich gerade danach,
    normal auszusehen. Der Survey nennt das an den Anfang, und es ist
    der Grund, warum die Kennzahlen bei niedriger Grundrate so trügen.
    """
    return ["die Grenze ist unscharf",
            "das Normale wandert",
            "Anomalien sind selten und schlecht beschriftet",
            "wer entdeckt werden will, sieht normal aus",
            "die Grundrate macht die Genauigkeit unbrauchbar"]
