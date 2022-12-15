"""Abfragen über mehrere Tabellen: Aufgabe 2 des siebten Tutoriums."""

import sqlite3

KUNDE = (
    (1, "Bachmann", "Otto", "Glueckauf Weg", 25, "44149", "Dortmund",
     "1949-08-12"),
    (2, "Kaufrausch", "Fridolin", "Goethe Strasse", 212, "44269",
     "Dortmund", "1945-01-17"),
    (3, "Geizig", "Ralf", "Doeblin Strasse", 23, "44793", "Bochum",
     "1955-02-16"),
    (4, "Mueller", "Klaus", "Alter Weg", 100, "58453", "Witten",
     "1975-03-15"),
    (5, "Maier", "Peter", "Dortmunder Allee", 4, "44689", "Bochum",
     "1950-04-14"),
    (6, "Bachmann", "Otto", "Hansastrasse", 7, "44137", "Dortmund",
     "1962-11-03"),
    (7, "Schmitz", "Anna", "Ruhrallee", 88, "44139", "Dortmund",
     "1980-06-22"),
    (8, "Lang", "Petra", "Herner Strasse", 15, "44787", "Bochum",
     "1971-09-09"),
    (9, "Vogel", "Hans", "Wittener Strasse", 40, "58452", "Witten",
     "1968-01-30"),
    (10, "Kurz", "Maria", "Am Markt", 2, "45127", "Essen", "1990-05-05"),
    (11, "Pfeiffer", "Gustav", "Kirchweg", 8, "44225", "Dortmund",
     "1957-12-19"),
)

ARTIKEL = (
    (1, "2er Sofa Leder", 499.90, 5),
    (2, "Sessel Leder", 399.90, 3),
    (3, "Schlafsofa", 549.98, 6),
    (4, "Couchtisch klein", 129.49, 3),
    (5, "Couchtisch Glas", 329.98, 4),
    (6, "Schrankwand Eiche rustikal", 899.00, 8),
)

LAGER = ((1, "Dortmund", 150), (2, "Bochum", 75), (3, "Witten", 250),
         (4, "Dortmund Wambel", 100), (5, "Essen", 300))

VERKAEUFER = ((1, "Berns", "Bernhardt"), (2, "Faulinski", "Paul"),
              (3, "Freundlich", "Johannes"))

LIEGT_IN = ((1, 1, 10), (1, 2, 12), (2, 3, 4), (2, 4, 6), (2, 5, 7),
            (3, 1, 10), (3, 6, 8), (4, 2, 5), (4, 4, 6), (5, 2, 9),
            (5, 3, 10), (5, 5, 11))

KUNDE_WIRBT_KUNDE = ((2, 1), (3, 1), (5, 2), (6, 1), (7, 2), (8, 1),
                     (9, 3))

KASSENBON = (
    (1, "2006-09-01 14:30:00", 1), (2, "2006-09-01 12:10:15", 5),
    (3, "2006-09-02 11:11:45", 3), (4, "2006-09-02 13:12:11", 1),
    (5, "2006-09-02 12:17:18", 4), (6, "2006-10-05 10:00:00", 2),
    (7, "2006-10-05 16:20:00", 7), (8, "2006-11-11 09:45:00", 10),
    (9, "2006-12-01 18:05:00", 10), (10, "2006-12-20 11:30:00", 8),
    (11, "2007-01-15 10:10:00", 1), (12, "2007-01-15 15:40:00", 2),
    (13, "2007-02-03 12:00:00", 3), (14, "2007-02-14 17:25:00", 10),
    (15, "2007-03-08 09:15:00", 4), (16, "2007-03-30 13:50:00", 5),
    (17, "2007-04-12 11:05:00", 6), (18, "2007-05-02 16:00:00", 7),
    (19, "2007-06-19 10:35:00", 8), (20, "2007-07-07 14:45:00", 9),
    (21, "2007-08-21 12:30:00", 10), (22, "2007-09-09 15:15:00", 11),
    (23, "2007-10-10 10:20:00", 1), (24, "2007-11-23 18:40:00", 2),
    (25, "2007-12-05 09:55:00", 10),
)

K_POSITION = (
    (1, 1, 1), (1, 2, 1), (2, 5, 1), (2, 4, 4), (3, 3, 4), (4, 1, 1),
    (5, 2, 2), (6, 4, 3), (6, 6, 1), (7, 3, 1), (8, 1, 2), (8, 5, 1),
    (9, 2, 1), (10, 6, 1), (11, 1, 1), (11, 4, 2), (12, 3, 1),
    (13, 2, 3), (14, 5, 2), (14, 6, 1), (15, 4, 1), (16, 1, 1),
    (17, 3, 2), (18, 2, 1), (18, 5, 1), (19, 6, 2), (20, 4, 4),
    (21, 1, 3), (22, 3, 1), (23, 2, 1), (23, 5, 2), (23, 6, 1),
    (24, 4, 2), (25, 1, 1), (25, 3, 1),
)

BETREUT = tuple((bon, anr, ((bon + anr) % 3) + 1)
                for bon, anr, _ in K_POSITION)

TABLES = {"kunde": KUNDE, "artikel": ARTIKEL, "lager": LAGER,
          "verkaeufer": VERKAEUFER, "liegt_in": LIEGT_IN,
          "kunde_wirbt_kunde": KUNDE_WIRBT_KUNDE, "kassenbon": KASSENBON,
          "k_position": K_POSITION, "betreut": BETREUT}

SCHEMA = """
CREATE TABLE kunde (knr INTEGER PRIMARY KEY, name TEXT, vorname TEXT,
    strasse TEXT, hnr INTEGER, plz TEXT, ort TEXT, geb_datum TEXT);
CREATE TABLE artikel (anr INTEGER PRIMARY KEY, abez TEXT, preis REAL,
    kap_beanspruchung INTEGER);
CREATE TABLE lager (lnr INTEGER PRIMARY KEY, ort TEXT,
    kapazitaet INTEGER);
CREATE TABLE verkaeufer (vnr INTEGER PRIMARY KEY, name TEXT,
    vorname TEXT);
CREATE TABLE liegt_in (lnr INTEGER, anr INTEGER, menge INTEGER,
    PRIMARY KEY (lnr, anr));
CREATE TABLE kunde_wirbt_kunde (knr_neu INTEGER PRIMARY KEY,
    knr_alt INTEGER);
CREATE TABLE kassenbon (bon_nr INTEGER PRIMARY KEY, datum TEXT,
    knr INTEGER);
CREATE TABLE k_position (bon_nr INTEGER, anr INTEGER, menge INTEGER,
    PRIMARY KEY (bon_nr, anr));
CREATE TABLE betreut (bon_nr INTEGER, anr INTEGER, vnr INTEGER,
    PRIMARY KEY (bon_nr, anr));
"""


def database():
    """Baut die Datenbank der Möbelhauskette im Arbeitsspeicher.

    Das Schema stammt aus dem fünften Tutorium, die Struktur der Daten aus
    dem sechsten. Die vollständige Ausprägung lag auf der Lernplattform
    und ist nicht in den Unterlagen; sie ist hier so ergänzt, dass jede
    Aufgabe der Tutorien sieben und acht eine Antwort hat.

    Returns:
        Eine offene Verbindung.
    """
    connection = sqlite3.connect(":memory:")
    connection.executescript(SCHEMA)
    for table, rows in TABLES.items():
        marks = ", ".join("?" * len(rows[0]))
        connection.executemany("INSERT INTO %s VALUES (%s)"
                               % (table, marks), rows)
    connection.commit()
    return connection


def articles_of_receipt(connection, bon_nr):
    """Teil a: welche Artikel wurden auf einem Kassenbon gekauft.

    Der Verbund läuft über ``k_position``: die Tabelle steht zwischen Bon
    und Artikel, weil ein Bon viele Artikel und ein Artikel viele Bons
    hat. Ohne die Zwischentabelle liesse sich die Beziehung nicht
    ablegen.
    """
    return connection.execute(
        "SELECT a.anr, a.abez, p.menge FROM k_position p "
        "JOIN artikel a ON a.anr = p.anr WHERE p.bon_nr = ? "
        "ORDER BY a.anr", (bon_nr,)).fetchall()


def articles_per_warehouse(connection):
    """Teil b: je Lager der Ort und die dort gelagerten Artikel."""
    return connection.execute(
        "SELECT l.ort, a.abez, i.menge FROM liegt_in i "
        "JOIN lager l ON l.lnr = i.lnr JOIN artikel a ON a.anr = i.anr "
        "ORDER BY l.ort, a.abez").fetchall()


def sellers_of_articles(connection, numbers):
    """Teil c: welche Verkäufer haben bestimmte Artikel betreut.

    Args:
        connection: die Datenbank.
        numbers: die Artikelnummern.

    Returns:
        Liste aus Artikelnummer, Name und Vorname, nach Artikel sortiert.

    Raises:
        ValueError: bei einer leeren Liste von Artikelnummern.
    """
    if not numbers:
        raise ValueError("keine Artikelnummern")
    marks = ", ".join("?" * len(numbers))
    return connection.execute(
        "SELECT DISTINCT b.anr, v.name, v.vorname FROM betreut b "
        "JOIN verkaeufer v ON v.vnr = b.vnr "
        "WHERE b.anr IN ({}) ORDER BY b.anr, v.name".format(marks),
        tuple(numbers)).fetchall()


def receipts_with_customer(connection):
    """Verbindet Bons mit ihren Kunden."""
    return connection.execute(
        "SELECT b.bon_nr, b.datum, k.name, k.vorname FROM kassenbon b "
        "JOIN kunde k ON k.knr = b.knr ORDER BY b.bon_nr").fetchall()


def articles_never_sold(connection):
    """Nennt die Artikel, die auf keinem Bon stehen.

    Das ist die Frage, die ein innerer Verbund nicht beantworten kann: er
    liefert nur Zeilen, zu denen es einen Partner gibt. Gesucht sind aber
    gerade die ohne Partner, und dafür braucht es den äusseren Verbund
    oder ein NOT IN.
    """
    return connection.execute(
        "SELECT a.anr, a.abez FROM artikel a "
        "LEFT JOIN k_position p ON p.anr = a.anr "
        "WHERE p.anr IS NULL ORDER BY a.anr").fetchall()


def the_missing_join_condition(connection):
    """Zeigt, was ein vergessener Verbund anrichtet.

    Ohne Bedingung verbindet der Verbund jede Zeile mit jeder: aus elf
    Kunden und fünf Lagern werden fünfundfünfzig Zeilen. Das Ergebnis
    sieht nach Daten aus und ist keines, und bei grossen Tabellen fällt
    es zuerst als Laufzeit auf und erst danach als Fehler.

    Returns:
        Abbildung mit beiden Zeilenzahlen.
    """
    cross = connection.execute(
        "SELECT COUNT(*) FROM kunde, lager").fetchone()[0]
    customers = connection.execute(
        "SELECT COUNT(*) FROM kunde").fetchone()[0]
    places = connection.execute("SELECT COUNT(*) FROM lager").fetchone()[0]
    return {"cross product": cross, "customers": customers,
            "warehouses": places, "product": customers * places}
