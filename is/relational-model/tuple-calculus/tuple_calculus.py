"""Tupelkalkül: Anfragen als Bedingung über einer Tupelvariablen."""


def evaluate(database, condition, source):
    """Wertet ``{t | t ∈ source ∧ condition(t)}`` aus.

    Args:
        database: Abbildung von Relationennamen auf Tupellisten.
        condition: Prädikat über einem Tupel.
        source: Name der Relation, über die die Variable läuft.

    Returns:
        Liste der Tupel, die die Bedingung erfüllen.

    Raises:
        KeyError: wenn die Relation in der Datenbasis fehlt.
    """
    return [tuple(row) for row in database[source] if condition(row)]


def is_safe(expression):
    """Schätzt, ob eine Anfrage sicher ist, also endlich viele Tupel liefert.

    Eine Anfrage ist unsicher, wenn ihre einzige Bedingung eine Negation
    ist: das Ergebnis wäre dann von der Wahl des Universums abhängig.
    """
    text = expression.strip()
    if text.startswith("not "):
        return False
    return "(" in text


def quantifier_meaning(quantifier):
    """Ordnet einem Quantor den entsprechenden Algebraoperator zu.

    Raises:
        ValueError: bei einem unbekannten Quantor.
    """
    table = {"exists": "join", "for all": "division"}
    if quantifier not in table:
        raise ValueError("unbekannter Quantor")
    return table[quantifier]


def domain_calculus_difference():
    """Beschreibt den Unterschied zum Bereichskalkül.

    Returns:
        Abbildung mit den Variablenarten beider Kalküle.
    """
    return {"tuple calculus": "variables range over tuples",
            "domain calculus": "variables range over attribute values",
            "same expressive power": True}
