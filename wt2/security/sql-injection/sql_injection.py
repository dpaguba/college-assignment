"""SQL-Injektion, gezeigt an einer echten Datenbank."""

import sqlite3


def _database():
    """Legt eine Benutzertabelle mit zwei Zeilen an."""
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE users (name TEXT, password TEXT)")
    connection.executemany("INSERT INTO users VALUES (?, ?)",
                           [("ada", "secret"), ("bob", "hunter2")])
    return connection


def login_by_concatenation(name, password):
    """Baut die Anfrage durch Zusammenkleben von Zeichenketten.

    Returns:
        Abbildung mit dem Ergebnis, der Zeilenzahl, der gestellten Anfrage
        und einem Vermerk, falls die Schnittstelle sie abgewiesen hat.
    """
    query = ("SELECT * FROM users WHERE name = '%s' AND password = '%s'"
             % (name, password))
    connection = _database()
    refused = None
    try:
        rows = connection.execute(query).fetchall()
    except (sqlite3.Error, sqlite3.Warning) as error:
        rows = []
        refused = str(error)
    finally:
        connection.close()
    return {"logged in": bool(rows), "rows": len(rows), "query": query,
            "refused by the interface": refused}


def login_by_parameters(name, password):
    """Stellt dieselbe Anfrage mit Platzhaltern.

    Der Wert erreicht die Datenbank getrennt vom Text der Anfrage und kann
    daher nicht Teil davon werden, gleich was darin steht.
    """
    connection = _database()
    try:
        rows = connection.execute(
            "SELECT * FROM users WHERE name = ? AND password = ?",
            (name, password)).fetchall()
    finally:
        connection.close()
    return {"logged in": bool(rows), "rows": len(rows),
            "query": "SELECT * FROM users WHERE name = ? AND password = ?"}


def where_the_payload_has_to_go():
    """Zeigt, dass dasselbe Muster nur an der richtigen Stelle wirkt.

    Im Namensfeld ergibt ``' OR '1'='1`` die Bedingung
    ``name = '' OR '1'='1' AND password = 'x'``. Die Konjunktion bindet
    stärker als die Disjunktion, also bleibt die Prüfung des Passworts
    stehen und die Anfrage findet nichts. Im Passwortfeld steht dieselbe
    Zeichenkette am Ende, die Disjunktion umfasst die ganze Bedingung, und
    jede Zeile passt.

    Returns:
        Abbildung mit dem Ergebnis für beide Felder und für den
        abgeschnittenen Rest.
    """
    payload = "' OR '1'='1"
    in_name = login_by_concatenation(payload, "x")
    in_password = login_by_concatenation("ada", payload)
    commented = login_by_concatenation("ada' --", "wrong")
    return {"in the name field": in_name["logged in"],
            "in the password field": in_password["logged in"],
            "rows in the password field": in_password["rows"],
            "comment cuts the check": commented["logged in"],
            "reason": "AND binds tighter than OR"}


def second_statement_attempt():
    """Versucht, eine zweite Anweisung anzuhängen.

    sqlite3 führt über ``execute`` nur eine Anweisung aus, deshalb
    scheitert das Anhängen an der Schnittstelle. Der Angriff über die
    Bedingung gelingt trotzdem, und in einer Datenbank, die mehrere
    Anweisungen zulässt, gelingt auch dieser.

    Returns:
        Abbildung mit beiden Ergebnissen.
    """
    payload = "ada'; DROP TABLE users; --"
    concatenated = login_by_concatenation(payload, "x")
    parameterised = login_by_parameters("ada", "' OR '1'='1")
    condition = login_by_concatenation("ada", "' OR '1'='1")
    return {"concatenation is vulnerable": condition["logged in"],
            "parameters are vulnerable": parameterised["logged in"],
            "second statement refused":
                concatenated["refused by the interface"] is not None}


def hand_escaping_fails():
    """Zeigt, dass eigenes Ersetzen der Anführungszeichen zu wenig ist.

    Verdoppelt jemand die Anführungszeichen von Hand, so bleibt der Fall
    des Zahlenfeldes offen: dort steht der Wert ohne Anführungszeichen in
    der Anfrage, und die Ersetzung greift gar nicht.

    Returns:
        Abbildung mit dem Ergebnis des Versuchs.
    """
    connection = _database()
    try:
        connection.execute("CREATE TABLE items (id INTEGER, owner TEXT)")
        connection.executemany("INSERT INTO items VALUES (?, ?)",
                               [(1, "ada"), (2, "bob")])
        payload = "1 OR 1=1"
        escaped = payload.replace("'", "''")
        rows = connection.execute(
            "SELECT * FROM items WHERE id = %s" % escaped).fetchall()
    finally:
        connection.close()
    return {"a case slips through": len(rows) > 1, "rows": len(rows),
            "reason": "a numeric field carries no quotes to escape"}


def defences():
    """Nennt die Massnahmen in der Reihenfolge ihrer Wirkung."""
    return ["parameterised statements, always",
            "an object mapper that produces them",
            "least privilege for the database account",
            "validation of the input, as a second net",
            "never build a query by concatenation, not even once"]
