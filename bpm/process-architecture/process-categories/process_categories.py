"""Prozesskategorien nach dem Wertkettenmodell von Porter."""

CATEGORIES = ("management", "core", "support")

EXERCISE = {
    "Projekte planen": "management",
    "Budget verwalten": "support",
    "Testing durchführen": "core",
    "Strategie entwickeln": "management",
    "Kunden betreuen": "core",
    "Buchhaltung durchführen": "support",
    "Daten analysieren": "core",
    "Software entwickeln": "core",
    "Daten erfassen": "core",
    "Risiko steuern": "management",
    "Personal verwalten": "support",
    "Dokumente erstellen": "support",
}

DESCRIPTION = {
    "management": "Richtlinien, Regeln und Verfahrensweisen: strategische "
                  "Planung, Budgetierung, Compliance und Risiko",
    "core": "die wesentliche Wertschöpfung: Entwicklung, Fertigung, "
            "Marketing, Vertrieb, Lieferung, Kundenbetreuung",
    "support": "ermöglichen die Kernprozesse: indirekte Beschaffung, "
               "Personal, IT, Rechnungswesen, Recht",
}


def categories():
    """Nennt die drei Kategorien von oben nach unten."""
    return list(CATEGORIES)


def porter():
    """Vergleicht den ursprünglichen und den heutigen Ansatz.

    Porter unterschied zunächst nur Kern- und Unterstützungsprozesse. Der
    Drei-Prozess-Ansatz zieht die Managementprozesse als eigene Schicht
    heraus, weil sie weder Wert schöpfen noch die Wertschöpfung
    unterstützen, sondern sie steuern.
    """
    return {"original": 2, "today": 3,
            "added": "management",
            "why": "steering is neither producing nor supporting"}


def describe(category):
    """Beschreibt eine Kategorie.

    Raises:
        ValueError: bei einer unbekannten Kategorie.
    """
    if category not in DESCRIPTION:
        raise ValueError("unbekannte Kategorie")
    return DESCRIPTION[category]


def classify(process):
    """Ordnet einen Prozess der Übung einer Kategorie zu.

    Raises:
        ValueError: bei einem Prozess, der nicht in der Übung steht.
    """
    if process not in EXERCISE:
        raise ValueError("unbekannter Prozess")
    return EXERCISE[process]


def architecture():
    """Zeichnet die Prozessarchitektur der Übung als drei Schichten.

    Die Reihenfolge der Schichten ist die des Bildes: Management oben,
    Kern in der Mitte, Unterstützung unten.

    Returns:
        Abbildung von der Kategorie auf die Prozesse, alphabetisch.
    """
    drawing = {category: [] for category in CATEGORIES}
    for process in sorted(EXERCISE):
        drawing[EXERCISE[process]].append(process)
    return drawing


def why_the_border_is_argued():
    """Nennt, warum die Zuordnung nicht eindeutig ist.

    Ob ein Prozess zum Kern gehört, hängt vom Geschäft ab und nicht vom
    Namen: die Buchhaltung eines Softwarehauses unterstützt, die
    Buchhaltung eines Steuerberaters ist sein Produkt.
    """
    return {"depends on": "the business, not the name",
            "example": "bookkeeping is support in a software house and "
                       "core in a tax practice",
            "consequence": "the map has to be agreed with the people who "
                           "run the processes"}
