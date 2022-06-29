"""SQL-Grundanfragen gegen eine kleine Beispieldatenbank."""

import sqlite3

PRESIDENTS = [("Heuss", 1, "FDP"), ("Luebke", 2, "CDU"),
              ("Heinemann", 3, "SPD"), ("Scheel", 4, "FDP"),
              ("Carstens", 5, "CDU")]

ELECTIONS = [(1949, "Heuss"), (1954, "Heuss"), (1959, "Luebke"),
             (1964, "Luebke")]


def connect():
    """Legt die Beispieldatenbank im Arbeitsspeicher an.

    Returns:
        Eine offene Verbindung mit den Tabellen ``presidents`` und
        ``elections``.
    """
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE presidents "
                       "(name TEXT, term INTEGER, party TEXT)")
    connection.execute("CREATE TABLE elections "
                       "(year INTEGER, president TEXT)")
    connection.executemany("INSERT INTO presidents VALUES (?, ?, ?)",
                           PRESIDENTS)
    connection.executemany("INSERT INTO elections VALUES (?, ?)", ELECTIONS)
    return connection


def run(query, parameters=()):
    """Führt eine Anfrage auf einer frischen Beispieldatenbank aus.

    Args:
        query: SQL-Text.
        parameters: Werte für Platzhalter.

    Returns:
        Liste der Ergebnistupel.

    Raises:
        sqlite3.Error: wenn die Anfrage fehlerhaft ist.
    """
    connection = connect()
    try:
        return connection.execute(query, parameters).fetchall()
    finally:
        connection.close()


def agrees_with_engine():
    """Vergleicht eine Anfrage mit derselben Auswahl in Python.

    Returns:
        Wahr, wenn beide Wege dieselbe Menge von Namen liefern.
    """
    by_sql = {row[0] for row in
              run("SELECT name FROM presidents WHERE party = 'FDP'")}
    by_python = {name for name, _, party in PRESIDENTS if party == "FDP"}
    return by_sql == by_python


def clause_order():
    """Nennt die Auswertungsreihenfolge der Klauseln.

    Sie weicht von der Schreibreihenfolge ab: die Projektion kommt spät,
    weshalb ein Alias aus SELECT in WHERE noch nicht bekannt ist.
    """
    return ["FROM", "WHERE", "GROUP BY", "HAVING", "SELECT", "ORDER BY",
            "LIMIT"]
