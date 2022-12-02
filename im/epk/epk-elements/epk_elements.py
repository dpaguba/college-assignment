"""Die Bausteine der ereignisgesteuerten Prozesskette."""

ELEMENTS = {
    "Ereignis": {"shape": "Sechseck", "passive": True,
                 "means": "ein eingetretener Zustand, der etwas auslöst "
                          "oder das Ergebnis einer Funktion ist"},
    "Funktion": {"shape": "abgerundetes Rechteck", "passive": False,
                 "means": "eine Tätigkeit, die Zeit und Ressourcen "
                          "verbraucht"},
    "Konnektor": {"shape": "Kreis mit Zeichen", "passive": True,
                  "means": "verzweigt oder führt den Kontrollfluss "
                           "zusammen"},
    "Kontrollfluss": {"shape": "gerichtete Kante", "passive": True,
                      "means": "die zeitlich-logische Abfolge"},
}

EXTENSIONS = {
    "Organisationseinheit": "wer die Funktion ausführt",
    "Informationsobjekt": "welche Daten die Funktion liest oder schreibt",
    "Anwendungssystem": "welches System sie unterstützt",
}


def elements():
    """Nennt die vier Bausteine der reinen EPK."""
    return dict(ELEMENTS)


def describe(name):
    """Beschreibt einen Baustein.

    Raises:
        ValueError: bei einem unbekannten Baustein.
    """
    if name in ELEMENTS:
        return dict(ELEMENTS[name])
    if name in EXTENSIONS:
        return {"shape": "Anhang an eine Funktion", "passive": True,
                "means": EXTENSIONS[name]}
    raise ValueError("unbekannter Baustein")


def is_active(name):
    """Sagt, ob ein Baustein etwas tut.

    Nur die Funktion tut etwas. Das Ereignis stellt fest, dass etwas der
    Fall ist, und der Konnektor ordnet. Aus dieser einen Unterscheidung
    folgen fast alle Regeln der Notation.

    Raises:
        ValueError: bei einem unbekannten Baustein.
    """
    return not describe(name)["passive"]


def extended():
    """Nennt die Erweiterungen der eEPK.

    Die reine EPK zeigt nur den Ablauf. Die erweiterte hängt an jede
    Funktion, wer sie ausführt, welche Daten sie berührt und welches
    System sie trägt; damit wird aus einem Ablaufbild eine Grundlage für
    die Einführung eines Systems.
    """
    return dict(EXTENSIONS)


def why_events_alternate_with_functions():
    """Erklärt die Grundregel der Notation.

    Ein Ereignis beschreibt einen Zustand, eine Funktion einen Übergang.
    Zwei Zustände hintereinander wären ohne Übergang dazwischen, zwei
    Funktionen ohne Zustand: in beiden Fällen fehlt die Hälfte der
    Geschichte. Deshalb wechseln sich beide entlang des Kontrollflusses ab.
    """
    return {"Ereignis": "Zustand", "Funktion": "Übergang",
            "rule": "sie wechseln sich entlang des Kontrollflusses ab",
            "connectors do not count": "ein Konnektor steht zwischen "
                                       "beiden und unterbricht die "
                                       "Abwechslung nicht"}
