"""Die Schemadefinition der Möbelhauskette."""

import sqlite3

TABLES = ("kunde", "artikel", "lager", "verkaeufer", "liegt_in",
          "kunde_wirbt_kunde", "kassenbon", "k_position", "betreut")

SCHEMA = """
CREATE TABLE kunde (
    knr INTEGER PRIMARY KEY, name TEXT NOT NULL, vorname TEXT NOT NULL,
    strasse TEXT, hnr INTEGER, plz TEXT, ort TEXT, geb_datum TEXT);
CREATE TABLE artikel (
    anr INTEGER PRIMARY KEY, abez TEXT NOT NULL, preis REAL NOT NULL,
    kap_beanspruchung INTEGER NOT NULL);
CREATE TABLE lager (
    lnr INTEGER PRIMARY KEY, ort TEXT NOT NULL, kapazitaet INTEGER NOT NULL);
CREATE TABLE verkaeufer (
    vnr INTEGER PRIMARY KEY, name TEXT NOT NULL, vorname TEXT NOT NULL);
CREATE TABLE liegt_in (
    lnr INTEGER, anr INTEGER, menge INTEGER NOT NULL,
    PRIMARY KEY (lnr, anr),
    FOREIGN KEY (lnr) REFERENCES lager (lnr),
    FOREIGN KEY (anr) REFERENCES artikel (anr));
CREATE TABLE kunde_wirbt_kunde (
    knr_neu INTEGER PRIMARY KEY, knr_alt INTEGER NOT NULL,
    FOREIGN KEY (knr_neu) REFERENCES kunde (knr),
    FOREIGN KEY (knr_alt) REFERENCES kunde (knr));
CREATE TABLE kassenbon (
    bon_nr INTEGER PRIMARY KEY, datum TEXT NOT NULL, knr INTEGER NOT NULL,
    FOREIGN KEY (knr) REFERENCES kunde (knr));
CREATE TABLE k_position (
    bon_nr INTEGER, anr INTEGER, menge INTEGER NOT NULL,
    PRIMARY KEY (bon_nr, anr),
    FOREIGN KEY (bon_nr) REFERENCES kassenbon (bon_nr),
    FOREIGN KEY (anr) REFERENCES artikel (anr));
CREATE TABLE betreut (
    bon_nr INTEGER, anr INTEGER, vnr INTEGER NOT NULL,
    PRIMARY KEY (bon_nr, anr),
    FOREIGN KEY (bon_nr) REFERENCES kassenbon (bon_nr),
    FOREIGN KEY (anr) REFERENCES artikel (anr),
    FOREIGN KEY (vnr) REFERENCES verkaeufer (vnr));
"""


def create(connection=None):
    """Legt das Schema an.

    Args:
        connection: eine offene Verbindung; ohne Angabe wird eine
            Datenbank im Arbeitsspeicher erzeugt.

    Returns:
        Die Verbindung.
    """
    if connection is None:
        connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SCHEMA)
    return connection


def tables(connection):
    """Nennt die vorhandenen Tabellen, alphabetisch."""
    rows = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' "
        "ORDER BY name").fetchall()
    return [row[0] for row in rows]


def columns(connection, table):
    """Nennt die Spalten einer Tabelle in ihrer Reihenfolge.

    Raises:
        ValueError: bei einer unbekannten Tabelle.
    """
    if table not in tables(connection):
        raise ValueError("unbekannte Tabelle")
    rows = connection.execute("PRAGMA table_info(%s)" % table).fetchall()
    return [row[1] for row in rows]


def add_column(connection, table, column, kind="TEXT"):
    """Fügt einer Tabelle eine Spalte hinzu.

    Aufgabe 1 des sechsten Tutoriums: der Kunde soll einen zweiten
    Vornamen bekommen, das Lager eine Anschrift.

    Raises:
        ValueError: bei einer unbekannten Tabelle.
    """
    if table not in tables(connection):
        raise ValueError("unbekannte Tabelle")
    connection.execute("ALTER TABLE %s ADD COLUMN %s %s"
                       % (table, column, kind))
    return columns(connection, table)


def drop_column(connection, table, column):
    """Entfernt eine Spalte wieder.

    Der dritte Teil der Aufgabe: der zweite Vorname wird kaum genutzt und
    fällt weg. In älteren Systemen ging das nicht, und der übliche Weg war
    eine neue Tabelle, ein Kopieren der Daten und ein Umbenennen; sqlite
    kann es seit 3.35 unmittelbar.

    Raises:
        ValueError: bei einer unbekannten Tabelle oder Spalte.
    """
    if table not in tables(connection):
        raise ValueError("unbekannte Tabelle")
    if column not in columns(connection, table):
        raise ValueError("unbekannte Spalte")
    connection.execute("ALTER TABLE %s DROP COLUMN %s" % (table, column))
    return columns(connection, table)


def creation_order():
    """Nennt die Reihenfolge, in der die Tabellen angelegt werden müssen.

    Die referentielle Integrität bestimmt sie: eine Tabelle mit einem
    Fremdschlüssel kann erst entstehen, wenn das Ziel des Schlüssels
    existiert. Zuerst die vier Tabellen ohne Fremdschlüssel, dann die
    fünf, die darauf verweisen.
    """
    return list(TABLES)


def drop_order():
    """Nennt die Reihenfolge beim Löschen: genau umgekehrt.

    Beim Löschen kehrt sich die Abhängigkeit um. Wer zuerst die Tabelle
    entfernt, auf die verwiesen wird, lässt Verweise ins Leere zeigen;
    eine Datenbank mit eingeschalteter Fremdschlüsselprüfung weist das
    zurück.
    """
    return list(reversed(TABLES))


def drop_all(connection):
    """Löscht alle Tabellen in der zulässigen Reihenfolge."""
    for table in drop_order():
        connection.execute("DROP TABLE IF EXISTS %s" % table)
    return tables(connection)
