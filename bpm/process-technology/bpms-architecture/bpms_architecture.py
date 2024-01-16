"""Die Bestandteile eines Business Process Management System."""

COMPONENTS = {
    "process modelling tool": {
        "does": "Modelle erfassen und für die Ausführung annotieren",
        "talks to": ["analyst", "execution engine"]},
    "execution engine": {
        "does": "Instanzen anlegen, Marken bewegen, Aufgaben verteilen",
        "talks to": ["worklist handler", "external services",
                     "administration and monitoring"]},
    "worklist handler": {
        "does": "die anstehenden Aufgaben je Rolle anzeigen und annehmen",
        "talks to": ["user", "execution engine"]},
    "administration and monitoring": {
        "does": "laufende Instanzen beobachten, eingreifen, auswerten",
        "talks to": ["administrator", "execution engine"]},
    "external services": {
        "does": "das, was der Prozess selbst nicht kann",
        "talks to": ["execution engine"]},
}


def components():
    """Nennt die Bestandteile, alphabetisch."""
    return sorted(COMPONENTS)


def centre():
    """Nennt den Bestandteil, an dem alle anderen hängen.

    Die Ausführungsmaschine hält den Zustand jeder Instanz. Alles andere
    schreibt hinein oder liest heraus; ohne sie gibt es keinen laufenden
    Prozess, sondern nur Bilder davon.
    """
    return "execution engine"


def describe(name):
    """Beschreibt einen Bestandteil.

    Raises:
        ValueError: bei einem unbekannten Bestandteil.
    """
    if name not in COMPONENTS:
        raise ValueError("unbekannter Bestandteil")
    return dict(COMPONENTS[name])


def external_services():
    """Nennt Beispiele für Dienste, die von aussen dazukommen."""
    return ["ein Zahlungsdienstleister",
            "eine Bonitätsauskunft",
            "der Versand von E-Mail",
            "ein Dokumentenarchiv",
            "das Buchhaltungssystem"]


def what_it_is_not():
    """Grenzt das BPMS gegen benachbarte Systeme ab.

    Es führt Prozesse aus und hält keine Stammdaten; die liegen im ERP.
    Es ruft Dienste auf und ersetzt sie nicht. Und es ist kein
    Zeichenwerkzeug: ein Modell, das nur gezeichnet wurde, läuft
    nirgendwo.
    """
    return {"not an ERP": "the master data lives elsewhere",
            "not the services": "it orchestrates, it does not compute",
            "not a drawing tool": "a drawn model is not an executable one"}
