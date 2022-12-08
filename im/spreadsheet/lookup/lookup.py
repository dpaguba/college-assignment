"""Die Verweisfunktion in ihren zwei Betriebsarten."""

SHIPPING = ((0.0, "Rechnung"), (100.0, "Nachnahme"),
            (1000.0, "Nachnahme"))

ARTICLES = ((1, "2er Sofa Leder", 499.90), (2, "Sessel Leder", 399.90),
            (3, "Schlafsofa", 549.98), (4, "Couchtisch klein", 129.49),
            (5, "Couchtisch Glas", 329.98))


def exact(table, key, column, key_column=0):
    """Sucht eine Zeile mit genau diesem Schlüssel.

    Das entspricht SVERWEIS mit dem vierten Argument FALSCH. Die Tabelle
    muss nicht sortiert sein, und ein fehlender Schlüssel ist ein Fehler
    und kein stiller Nachbarwert.

    Raises:
        ValueError: bei einer leeren Tabelle, einer unbekannten Spalte
            oder einem Schlüssel, den es nicht gibt.
    """
    if not table:
        raise ValueError("leere Tabelle")
    if not 0 <= column < len(table[0]):
        raise ValueError("unbekannte Spalte")
    for row in table:
        if row[key_column] == key:
            return row[column]
    raise ValueError("kein Eintrag für %r" % (key,))


def approximate(table, key, column, key_column=0):
    """Sucht den letzten Eintrag, der nicht über dem Schlüssel liegt.

    Das entspricht SVERWEIS mit WAHR und ist der Fall, für den die
    Funktion eigentlich gemacht ist: Staffeln, Steuerklassen,
    Notenspiegel. Die Tabelle muss aufsteigend sortiert sein, sonst
    liefert die Suche einen Wert, der aussieht wie eine Antwort.

    Raises:
        ValueError: bei einer leeren oder unsortierten Tabelle oder wenn
            der Schlüssel unter dem ersten Eintrag liegt.
    """
    if not table:
        raise ValueError("leere Tabelle")
    keys = [row[key_column] for row in table]
    if keys != sorted(keys):
        raise ValueError("die Tabelle ist nicht aufsteigend sortiert")
    if key < keys[0]:
        raise ValueError("der Schlüssel liegt unter dem ersten Eintrag")
    found = table[0]
    for row in table:
        if row[key_column] <= key:
            found = row
        else:
            break
    return found[column]


def shipping_for(value):
    """Bestimmt die Versandart über eine Staffel.

    Raises:
        ValueError: bei einem negativen Wert.
    """
    if value < 0:
        raise ValueError("negativer Wert")
    return approximate(SHIPPING, value, 1)


def price_of(number):
    """Sucht den Preis eines Artikels über die Artikelnummer.

    Raises:
        ValueError: bei einer unbekannten Artikelnummer.
    """
    return exact(ARTICLES, number, 2)


def unsorted_gives_a_wrong_answer():
    """Zeigt, was die ungefähre Suche in einer unsortierten Tabelle tut.

    Die Funktion sucht von oben und hört auf, sobald ein Eintrag über dem
    Schlüssel liegt. In einer unsortierten Tabelle steht der passende
    Eintrag womöglich dahinter und wird nie erreicht. Hier wird das
    abgefangen und gemeldet; die Tabellenkalkulation meldet nichts,
    sondern liefert den Wert der Zeile, bei der sie stehen geblieben ist.

    Returns:
        Abbildung mit der Fehlermeldung und dem, was ohne Prüfung
        herauskäme.
    """
    jumbled = ((1000.0, "Nachnahme"), (0.0, "Rechnung"),
               (100.0, "Nachnahme"))
    try:
        approximate(jumbled, 500.0, 1)
        message = None
    except ValueError as problem:
        message = str(problem)
    without_check = jumbled[0][1]
    return {"rejected": message,
            "what a spreadsheet would return": without_check,
            "correct answer": shipping_for(500.0),
            "why": "die Suche hört beim ersten grösseren Eintrag auf"}


def when_to_use_which():
    """Nennt die Regel für die Wahl der Betriebsart.

    Genaue Suche für Schlüssel: Artikelnummer, Kundennummer,
    Matrikelnummer. Ungefähre Suche für Staffeln, in denen ein Bereich
    auf einen Wert abgebildet wird. Wer die ungefähre Suche für Schlüssel
    benutzt, bekommt bei einem fehlenden Schlüssel den Nachbarn, und das
    ist der stillste Fehler, den eine Tabelle machen kann.
    """
    return {"exact": "Schlüssel, die es entweder gibt oder nicht",
            "approximate": "Staffeln und Klassen",
            "default in Excel": "WAHR, also die ungefähre Suche",
            "advice": "bei Schlüsseln immer FALSCH angeben"}
