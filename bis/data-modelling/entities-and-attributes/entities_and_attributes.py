"""Entitätstypen, Attribute und die Suche nach Schlüsselkandidaten."""

import itertools


def entity_type(name, attributes):
    """Beschreibt einen Entitätstyp.

    Ein Entitätstyp fasst alle gleichartigen Entitäten zusammen: der Typ
    ``Kunde`` alle Kunden, der Typ ``Vorlesung`` alle Lehrveranstaltungen.
    Im Diagramm steht er in einem Rechteck, seine Attribute in Ellipsen.

    Args:
        name: der Name des Typs.
        attributes: seine Attribute.

    Returns:
        Abbildung mit Namen, Attributen und der Darstellung.

    Raises:
        ValueError: ohne Namen oder ohne Attribute.
    """
    if not name:
        raise ValueError("ein Entitätstyp braucht einen Namen")
    if not attributes:
        raise ValueError("ein Entitätstyp ohne Attribut speichert nichts")
    return {"name": name, "attributes": list(attributes),
            "shape": "Rechteck", "attribute shape": "Ellipse"}


def key_candidates(rows):
    """Nennt die einzelnen Attribute, die eine Zeile eindeutig bestimmen.

    Ein Schlüsselkandidat ist jedes Attribut, dessen Werte über die ganze
    Tabelle verschieden sind. Der Name taugt fast nie: zwei Studierende
    dürfen Thomas Wagner heissen, zwei Matrikelnummern dürfen nicht gleich
    sein.

    Args:
        rows: die Zeilen als Abbildungen.

    Returns:
        Die tauglichen Attribute, alphabetisch.

    Raises:
        ValueError: bei einer leeren Tabelle.
    """
    if not rows:
        raise ValueError("leere Tabelle")
    columns = sorted(rows[0])
    return [name for name in columns
            if len({row[name] for row in rows}) == len(rows)]


def composite_keys(rows, limit=3):
    """Sucht die kleinsten Attributkombinationen, die eindeutig sind.

    Gesucht werden nur minimale Kombinationen: eine Menge, die eine
    kleinere eindeutige Menge enthält, ist kein Kandidat, sondern nur ein
    Kandidat mit Ballast.

    Args:
        rows: die Zeilen.
        limit: die höchste betrachtete Grösse einer Kombination.

    Returns:
        Liste der Kombinationen als Tupel, alphabetisch.

    Raises:
        ValueError: bei einer leeren Tabelle.
    """
    if not rows:
        raise ValueError("leere Tabelle")
    columns = sorted(rows[0])
    found = []
    for size in range(1, min(limit, len(columns)) + 1):
        for combination in itertools.combinations(columns, size):
            if any(set(other) <= set(combination) for other in found):
                continue
            keys = {tuple(row[name] for name in combination) for row in rows}
            if len(keys) == len(rows):
                found.append(combination)
    return found


def choose_key(candidates, chosen):
    """Wählt aus den Kandidaten das Schlüsselattribut.

    Der Kandidat ist eine Eigenschaft der Daten, die Wahl eine
    Entscheidung des Modellierers. Im Diagramm wird das gewählte Attribut
    unterstrichen.

    Raises:
        ValueError: wenn die Wahl kein Kandidat ist.
    """
    if chosen not in candidates:
        raise ValueError("die Wahl steht nicht unter den Kandidaten")
    return {"candidates": list(candidates), "key": chosen,
            "underlined in the diagram": True,
            "usually": "eine eindeutige Nummer, keine sprechende Angabe"}


def think_in_tables():
    """Nennt den Rat, den das Merkblatt an den Anfang stellt.

    Wer sich unsicher ist, ob ein Attribut ein Schlüssel sein kann, soll
    sich den Entitätstyp als Tabelle vorstellen und drei Zeilen
    hinschreiben. Bei Thomas Wagner, Thomas Wagner und Sabrina Müller ist
    sofort zu sehen, dass der Name nicht trägt.
    """
    return {"advice": "picture the entity type as a table",
            "then ask": "may two rows share this value",
            "example": "two students may share a name, not a number"}
