"""Zelladressen, Bereiche und Bereichsnamen."""

import re

ADDRESS = re.compile(r"^(\$?)([A-Z]{1,3})(\$?)([1-9][0-9]*)$")


def parse(address):
    """Zerlegt eine Adresse in Spalte, Zeile und die beiden Dollarzeichen.

    Args:
        address: etwa ``A1``, ``$B$7`` oder ``C$12``.

    Returns:
        Abbildung mit ``column``, ``row``, ``column absolute`` und
        ``row absolute``.

    Raises:
        ValueError: bei einer Adresse, die nicht der Form entspricht.
    """
    match = ADDRESS.match(str(address).strip().upper())
    if not match:
        raise ValueError("keine gültige Adresse: %s" % address)
    column_mark, letters, row_mark, digits = match.groups()
    return {"column": column_number(letters), "row": int(digits),
            "column absolute": column_mark == "$",
            "row absolute": row_mark == "$"}


def column_number(letters):
    """Rechnet Spaltenbuchstaben in eine Nummer um; A ist eins.

    Raises:
        ValueError: bei etwas anderem als Buchstaben.
    """
    text = str(letters).strip().upper()
    if not text or not text.isalpha():
        raise ValueError("keine Spaltenbezeichnung")
    number = 0
    for character in text:
        number = number * 26 + (ord(character) - ord("A") + 1)
    return number


def column_letters(number):
    """Rechnet eine Spaltennummer zurück in Buchstaben.

    Die Umrechnung ist kein gewöhnliches Stellenwertsystem: es gibt keine
    Null, auf Z folgt AA und nicht BA. Deshalb wird vor jeder Division
    eins abgezogen.

    Raises:
        ValueError: bei einer Nummer unter eins.
    """
    if number < 1:
        raise ValueError("die Spaltennummer beginnt bei eins")
    letters = ""
    while number:
        number, rest = divmod(number - 1, 26)
        letters = chr(ord("A") + rest) + letters
    return letters


def address_of(column, row, column_absolute=False, row_absolute=False):
    """Baut eine Adresse aus Spalte und Zeile.

    Raises:
        ValueError: bei einer Spalte oder Zeile unter eins.
    """
    if row < 1:
        raise ValueError("die Zeile beginnt bei eins")
    return "%s%s%s%s" % ("$" if column_absolute else "",
                         column_letters(column),
                         "$" if row_absolute else "", row)


def expand(area):
    """Zählt die Adressen eines Bereichs auf, zeilenweise.

    Args:
        area: etwa ``D6:D13`` oder ``A1:C2``.

    Returns:
        Liste der Adressen.

    Raises:
        ValueError: bei einem Bereich, der nicht aus zwei Adressen
            besteht.
    """
    parts = str(area).split(":")
    if len(parts) != 2:
        raise ValueError("kein Bereich: %s" % area)
    first, second = (parse(part) for part in parts)
    columns = range(min(first["column"], second["column"]),
                    max(first["column"], second["column"]) + 1)
    rows = range(min(first["row"], second["row"]),
                 max(first["row"], second["row"]) + 1)
    return [address_of(column, row) for row in rows for column in columns]


def size(area):
    """Nennt Breite, Höhe und Zellenzahl eines Bereichs.

    Raises:
        ValueError: bei einem fehlerhaften Bereich.
    """
    cells = expand(area)
    first, second = (parse(part) for part in str(area).split(":"))
    width = abs(first["column"] - second["column"]) + 1
    height = abs(first["row"] - second["row"]) + 1
    return {"width": width, "height": height, "cells": len(cells)}


def named_ranges():
    """Nennt die Namen aus Aufgabe 2 des achten Tutoriums.

    Ein Name ist eine Form des absoluten Bezugs und gilt in der ganzen
    Arbeitsmappe. Das ist sein Vorteil und seine Falle: er verschiebt
    sich beim Kopieren nicht, und er verrät auch nicht, worauf er zeigt,
    wenn jemand den Bereich später ändert.
    """
    return {"Umsatzsteuersatz": "D22",
            "Nettopreise Lebensmittel": "C6:C13",
            "Nettopreise Non-Food": "C17:C18",
            "Bruttopreise Lebensmittel": "D6:D13",
            "Bruttopreise Non-Food": "D17:D18"}


def why_a_name_is_absolute():
    """Erklärt, warum ein Name sich beim Kopieren nicht verschiebt.

    Ein Name zeigt auf einen festen Bereich, nicht auf eine Stelle
    relativ zur Formel. Deshalb ersetzt er den absoluten Bezug und macht
    die Formel zugleich lesbar: ``=C6*(1+Umsatzsteuersatz)`` sagt, was
    gerechnet wird, ``=C6*(1+$D$22)`` sagt, wo es steht.
    """
    return {"behaves like": "ein absoluter Bezug",
            "scope": "die ganze Arbeitsmappe",
            "advantage": "die Formel wird lesbar",
            "risk": "der Name verrät nicht, wenn sein Bereich sich ändert"}
