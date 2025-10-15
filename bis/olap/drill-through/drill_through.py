"""Drill-through: von der verdichteten Zahl zurück zu den Zeilen."""

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


def rows_behind(built, selection):
    """Nennt die Zeilen, aus denen eine Zahl entstanden ist.

    Raises:
        ValueError: bei einer unbekannten Dimension.
    """
    for name in selection:
        if name not in built["dimensions"]:
            raise ValueError("unbekannte Dimension: %s" % name)
    return [row for row in built["rows"]
            if all(row[name] == value for name, value in selection.items())]


def explain(built, selection, measure, how="sum"):
    """Rechnet eine Zahl aus und legt ihre Herkunft daneben.

    Das ist der Zweck der Operation: eine auffällige Kennzahl im Bericht
    lässt sich nur beurteilen, wenn sichtbar wird, aus welchen Zeilen sie
    kommt. Ein Mittelwert über drei Zeilen und einer über dreissig sehen
    im Bericht gleich aus.

    Args:
        built: der Würfel.
        selection: die Auswahl, die zu der Zahl geführt hat.
        measure: die Kennzahl.
        how: die Verdichtung.

    Returns:
        Abbildung mit dem Wert, den Beiträgen, den Zeilen und ihrer Zahl.

    Raises:
        ValueError: bei unbekannter Dimension, Kennzahl oder Verdichtung.
    """
    if measure not in built["measures"]:
        raise ValueError("unbekannte Kennzahl: %s" % measure)
    if how not in AGGREGATES:
        raise ValueError("unbekannte Verdichtung: %s" % how)
    rows = rows_behind(built, selection)
    contributions = [row[measure] for row in rows]
    return {"value": _apply(contributions, how) if rows else None,
            "contributions": contributions, "rows": rows,
            "row count": len(rows), "selection": dict(selection),
            "measure": measure, "how": how}


def when_a_figure_is_thin(built, selection, measure, floor=3):
    """Warnt, wenn zu wenige Zeilen hinter einer Zahl stehen.

    Raises:
        ValueError: bei unbekannter Dimension oder Kennzahl.
    """
    report = explain(built, selection, measure, "count")
    return {"rows": report["value"], "thin": report["value"] < floor,
            "floor": floor,
            "why": "an average over two rows is not an average"}


def difference_to_drill_down():
    """Trennt Drill-through von Drill-down.

    Drill-down bleibt im Würfel und geht eine Ebene tiefer; die Antwort
    ist wieder eine verdichtete Zahl. Drill-through verlässt den Würfel
    und zeigt die Einzelsätze aus dem Vorsystem.
    """
    return {"drill down": "one level deeper, still aggregated",
            "drill through": "out of the cube, the source records",
            "typical use": "explaining an outlier to whoever reported it"}
