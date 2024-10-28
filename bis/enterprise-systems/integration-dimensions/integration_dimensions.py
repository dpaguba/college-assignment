"""Die fünf Dimensionen der Integration der Informationsverarbeitung."""

DIMENSIONS = {
    "Integrationsgegenstand": ["Daten", "Funktionen", "Objekte", "Prozesse",
                               "Methoden", "Programme"],
    "Integrationsrichtung": ["horizontal", "vertikal"],
    "Integrationsreichweite": ["bereichsumfassend",
                               "funktionsbereichs- und "
                               "prozessübergreifend", "innerbetrieblich",
                               "zwischenbetrieblich"],
    "Automationsgrad": ["Vollautomation", "Teilautomation"],
    "Integrationszeitpunkt": ["Stapel", "Echtzeit"],
}

MEANING = {
    "Daten": "gemeinsame Nutzung derselben Daten",
    "Funktionen": "Ressourcen für gleichartige oder anspruchsvollere "
                  "Aufgaben freisetzen",
    "Objekte": "aufgabenträgerorientierte Funktions- und Datenintegration",
    "Prozesse": "im Zentrum steht der zu integrierende Geschäftsprozess",
    "Methoden": "dieselben Methoden in unterschiedlichen Funktionen",
    "Programme": "Abstimmung einzelner Softwarebausteine",
    "horizontal": "entlang des Prozesses, über Funktionsbereiche hinweg",
    "vertikal": "über die Ebenen der Pyramide, von der Transaktion bis "
                "zur Führungskennzahl",
    "Stapel": "die Daten fliessen gebündelt, meist nachts",
    "Echtzeit": "die Daten fliessen sofort",
}


def dimensions():
    """Nennt die fünf Dimensionen."""
    return sorted(DIMENSIONS)


def values(dimension):
    """Nennt die Ausprägungen einer Dimension.

    Raises:
        ValueError: bei einer unbekannten Dimension.
    """
    if dimension not in DIMENSIONS:
        raise ValueError("unbekannte Dimension")
    return list(DIMENSIONS[dimension])


def explain(value):
    """Erklärt eine Ausprägung.

    Raises:
        ValueError: bei einer unbekannten Ausprägung.
    """
    if value not in MEANING:
        raise ValueError("unbekannte Ausprägung")
    return MEANING[value]


def definition():
    """Gibt die Definition der Vorlesung wieder.

    Integration bezeichnet die Verknüpfung von Menschen, Aufgaben und
    Technik zu einem einheitlichen Ganzen, um den Folgen der durch
    Arbeitsteilung und Spezialisierung entstandenen Funktions-, Prozess-
    und Abteilungsgrenzen entgegenzuwirken.
    """
    return {"links": ["Menschen", "Aufgaben", "Technik"],
            "against": ["Funktionsgrenzen", "Prozessgrenzen",
                        "Abteilungsgrenzen"],
            "cause of the borders": "Arbeitsteilung und Spezialisierung"}


def why_the_borders_exist():
    """Sagt, warum die Grenzen überhaupt da sind.

    Sie sind kein Versehen, sondern das Ergebnis von Arbeitsteilung, und
    Arbeitsteilung ist der Grund, warum ein Unternehmen mehr schafft als
    eine Person. Integration hebt die Grenzen deshalb nicht auf, sondern
    macht sie durchlässig für Daten und Prozesse.
    """
    return {"borders come from": "die Arbeitsteilung, die produktiv macht",
            "integration does not": "die Arbeitsteilung rückgängig machen",
            "integration does": "die Grenzen für Daten und Prozesse "
                                "durchlässig machen"}
