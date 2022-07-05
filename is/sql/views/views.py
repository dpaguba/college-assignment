"""Sichten: gespeicherte Anfragen, ihre Aktualität und Änderbarkeit."""

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "basic-queries"))

import basic_queries


def run_with_view(definition, query):
    """Legt eine Sicht an und fragt sie ab.

    Args:
        definition: CREATE-VIEW-Anweisung.
        query: Anfrage, die die Sicht benutzt.

    Returns:
        Liste der Ergebnistupel.
    """
    connection = basic_queries.connect()
    try:
        connection.execute(definition)
        return connection.execute(query).fetchall()
    finally:
        connection.close()


def reflects_changes():
    """Misst die Größe einer Sicht vor und nach einer Einfügung.

    Returns:
        Abbildung mit beiden Zählungen; die Sicht speichert kein
        Ergebnis, sondern die Anfrage.
    """
    connection = basic_queries.connect()
    try:
        connection.execute("CREATE VIEW recent AS SELECT * FROM presidents "
                           "WHERE term > 2")
        before = connection.execute(
            "SELECT COUNT(*) FROM recent").fetchone()[0]
        connection.execute("INSERT INTO presidents VALUES ('Koehler', 9, "
                           "'CDU')")
        after = connection.execute(
            "SELECT COUNT(*) FROM recent").fetchone()[0]
    finally:
        connection.close()
    return {"before": before, "after": after}


def is_updatable(query):
    """Schätzt, ob Änderungen an einer Sicht eindeutig zurückführbar sind.

    Nicht änderbar ist eine Sicht mit Gruppierung, Aggregat, DISTINCT,
    Vereinigung oder mehreren Tabellen, weil eine geänderte Zeile keiner
    eindeutigen Basiszeile entspricht.
    """
    text = query.upper()
    for blocker in ("GROUP BY", "DISTINCT", "UNION", "HAVING", "JOIN"):
        if blocker in text:
            return False
    if re.search(r"\b(COUNT|SUM|AVG|MIN|MAX)\s*\(", text):
        return False
    match = re.search(r"FROM (.+?)(?:WHERE|ORDER|$)", text, re.DOTALL)
    if match and "," in match.group(1):
        return False
    return True


def materialised_trade_off():
    """Stellt die materialisierte Sicht der gespeicherten Anfrage gegenüber."""
    return {"faster": True, "can be stale": True,
            "needs refresh": True, "costs storage": True}


def purposes():
    """Nennt die Gründe, aus denen Sichten angelegt werden."""
    return ["simplification", "access control", "logical independence"]
