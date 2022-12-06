"""Die Bestellannahme des Versandunternehmens, Aufgabe 1 des Tutoriums."""

SHIPPING = (
    (0.0, 100.0, {"Neukunde": "Rechnung", "Altkunde": "Rechnung"}),
    (100.0, 1000.0, {"Neukunde": "Nachnahme", "Altkunde": "Rechnung"}),
    (1000.0, None, {"Neukunde": "Nachnahme", "Altkunde": "Nachnahme"}),
)

STATUS = ("Neukunde", "Altkunde")


def bracket(value):
    """Nennt die Wertstufe einer Bestellung.

    Raises:
        ValueError: bei einem negativen Bestellwert.
    """
    if value < 0:
        raise ValueError("negativer Bestellwert")
    for low, high, _ in SHIPPING:
        if value >= low and (high is None or value < high):
            return (low, high)
    raise ValueError("kein passendes Intervall")


def shipping_kind(value, status):
    """Bestimmt die Versandart aus Bestellwert und Kundenstatus.

    Die Tabelle der Aufgabe in einer Zeile gelesen: unter hundert Euro
    immer auf Rechnung, ab tausend immer per Nachnahme, und dazwischen
    entscheidet der Status. Der Neukunde zahlt per Nachnahme, weil das
    Unternehmen ihn noch nicht kennt.

    Raises:
        ValueError: bei einem negativen Wert oder unbekanntem Status.
    """
    if status not in STATUS:
        raise ValueError("unbekannter Kundenstatus")
    low, high = bracket(value)
    for other_low, other_high, kinds in SHIPPING:
        if (other_low, other_high) == (low, high):
            return kinds[status]
    raise ValueError("kein passendes Intervall")


def decision_table():
    """Gibt die Tabelle der Aufgabe als Abbildung zurück."""
    return {"<100": SHIPPING[0][2], ">=100 <1000": SHIPPING[1][2],
            ">=1000": SHIPPING[2][2]}


def process():
    """Beschreibt den Ablauf als Kette von Schritten.

    Nach dem Eingang wird die Bestellung geprüft. Sind die Unterlagen
    nicht in Ordnung, wird storniert und der Kunde zugleich informiert;
    das ist eine parallele Verzweigung, keine exklusive, weil beides
    geschieht. Sind sie in Ordnung, werden Kundenstatus und Bestellwert
    gleichzeitig ermittelt, wieder parallel, und danach entscheidet die
    Tabelle über die Versandart.

    Returns:
        Abbildung mit den Schritten und den benutzten Konnektoren.
    """
    return {
        "start": "Bestellung ist eingegangen",
        "steps": ["Bestellung prüfen",
                  "XOR: Unterlagen in Ordnung oder nicht",
                  "nicht in Ordnung: AND aus Stornieren und Kunde "
                  "informieren",
                  "in Ordnung: AND aus Kundenstatus ermitteln und "
                  "Bestellwert ermitteln",
                  "Versandart bestimmen",
                  "Versand durchführen"],
        "connectors": {"nach der Prüfung": "XOR",
                       "bei der Stornierung": "AND",
                       "vor der Versandart": "AND"},
        "why the second is AND": "der Kunde wird informiert und die "
                                 "Bestellung storniert, nicht das eine "
                                 "oder das andere",
        "why the third is AND": "Status und Wert werden beide gebraucht, "
                                "um die Versandart zu bestimmen",
    }


def all_cases():
    """Zählt die Fälle der Entscheidungstabelle auf.

    Returns:
        Abbildung von Wertstufe und Status auf die Versandart.
    """
    samples = {"<100": 50.0, ">=100 <1000": 500.0, ">=1000": 1500.0}
    return {(name, status): shipping_kind(value, status)
            for name, value in samples.items() for status in STATUS}


def the_boundaries():
    """Zeigt, dass die Grenzen der Tabelle geschlossen und offen sind.

    Bei genau hundert Euro gilt die mittlere Zeile, bei genau tausend die
    untere: die Tabelle schreibt ``>=100`` und ``>=1000``. Wer die
    Grenzen als ``>`` liest, bekommt für genau diese beiden Werte die
    falsche Versandart, und das sind die Werte, an denen ein Test zuerst
    hinsieht.
    """
    return {99.99: shipping_kind(99.99, "Neukunde"),
            100.0: shipping_kind(100.0, "Neukunde"),
            999.99: shipping_kind(999.99, "Altkunde"),
            1000.0: shipping_kind(1000.0, "Altkunde")}
