"""Slicing und Dicing: den Würfel beschneiden."""


def slice_cube(built, dimension, value):
    """Schneidet eine Scheibe heraus und verliert dabei eine Achse.

    Beim Slicing wird eine Dimension auf genau eine Ausprägung
    festgelegt. Danach trägt sie keine Information mehr und fällt aus der
    Darstellung: aus einem dreidimensionalen Würfel wird eine
    zweidimensionale Fläche.

    Args:
        built: der Würfel.
        dimension: die festzulegende Achse.
        value: die Ausprägung.

    Returns:
        Abbildung mit den verbliebenen Zeilen und Achsen.

    Raises:
        ValueError: bei einer unbekannten Dimension.
    """
    if dimension not in built["dimensions"]:
        raise ValueError("unbekannte Dimension: %s" % dimension)
    rows = [row for row in built["rows"] if row[dimension] == value]
    remaining = [name for name in built["dimensions"] if name != dimension]
    return {"rows": rows, "dimensions": remaining,
            "fixed": {dimension: value},
            "measures": list(built["measures"]),
            "members": {name: sorted({row[name] for row in rows})
                        for name in remaining}}


def dice(built, selection):
    """Schneidet einen kleineren Würfel heraus und behält alle Achsen.

    Beim Dicing werden mehrere Dimensionen auf je eine Teilmenge ihrer
    Ausprägungen eingeschränkt. Anders als beim Slicing bleibt jede Achse
    erhalten, nur kürzer; das Ergebnis ist wieder ein Würfel derselben
    Dimensionszahl.

    Args:
        built: der Würfel.
        selection: Abbildung von der Dimension auf die erlaubten
            Ausprägungen.

    Returns:
        Abbildung mit den verbliebenen Zeilen und den unveränderten Achsen.

    Raises:
        ValueError: bei einer unbekannten Dimension oder einer leeren
            Auswahl.
    """
    for name, values in selection.items():
        if name not in built["dimensions"]:
            raise ValueError("unbekannte Dimension: %s" % name)
        if not values:
            raise ValueError("leere Auswahl für %s" % name)
    rows = [row for row in built["rows"]
            if all(row[name] in values for name, values in selection.items())]
    return {"rows": rows, "dimensions": list(built["dimensions"]),
            "restricted": {name: list(values)
                           for name, values in selection.items()},
            "measures": list(built["measures"]),
            "members": {name: sorted({row[name] for row in rows})
                        for name in built["dimensions"]}}


def difference():
    """Stellt die beiden Operationen gegenüber.

    Der Unterschied wird oft übersehen, weil beide Ergebnisse gleich viele
    Zeilen haben können. Er liegt in den Achsen: nach dem Slicing ist eine
    weg, nach dem Dicing sind alle noch da.
    """
    return {"slicing": {"fixes": "one dimension to one value",
                        "dimensions after": "one fewer"},
            "dicing": {"fixes": "several dimensions to a subset each",
                       "dimensions after": "the same"},
            "same row count possible": True}
