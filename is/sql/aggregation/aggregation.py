"""Gruppierung, Aggregatfunktionen und ihr Verhalten bei Nullwerten."""

import os
import re
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "basic-queries"))

import basic_queries


def run(query, parameters=()):
    """Führt eine Anfrage auf der Beispieldatenbank aus."""
    return basic_queries.run(query, parameters)


def _table_with_nulls():
    """Legt eine Tabelle mit drei Werten und zwei Nullwerten an."""
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE measurement (value INTEGER)")
    connection.executemany("INSERT INTO measurement VALUES (?)",
                           [(10,), (20,), (30,), (None,), (None,)])
    return connection


def null_counting():
    """Vergleicht COUNT(*) mit COUNT(spalte) auf Daten mit Nullwerten.

    Returns:
        Abbildung mit beiden Zählungen; die zweite überspringt die
        Nullwerte.
    """
    connection = _table_with_nulls()
    try:
        star = connection.execute(
            "SELECT COUNT(*) FROM measurement").fetchone()[0]
        column = connection.execute(
            "SELECT COUNT(value) FROM measurement").fetchone()[0]
    finally:
        connection.close()
    return {"count star": star, "count column": column}


def null_average():
    """Zeigt, dass AVG die Nullwerte auslässt statt sie als Null zu zählen.

    Returns:
        Abbildung mit dem Mittelwert der Datenbank und dem Mittelwert,
        der Nullwerte als Zahl 0 behandelt.
    """
    connection = _table_with_nulls()
    try:
        ignoring = connection.execute(
            "SELECT AVG(value) FROM measurement").fetchone()[0]
        counting = connection.execute(
            "SELECT AVG(COALESCE(value, 0)) FROM measurement").fetchone()[0]
    finally:
        connection.close()
    return {"average ignoring nulls": ignoring,
            "average counting nulls as zero": counting}


def is_ambiguous(query):
    """Prüft, ob eine Spalte weder gruppiert noch aggregiert wird.

    Args:
        query: SQL-Text einer Anfrage mit einer SELECT-Liste.

    Returns:
        Wahr, wenn eine nackte Spalte neben einem Aggregat steht, ohne in
        GROUP BY vorzukommen.
    """
    match = re.search(r"SELECT (.+?) FROM", query, re.IGNORECASE | re.DOTALL)
    if match is None:
        return False
    items = [item.strip() for item in match.group(1).split(",")]
    grouped = []
    group_match = re.search(r"GROUP BY (.+?)(?:HAVING|ORDER|$)", query,
                            re.IGNORECASE | re.DOTALL)
    if group_match:
        grouped = [item.strip() for item in group_match.group(1).split(",")]
    aggregates = ("COUNT", "SUM", "AVG", "MIN", "MAX")
    has_aggregate = any(item.upper().startswith(aggregates) for item in items)
    if not has_aggregate:
        return False
    for item in items:
        if item.upper().startswith(aggregates):
            continue
        if item not in grouped:
            return True
    return False


def having_versus_where():
    """Beschreibt, worauf die beiden Filter wirken."""
    return {"where": "rows before grouping",
            "having": "groups after grouping"}
