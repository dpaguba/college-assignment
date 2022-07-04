"""Unteranfragen, ihre Korrelation und die Falle NOT IN mit Nullwerten."""

import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "basic-queries"))

import basic_queries


def run(query, parameters=()):
    """Führt eine Anfrage auf der Beispieldatenbank aus."""
    return basic_queries.run(query, parameters)


def not_in_with_null():
    """Vergleicht NOT IN und NOT EXISTS über einer Liste mit Nullwert.

    Enthält die Unteranfrage einen Nullwert, ist ``x NOT IN (…)`` nie
    wahr, weil der Vergleich unbekannt bleibt. NOT EXISTS prüft dagegen
    nur, ob eine Zeile gefunden wird.

    Returns:
        Abbildung mit der Zeilenzahl beider Formulierungen.
    """
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("CREATE TABLE left_side (value INTEGER)")
        connection.execute("CREATE TABLE right_side (value INTEGER)")
        connection.executemany("INSERT INTO left_side VALUES (?)",
                               [(1,), (2,), (3,)])
        connection.executemany("INSERT INTO right_side VALUES (?)",
                               [(2,), (None,)])
        not_in = connection.execute(
            "SELECT value FROM left_side WHERE value NOT IN "
            "(SELECT value FROM right_side)").fetchall()
        not_exists = connection.execute(
            "SELECT l.value FROM left_side l WHERE NOT EXISTS "
            "(SELECT 1 FROM right_side r WHERE r.value = l.value)").fetchall()
    finally:
        connection.close()
    return {"not in": len(not_in), "not exists": len(not_exists)}


def rewrite_as_join():
    """Zeigt eine unkorrelierte Unteranfrage und ihren Verbund.

    Returns:
        Abbildung mit der Zeilenzahl beider Formulierungen; sie stimmen
        überein, weil jeder Präsident höchstens einmal in der
        Unteranfrage steht.
    """
    by_subquery = run("SELECT name FROM presidents WHERE name IN "
                      "(SELECT DISTINCT president FROM elections)")
    by_join = run("SELECT DISTINCT p.name FROM presidents p "
                  "JOIN elections e ON e.president = p.name")
    return {"subquery": len(by_subquery), "join": len(by_join)}


def correlated(query):
    """Sagt, ob eine Unteranfrage auf die äußere Anfrage verweist.

    Erkannt wird der Verweis daran, dass innerhalb der Klammer ein Alias
    der äußeren Anfrage vorkommt.
    """
    start = query.find("(")
    if start < 0:
        return False
    inner = query[start:]
    outer = query[:start]
    aliases = [word for word in outer.replace(",", " ").split()
               if len(word) <= 2 and word.isalpha()]
    return any((alias + ".") in inner for alias in aliases)


def placement():
    """Nennt die Stellen, an denen eine Unteranfrage stehen darf."""
    return ["SELECT", "FROM", "WHERE", "HAVING"]
