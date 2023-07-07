"""Abbildung eines Dokuments auf Tabellen und was dabei verloren geht."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "xml-model"))

import xml_model


def shred(root, element_name):
    """Zerlegt gleichnamige Elemente in eine Tabelle.

    Jedes Kindelement wird zu einer Spalte; fehlt es in einem Element,
    steht dort ein Nullwert.

    Args:
        root: Wurzel des Dokuments.
        element_name: Name der Elemente, die zu Zeilen werden.

    Returns:
        Abbildung mit den Schlüsseln ``columns`` und ``rows``.
    """
    records = [node for node in root.iter(element_name)]
    columns = []
    for record in records:
        for child in record:
            if child.tag not in columns:
                columns.append(child.tag)
    rows = []
    for record in records:
        found = {child.tag: child.text for child in record}
        rows.append(tuple(found.get(column) for column in columns))
    return {"columns": columns, "rows": rows}


def loses_order():
    """Sagt, ob die Zerlegung die Dokumentreihenfolge erhält.

    Eine Tabelle ist eine Menge von Zeilen; die Reihenfolge der
    Geschwister muss in einer eigenen Spalte festgehalten werden, sonst
    geht sie verloren.
    """
    return True


def tables_needed(depth):
    """Schätzt die Zahl der Tabellen für ein Dokument gegebener Tiefe.

    Jede Schachtelungsebene mit mehrwertigen Kindern braucht eine eigene
    Tabelle mit Fremdschlüssel auf die darüberliegende.

    Raises:
        ValueError: bei einer Tiefe kleiner als eins.
    """
    if depth < 1:
        raise ValueError("Tiefe ist kleiner als eins")
    return depth - 1 if depth > 1 else 1


def approaches():
    """Nennt die Wege, ein Dokument in einer Datenbank zu halten."""
    return {"shredding": "one table per element type",
            "clob": "the document as a single value",
            "native": "a store built for trees"}
