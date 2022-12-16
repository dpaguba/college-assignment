"""Bedingte Anweisungen und die Adressierung über Offset."""

SEATS = 20


def tutorials_needed(students, seats=SEATS, share=1.0):
    """Aufgabe 11: wie viele Tutorien angeboten werden.

    Früher wurden nur voll belegte Tutorien angeboten, also ganze
    Zwanzigergruppen. Jetzt genügt eine Belegung von der Hälfte, also
    zählt eine angefangene Gruppe mit, sobald genug Studierende für den
    Anteil übrig sind.

    Args:
        students: die Zahl der Zugelassenen.
        seats: die Plätze je Tutorium.
        share: der geforderte Anteil der Belegung.

    Returns:
        Abbildung mit der Zahl der Tutorien, dem Rest, den leer
        bleibenden Plätzen und den Studierenden ohne Platz. Unter der
        alten Regel ist die zweite Zahl der eigentliche Befund: wer im
        Rest steht, bekommt kein Tutorium.

    Raises:
        ValueError: bei negativen Studierenden, nicht positiven Plätzen
            oder einem Anteil ausserhalb von null bis eins.
    """
    if students < 0:
        raise ValueError("negative Zahl von Studierenden")
    if seats < 1:
        raise ValueError("mindestens ein Platz je Tutorium")
    if not 0 < share <= 1:
        raise ValueError("der Anteil liegt ausserhalb von 0 bis 1")
    full, rest = divmod(students, seats)
    extra = 1 if rest >= seats * share else 0
    offered = (full + extra) * seats
    return {"tutorials": full + extra, "full": full, "rest": rest,
            "extra opened": bool(extra),
            "seats left empty": max(0, offered - students),
            "students without a place": max(0, students - offered)}


def offset(cell, rows, columns):
    """Bildet ``Range(cell).Offset(rows, columns)`` nach.

    Offset zählt von der Zelle aus, nicht vom Blattanfang, und die
    Zählung beginnt bei null: ``Offset(0, 0)`` ist die Zelle selbst. Das
    ist die häufigste Verwechslung, weil Zeilen und Spalten sonst bei
    eins beginnen.

    Args:
        cell: die Ausgangszelle, etwa ``B3``.
        rows: die Verschiebung nach unten.
        columns: die Verschiebung nach rechts.

    Returns:
        Die neue Adresse.

    Raises:
        ValueError: bei einer fehlerhaften Adresse oder wenn die
            Verschiebung aus dem Blatt hinausführt.
    """
    text = str(cell).strip().upper()
    letters = "".join(character for character in text
                      if character.isalpha())
    digits = "".join(character for character in text if character.isdigit())
    if not letters or not digits:
        raise ValueError("keine gültige Adresse")
    column = 0
    for character in letters:
        column = column * 26 + (ord(character) - ord("A") + 1)
    column += columns
    row = int(digits) + rows
    if column < 1 or row < 1:
        raise ValueError("die Verschiebung führt aus dem Blatt hinaus")
    name = ""
    while column:
        column, rest = divmod(column - 1, 26)
        name = chr(ord("A") + rest) + name
    return "%s%d" % (name, row)


def even_or_odd_target(number, anchor="B3"):
    """Aufgabe 12a: gerade Zahlen nach D7, ungerade nach D10.

    Die Auflage der Aufgabe ist, jede Zelle nur über B3 anzusprechen.
    Von B3 aus ist D7 die Verschiebung um vier Zeilen und zwei Spalten,
    D10 die um sieben Zeilen und zwei Spalten.

    Raises:
        ValueError: bei einer fehlerhaften Ankeradresse.
    """
    if number % 2 == 0:
        rows, columns = 4, 2
    else:
        rows, columns = 7, 2
    return {"target": offset(anchor, rows, columns),
            "offset": (rows, columns), "even": number % 2 == 0,
            "anchor": anchor}


def select_case(value, cases, otherwise=None):
    """Bildet ``Select Case`` nach.

    Der erste passende Fall gewinnt und die übrigen werden nicht mehr
    geprüft; das unterscheidet die Anweisung von einer Folge einzelner
    Bedingungen und macht die Reihenfolge der Fälle bedeutsam.

    Args:
        value: der zu prüfende Wert.
        cases: Paare aus Bedingung und Ergebnis, in der Reihenfolge.
        otherwise: das Ergebnis für ``Case Else``.

    Returns:
        Das Ergebnis des ersten passenden Falles.
    """
    for condition, result in cases:
        if condition(value):
            return result
    return otherwise


def if_then_else_shape():
    """Nennt die Form der Anweisung aus dem Tutorium.

    Der Else-Teil darf fehlen, ElseIf beliebig oft stehen, und ``End If``
    schliesst die mehrzeilige Form ab. Die einzeilige Form kommt ohne
    ``End If`` aus und ist genau deshalb eine Fehlerquelle: wer später
    eine zweite Anweisung hinzufügt, bekommt sie ausserhalb der Bedingung.
    """
    return {"shape": ["If <Ausdruck> Then", "<Anweisung>",
                      "ElseIf <Ausdruck> Then", "<Anweisung>", "Else",
                      "<Anweisung>", "End If"],
            "Else optional": True,
            "one line form": "If x > 0 Then y = 1",
            "trap": "eine zweite Anweisung in der einzeiligen Form steht "
                    "ausserhalb der Bedingung"}
