"""Roll-up und Drill-down: die Aggregationsebene wechseln."""

AGGREGATES = ("sum", "mean", "min", "max", "count")


def aggregates():
    """Nennt die Verdichtungen, die hier vorgesehen sind."""
    return list(AGGREGATES)


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


def _check(built, by, measure, how):
    """Prüft Achsen, Kennzahl und Verdichtung.

    Raises:
        ValueError: bei einer unbekannten Dimension, Kennzahl oder
            Verdichtung.
    """
    for name in by:
        if name not in built["dimensions"]:
            raise ValueError("unbekannte Dimension: %s" % name)
    if measure not in built["measures"]:
        raise ValueError("unbekannte Kennzahl: %s" % measure)
    if how not in AGGREGATES:
        raise ValueError("unbekannte Verdichtung: %s" % how)


def roll_up(built, by, measure, how="sum"):
    """Verdichtet auf die genannten Achsen und lässt die anderen fallen.

    Args:
        built: der Würfel.
        by: die Achsen, die bleiben.
        measure: die Kennzahl.
        how: die Verdichtung.

    Returns:
        Abbildung vom Schlüssel auf den Wert; bei einer Achse ist der
        Schlüssel die Ausprägung, bei mehreren ein Tupel.

    Raises:
        ValueError: bei unbekannter Dimension, Kennzahl oder Verdichtung.
    """
    _check(built, by, measure, how)
    groups = {}
    for row in built["rows"]:
        key = tuple(row[name] for name in by)
        groups.setdefault(key if len(by) > 1 else key[0], []).append(
            row[measure])
    return {key: _apply(values, how) for key, values in groups.items()}


def drill_down(built, by, extra, measure, how="sum"):
    """Zerlegt eine Verdichtung um eine weitere Achse.

    Roll-up und Drill-down sind dieselbe Rechnung in zwei Richtungen. Was
    sie verbindet: bei einer additiven Kennzahl muss die Summe der
    feineren Werte den gröberen ergeben. Sobald das nicht mehr stimmt, ist
    entweder die Kennzahl nicht additiv oder die Zerlegung falsch.

    Raises:
        ValueError: bei unbekannter Dimension, Kennzahl oder Verdichtung.
    """
    if extra not in built["dimensions"]:
        raise ValueError("unbekannte Dimension: %s" % extra)
    return roll_up(built, list(by) + [extra], measure, how)


def hierarchy_levels():
    """Nennt die Ebenen, entlang derer verdichtet wird.

    Eine Dimension trägt in der Regel eine Hierarchie: Tag, Monat,
    Quartal, Jahr. Roll-up geht eine Ebene hinauf, Drill-down eine
    hinunter; die Zeitachse dieser Tabelle hat nur Quartal und Jahr.
    """
    return {"Zeit": ["Jahr", "Quartal"],
            "Projekt": ["Portfolio", "Projekt"],
            "Risiko": ["Gesamtrisiko", "Risikoart"],
            "note": "die Tabelle führt nur die unterste Ebene, alles "
                    "andere wird gerechnet"}


def consistency(built, by, extra, measure):
    """Prüft, ob die Zerlegung sich wieder zur Verdichtung addiert.

    Returns:
        Abbildung mit dem Befund je Schlüssel der gröberen Ebene.

    Raises:
        ValueError: bei unbekannter Dimension oder Kennzahl.
    """
    coarse = roll_up(built, by, measure, "sum")
    fine = drill_down(built, by, extra, measure, "sum")
    checked = {}
    for key, total in coarse.items():
        parts = [value for other, value in fine.items()
                 if (other[:len(by)] if len(by) > 1 else other[0]) == key]
        checked[key] = abs(sum(parts) - total) < 1e-9
    return {"consistent": all(checked.values()), "per key": checked}
