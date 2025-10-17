"""Rotation: dieselben Zahlen, andere Achsen."""

AGGREGATES = ("sum", "mean", "min", "max", "count")


def _apply(values, how):
    """Verdichtet eine Liste von Werten.

    Raises:
        ValueError: bei einer unbekannten Verdichtung.
    """
    if how not in AGGREGATES:
        raise ValueError("unbekannte Verdichtung: %s" % how)
    if how == "count":
        return len(values)
    if not values:
        return None
    if how == "sum":
        return sum(values)
    if how == "mean":
        return sum(values) / len(values)
    if how == "min":
        return min(values)
    return max(values)


def pivot(built, rows, columns, measure, how="sum"):
    """Stellt eine Kennzahl als Kreuztabelle dar.

    Args:
        built: der Würfel.
        rows: die Dimension der Zeilen.
        columns: die Dimension der Spalten.
        measure: die Kennzahl.
        how: die Verdichtung.

    Returns:
        Verschachtelte Abbildung Zeile nach Spalte nach Wert; leere
        Kombinationen stehen als ``None`` darin, damit die Tabelle
        rechteckig bleibt.

    Raises:
        ValueError: bei unbekannter Dimension, Kennzahl oder Verdichtung.
    """
    for name in (rows, columns):
        if name not in built["dimensions"]:
            raise ValueError("unbekannte Dimension: %s" % name)
    if measure not in built["measures"]:
        raise ValueError("unbekannte Kennzahl: %s" % measure)
    if how not in AGGREGATES:
        raise ValueError("unbekannte Verdichtung: %s" % how)
    groups = {}
    for row in built["rows"]:
        groups.setdefault((row[rows], row[columns]), []).append(row[measure])
    table = {}
    for name in built["members"][rows]:
        table[name] = {}
        for other in built["members"][columns]:
            values = groups.get((name, other))
            table[name][other] = _apply(values, how) if values else None
    return table


def transpose(table):
    """Vertauscht Zeilen und Spalten einer Kreuztabelle.

    Das ist die Rotation im engeren Sinne: die Zahlen bleiben, nur die
    Blickrichtung ändert sich. Zweimal angewandt kommt die
    Ausgangstabelle zurück, und genau das macht sie zur Probe für die
    Operation.
    """
    turned = {}
    for name, line in table.items():
        for other, value in line.items():
            turned.setdefault(other, {})[name] = value
    return turned


def why_it_matters():
    """Sagt, wozu die Rotation gut ist.

    Der Inhalt einer Kreuztabelle ändert sich nicht, die Frage, die sie
    beantwortet, schon. Projekte in den Zeilen und Risikoarten in den
    Spalten liest der Projektleiter; umgekehrt liest es der
    Risikomanager, der wissen will, welche Risikoart über alle Projekte
    hinweg drückt.
    """
    return {"changes": "the reading direction",
            "does not change": "the numbers",
            "project view": "one row per project",
            "risk view": "one row per kind of risk"}
