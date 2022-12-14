"""Gruppierung mit Bedingung.

Aufgabe 4 des siebten und Aufgabe 1 des achten Tutoriums.
"""

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


def articles_per_customer(connection, first=1, last=10):
    """Teil 4a: wie viele Artikel die Kunden insgesamt gekauft haben."""
    return connection.execute(
        "SELECT b.knr, SUM(p.menge) AS Menge FROM kassenbon b "
        "JOIN k_position p ON p.bon_nr = b.bon_nr "
        "WHERE b.knr BETWEEN ? AND ? GROUP BY b.knr ORDER BY b.knr",
        (first, last)).fetchall()


def articles_per_seller(connection):
    """Teil 4b: wie viele unterschiedliche Artikel je Verkäufer.

    Das Wort «unterschiedliche» entscheidet: ohne DISTINCT zählt die
    Abfrage die Betreuungen, mit DISTINCT die Artikelarten. Derselbe
    Artikel auf zwei Bons ist zweimal betreut und trotzdem ein Artikel.
    """
    return connection.execute(
        "SELECT v.vnr, v.name, v.vorname, COUNT(DISTINCT b.anr) AS Anzahl "
        "FROM betreut b JOIN verkaeufer v ON v.vnr = b.vnr "
        "GROUP BY v.vnr, v.name, v.vorname ORDER BY v.vnr").fetchall()


def pieces_per_warehouse(connection):
    """Teil 4c: wie viele Möbelstücke in den einzelnen Lagern liegen."""
    return connection.execute(
        "SELECT l.ort, SUM(i.menge) AS Anzahl FROM liegt_in i "
        "JOIN lager l ON l.lnr = i.lnr GROUP BY l.lnr, l.ort "
        "ORDER BY l.ort").fetchall()


def warehouse_value(connection):
    """Teil 4d: der Lagerwert der einzelnen Lager."""
    return connection.execute(
        "SELECT i.lnr, SUM(i.menge * a.preis) AS wert FROM liegt_in i "
        "JOIN artikel a ON a.anr = i.anr GROUP BY i.lnr "
        "ORDER BY i.lnr").fetchall()


def smallest_capacity(connection):
    """Teil 1a des achten Tutoriums: die kleinste Lagerkapazität."""
    return connection.execute(
        "SELECT MIN(kapazitaet) AS minimalkapazitaet FROM lager"
    ).fetchone()[0]


def free_space(connection):
    """Teil 1b: der freie Raum je Lager.

    Der belegte Raum ist die Summe aus Menge mal Kapazitätsbeanspruchung.
    Ein Lager ohne Artikel taucht in ``liegt_in`` nicht auf und fiele bei
    einem inneren Verbund heraus, obwohl es das Lager mit dem meisten
    freien Raum wäre; deshalb der äussere Verbund und der Ersatzwert
    null.
    """
    return connection.execute(
        "SELECT l.lnr, l.ort, "
        "l.kapazitaet - COALESCE(SUM(i.menge * a.kap_beanspruchung), 0) "
        "AS freiraum FROM lager l "
        "LEFT JOIN liegt_in i ON i.lnr = l.lnr "
        "LEFT JOIN artikel a ON a.anr = i.anr "
        "GROUP BY l.lnr, l.ort, l.kapazitaet ORDER BY l.ort").fetchall()


def turnover(connection, year="2007"):
    """Teil 1c: der Umsatz je Kunde in einem Jahr."""
    return connection.execute(
        "SELECT k.knr, k.name, k.vorname, "
        "SUM(p.menge * a.preis) AS umsatz FROM kunde k "
        "JOIN kassenbon b ON b.knr = k.knr "
        "JOIN k_position p ON p.bon_nr = b.bon_nr "
        "JOIN artikel a ON a.anr = p.anr "
        "WHERE substr(b.datum, 1, 4) = ? "
        "GROUP BY k.knr, k.name, k.vorname ORDER BY k.knr",
        (year,)).fetchall()


def turnover_above(connection, floor=1000.0, year="2007"):
    """Teil 1d: nur die Kunden über einer Umsatzgrenze.

    Die Bedingung betrifft eine Summe und gehört deshalb in HAVING. In
    WHERE stünde sie vor der Gruppierung und hätte nichts, worauf sie
    sich beziehen könnte: die Summe gibt es zu diesem Zeitpunkt noch
    nicht.
    """
    return connection.execute(
        "SELECT k.knr, k.name, k.vorname, "
        "SUM(p.menge * a.preis) AS umsatz FROM kunde k "
        "JOIN kassenbon b ON b.knr = k.knr "
        "JOIN k_position p ON p.bon_nr = b.bon_nr "
        "JOIN artikel a ON a.anr = p.anr "
        "WHERE substr(b.datum, 1, 4) = ? "
        "GROUP BY k.knr, k.name, k.vorname HAVING SUM(p.menge * a.preis) > ? "
        "ORDER BY k.knr", (year, floor)).fetchall()


def recruiters(connection, least=2):
    """Teil 1e: welche Kunden mindestens so viele Neukunden geworben haben."""
    return connection.execute(
        "SELECT k.knr, k.name, k.vorname, COUNT(*) AS geworben "
        "FROM kunde_wirbt_kunde w JOIN kunde k ON k.knr = w.knr_alt "
        "GROUP BY k.knr, k.name, k.vorname HAVING COUNT(*) >= ? "
        "ORDER BY k.knr", (least,)).fetchall()


def where_against_having():
    """Trennt die beiden Bedingungen.

    WHERE wählt Zeilen aus, bevor gruppiert wird, und kann deshalb keine
    Aggregatfunktion enthalten. HAVING wählt Gruppen aus, nachdem
    gruppiert wurde, und kann nichts anderes sinnvoll enthalten. Wer eine
    Zeilenbedingung in HAVING schreibt, bekommt dasselbe Ergebnis und
    eine langsamere Abfrage, weil erst gruppiert und dann verworfen wird.
    """
    return {"WHERE": "vor der Gruppierung, über Zeilen",
            "HAVING": "nach der Gruppierung, über Gruppen",
            "row condition in HAVING": "gleiches Ergebnis, mehr Arbeit",
            "aggregate in WHERE": "Fehler, die Summe gibt es noch nicht"}
