"""Dreiwertige Logik von SQL: wahr, falsch und unbekannt."""

import sqlite3


def compare(left, right):
    """Vergleicht zwei Werte nach SQL-Regeln.

    Returns:
        None, sobald ein Nullwert beteiligt ist, sonst das Ergebnis des
        Gleichheitstests.
    """
    if left is None or right is None:
        return None
    return left == right


def and_(left, right):
    """Konjunktion der dreiwertigen Logik.

    Falsch dominiert: ``False and None`` ist falsch, weil das Ergebnis
    unabhängig vom unbekannten Wert feststeht.
    """
    if left is False or right is False:
        return False
    if left is None or right is None:
        return None
    return True


def or_(left, right):
    """Disjunktion der dreiwertigen Logik; wahr dominiert."""
    if left is True or right is True:
        return True
    if left is None or right is None:
        return None
    return False


def not_(value):
    """Negation; die Negation von unbekannt bleibt unbekannt."""
    if value is None:
        return None
    return not value


def passes_where(value):
    """Sagt, ob eine Zeile die WHERE-Klausel übersteht.

    Nur der Wahrheitswert wahr genügt: unbekannt filtert die Zeile
    genauso weg wie falsch.
    """
    return value is True


def excluded_middle_fails():
    """Zeigt eine Zeile, die weder Bedingung noch Gegenbedingung erfüllt.

    Returns:
        Abbildung mit der Gesamtzahl und den Treffern beider Anfragen.
    """
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("CREATE TABLE t (value INTEGER)")
        connection.execute("INSERT INTO t VALUES (NULL)")
        matching = connection.execute(
            "SELECT * FROM t WHERE value = 1").fetchall()
        not_matching = connection.execute(
            "SELECT * FROM t WHERE value <> 1").fetchall()
        total = connection.execute("SELECT COUNT(*) FROM t").fetchone()[0]
    finally:
        connection.close()
    return {"matching": len(matching), "not matching": len(not_matching),
            "total": total}


def engine_agrees():
    """Vergleicht die Wahrheitstafeln dieses Moduls mit denen der Datenbank.

    Returns:
        Wahr, wenn AND und OR für alle neun Kombinationen übereinstimmen.
    """
    values = [True, False, None]
    connection = sqlite3.connect(":memory:")
    try:
        for left in values:
            for right in values:
                for name, function in (("AND", and_), ("OR", or_)):
                    query = "SELECT ? %s ?" % name
                    engine = connection.execute(
                        query, (_to_sql(left), _to_sql(right))).fetchone()[0]
                    if _from_sql(engine) is not function(left, right):
                        return False
    finally:
        connection.close()
    return True


def _to_sql(value):
    """Bildet einen dreiwertigen Wahrheitswert auf SQL ab."""
    if value is None:
        return None
    return 1 if value else 0


def _from_sql(value):
    """Bildet ein Ergebnis der Datenbank auf einen Wahrheitswert ab."""
    if value is None:
        return None
    return bool(value)


def is_null_is_the_only_test():
    """Nennt den Operator, mit dem sich ein Nullwert prüfen lässt."""
    return "IS NULL"
