"""Die sieben Aufgabentypen und was sich davon automatisieren lässt."""

TYPES = {
    "send": {"person": False, "system": True,
             "does": "schickt eine Nachricht an einen anderen Beteiligten"},
    "receive": {"person": False, "system": True,
                "does": "wartet auf eine Nachricht"},
    "user": {"person": True, "system": True,
             "does": "ein Mensch arbeitet in einer Anwendung"},
    "manual": {"person": True, "system": False,
               "does": "ein Mensch arbeitet ohne jede Anwendung"},
    "script": {"person": False, "system": True,
               "does": "die Maschine führt ein Skript aus"},
    "service": {"person": False, "system": True,
                "does": "ein Dienst wird aufgerufen"},
    "business rule": {"person": False, "system": True,
                      "does": "eine Entscheidungstabelle wird ausgewertet"},
}


def describe(name):
    """Beschreibt einen Aufgabentyp.

    Raises:
        ValueError: bei einem unbekannten Typ.
    """
    if name not in TYPES:
        raise ValueError("unbekannter Aufgabentyp")
    return dict(TYPES[name])


def needs_a_person(name):
    """Sagt, ob ein Mensch die Aufgabe ausführt.

    Raises:
        ValueError: bei einem unbekannten Typ.
    """
    return describe(name)["person"]


def automatable():
    """Nennt die Typen, die ohne Menschen auskommen.

    Das Empfangen bleibt aussen vor: die Maschine wartet zwar allein, aber
    ob die Nachricht kommt, entscheidet der andere Beteiligte.
    """
    return sorted(name for name, row in TYPES.items()
                  if not row["person"] and name != "receive")


def invisible_to_the_system():
    """Nennt die Typen, von denen ein BPMS nichts mitbekommt.

    Nur die manuelle Aufgabe: sie läuft ohne Anwendung, also gibt es
    nichts, was ein System beobachten könnte. Wenn eine Tätigkeit nicht
    sichtbar ist, existiert sie für das BPMS nicht.
    """
    return sorted(name for name, row in TYPES.items() if not row["system"])


def make_visible(name):
    """Schlägt vor, wie eine unsichtbare Aufgabe sichtbar wird.

    Zwei Wege: die Tätigkeit wird zur Benutzeraufgabe, dann meldet der
    Mensch sie im System an und ab; oder sie wird herausgelöst und der
    Rest des Prozesses läuft automatisiert weiter, während sie daneben
    stattfindet.

    Raises:
        ValueError: bei einem unbekannten Typ.
    """
    row = describe(name)
    if row["system"]:
        return {"already visible": True, "measure": None}
    return {"already visible": False,
            "measure": ["als Benutzeraufgabe implementieren",
                        "isolieren und den Rest automatisieren"],
            "price": "der Mensch muss die Aufgabe quittieren"}
