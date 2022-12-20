"""Public Function: eine eigene Funktion für das Tabellenblatt."""


def net_from_gross(gross, rate=0.19):
    """Rechnet aus einem Bruttobetrag den Nettobetrag.

    Das ist die Art Funktion, für die sich eine eigene Funktion lohnt:
    die Formel ``=Brutto/(1+Satz)`` steht sonst in jeder Zelle und muss
    an jeder geändert werden, wenn der Satz sich ändert.

    Raises:
        ValueError: bei einem Satz von minus eins oder darunter.
    """
    if rate <= -1:
        raise ValueError("der Satz führt zu einer Division durch null")
    return gross / (1.0 + rate)


def by_value(value):
    """Zeigt die Übergabe mit ByVal: die Kopie wird geändert.

    Returns:
        Abbildung mit dem Wert vor und nach dem Aufruf.
    """
    inner = value
    inner += 1
    return {"outside before": value, "inside after": inner,
            "outside after": value, "changed outside": False}


def by_reference(container):
    """Zeigt die Übergabe mit ByRef: das Original wird geändert.

    In VBA ist ByRef die Voreinstellung, anders als in den meisten
    Sprachen, die man daneben lernt. Eine Funktion, die ein Argument
    ändert, ändert damit die Variable des Aufrufers, und das ist die
    Erklärung für einen ganzen Typ von Fehlern, die weit weg von der
    Funktion auffallen.

    Args:
        container: eine änderbare Ablage mit dem Schlüssel ``value``.

    Returns:
        Abbildung mit dem Wert nach dem Aufruf.

    Raises:
        ValueError: wenn der Schlüssel fehlt.
    """
    if "value" not in container:
        raise ValueError("die Ablage braucht den Schlüssel value")
    container["value"] += 1
    return {"value after": container["value"], "changed outside": True,
            "default in VBA": "ByRef"}


def sub_against_function():
    """Trennt Sub und Function.

    Eine Sub tut etwas und gibt nichts zurück; sie steht hinter einer
    Schaltfläche. Eine Function liefert einen Wert und lässt sich deshalb
    in einer Zelle aufrufen. Nur eine Function taucht im Assistenten
    unter den benutzerdefinierten Funktionen auf.
    """
    return {"Sub": {"returns": None, "callable from a cell": False,
                    "typical use": "hinter einer Schaltfläche"},
            "Function": {"returns": "einen Wert",
                         "callable from a cell": True,
                         "typical use": "eine eigene Tabellenfunktion"},
            "the name is the result": "in VBA wird der Rückgabewert der "
                                      "Funktion unter ihrem eigenen Namen "
                                      "zugewiesen"}


def why_a_function_should_not_write_to_cells():
    """Nennt die Einschränkung einer Tabellenfunktion.

    Eine aus einer Zelle aufgerufene Funktion darf das Blatt nicht
    ändern. Sie wird bei jeder Neuberechnung aufgerufen, und wenn sie
    dabei schreibt, löst sie die nächste Neuberechnung aus. Excel weist
    solche Schreibzugriffe deshalb still zurück, und die Funktion liefert
    einen Fehlerwert, ohne dass etwas passiert.
    """
    return {"may not": "Zellen schreiben, Blätter anlegen, formatieren",
            "why": "jede Neuberechnung würde die nächste auslösen",
            "symptom": "die Zelle zeigt einen Fehlerwert und das Blatt "
                       "bleibt unverändert",
            "way out": "eine Sub hinter einer Schaltfläche"}
