"""Felder in VBA und ihre Eigenheiten."""


def bounds(size, option_base=0):
    """Nennt die Grenzen eines mit ``Dim a(size)`` erklärten Feldes.

    ``Dim a(5)`` erzeugt sechs Elemente, von null bis fünf, weil die
    Zahl in der Klammer die obere Grenze ist und nicht die Länge. Mit
    ``Option Base 1`` sind es fünf, von eins bis fünf. Das ist die
    häufigste Verwechslung im Umgang mit Feldern.

    Args:
        size: die Zahl in der Klammer.
        option_base: null oder eins.

    Returns:
        Abbildung mit unterer und oberer Grenze und der Länge.

    Raises:
        ValueError: bei einer negativen Grösse oder einer anderen Basis
            als null oder eins.
    """
    if size < 0:
        raise ValueError("negative Grösse")
    if option_base not in (0, 1):
        raise ValueError("Option Base ist null oder eins")
    return {"lower": option_base, "upper": size,
            "length": size - option_base + 1,
            "note": "die Zahl in der Klammer ist die obere Grenze"}


def explicit_bounds(lower, upper):
    """Nennt die Grenzen bei ``Dim a(lower To upper)``.

    Die ausdrückliche Form ist die einzige, die unabhängig von Option
    Base dasselbe bedeutet, und deshalb die einzige, die man in fremdem
    Code ohne Nachsehen lesen kann.

    Raises:
        ValueError: wenn die untere Grenze über der oberen liegt.
    """
    if lower > upper:
        raise ValueError("die untere Grenze liegt über der oberen")
    return {"lower": lower, "upper": upper, "length": upper - lower + 1,
            "independent of Option Base": True}


def redim_preserve(values, new_upper, option_base=0):
    """Bildet ``ReDim Preserve`` nach.

    Die Anweisung ändert die Grösse und behält die Werte. Beim Verkleinern
    gehen die hinteren verloren, und zwar ohne Warnung; beim Vergrössern
    kommen leere Elemente hinzu.

    Args:
        values: die bisherigen Werte.
        new_upper: die neue obere Grenze.
        option_base: null oder eins.

    Returns:
        Abbildung mit den neuen Werten und dem, was verloren ging.

    Raises:
        ValueError: bei einer oberen Grenze unter der Basis.
    """
    if new_upper < option_base - 1:
        raise ValueError("die obere Grenze liegt unter der Basis")
    length = new_upper - option_base + 1
    kept = list(values[:length])
    lost = list(values[length:])
    while len(kept) < length:
        kept.append(None)
    return {"values": kept, "lost": lost, "length": length,
            "warning": "das Verkleinern verwirft ohne Meldung"}


def only_the_last_dimension():
    """Nennt die Einschränkung von ReDim Preserve.

    Bei einem mehrdimensionalen Feld darf nur die letzte Dimension
    geändert werden. Der Grund liegt in der Ablage: die Werte stehen
    hintereinander im Speicher, und eine Änderung an einer vorderen
    Dimension würde jeden Wert an eine andere Stelle schieben.
    """
    return {"allowed": "nur die letzte Dimension",
            "why": "die Werte liegen hintereinander, eine vordere "
                   "Dimension zu ändern verschiebt alle",
            "without Preserve": "jede Dimension, aber die Werte gehen "
                                "verloren"}


def average(values):
    """Rechnet den Mittelwert über ein Feld aus.

    Raises:
        ValueError: bei einem leeren Feld.
    """
    numbers = [value for value in values if value is not None]
    if not numbers:
        raise ValueError("leeres Feld")
    return sum(numbers) / len(numbers)


def largest(values):
    """Sucht den grössten Wert und seine Stelle.

    Die Schleife über ein Feld ist die Aufgabe des dreizehnten
    Tutoriums, und der übliche Fehler steckt im Anfangswert: wer mit null
    beginnt statt mit dem ersten Element, findet in einem Feld aus lauter
    negativen Zahlen die Null, die gar nicht darin steht.

    Returns:
        Abbildung mit dem Wert und seiner Stelle.

    Raises:
        ValueError: bei einem leeren Feld.
    """
    numbers = [value for value in values if value is not None]
    if not numbers:
        raise ValueError("leeres Feld")
    best = numbers[0]
    where = 0
    for index, value in enumerate(numbers):
        if value > best:
            best, where = value, index
    return {"value": best, "index": where,
            "trap": "ein Anfangswert von null findet in lauter negativen "
                    "Zahlen die Null"}
