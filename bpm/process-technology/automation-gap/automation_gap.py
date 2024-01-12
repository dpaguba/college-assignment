"""Was ein BPMS aus einem fachlichen Modell nicht lesen kann."""

ELEMENTS = {
    "user task": True,
    "service task": True,
    "script task": True,
    "send task": True,
    "receive task": True,
    "business rule task": True,
    "manual task": False,
    "condition with no data": False,
    "unlabelled gateway": False,
    "text annotation": False,
    "activity without a resource": False,
}


def interpretable(element):
    """Sagt, ob ein BPMS mit einem Element etwas anfangen kann.

    Raises:
        ValueError: bei einem unbekannten Element.
    """
    if element not in ELEMENTS:
        raise ValueError("unbekanntes Element")
    return ELEMENTS[element]


def gaps(elements):
    """Trennt die Elemente eines Modells in lesbare und nicht lesbare.

    Raises:
        ValueError: bei einem unbekannten Element.
    """
    readable = [name for name in elements if interpretable(name)]
    return {"interpretable": readable,
            "not interpretable": [name for name in elements
                                  if not interpretable(name)]}


def measure_for(element):
    """Schlägt vor, wie ein nicht lesbares Element behandelt wird.

    Raises:
        ValueError: bei einem unbekannten Element.
    """
    if interpretable(element):
        return "nichts zu tun"
    if element == "manual task":
        return ("als Benutzeraufgabe implementieren, damit der Mensch sie "
                "quittiert, oder isolieren und den Rest automatisieren")
    if element == "condition with no data":
        return "das Datenobjekt ergänzen, das die Bedingung liest"
    if element == "unlabelled gateway":
        return "die Bedingung an den ausgehenden Fluss schreiben"
    if element == "text annotation":
        return "in eine Geschäftsregel oder eine Bedingung überführen"
    return "die ausführende Rolle eintragen"


def loan_application():
    """Der Darlehensprozess aus Tech 1 als Beispiel.

    Die Aufgabe setzt voraus, dass Verträge die Schriftform brauchen. Der
    Postweg und die Unterschrift bleiben damit ausserhalb des Systems;
    sichtbar werden sie nur, wenn jemand ihren Abschluss meldet.

    Returns:
        Abbildung mit den Befunden und den Massnahmen.
    """
    elements = ["user task", "manual task", "service task",
                "condition with no data", "manual task"]
    report = gaps(elements)
    report["measures"] = [
        "die Unterlagen per Post: Schriftform verlangt sie, also bleibt "
        "sie manuell und wird nur quittiert",
        "die fehlenden Datenobjekte für die Bedingungen ergänzen",
        "die Prüfung der Bonität als Dienst aufrufen",
    ]
    report["assumption"] = "elektronische Form ist ausgeschlossen"
    return report


def the_rule():
    """Nennt den Satz, an dem alles hängt.

    Was für das System nicht sichtbar ist, existiert für das System
    nicht. Eine Tätigkeit, die niemand meldet, taucht in keiner Kennzahl
    auf, blockiert aber trotzdem den Fall.
    """
    return {"rule": "if the activity is not visible, it does not exist",
            "two ways out": ["make it a user task",
                             "isolate it and automate the rest"],
            "cost of the first": "somebody has to confirm it by hand"}
