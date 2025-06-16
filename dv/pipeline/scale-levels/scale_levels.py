"""Skalenniveaus und was auf ihnen zulässig ist."""

OPERATIONS = {
    "nominal": ["equality", "mode", "frequency"],
    "ordinal": ["equality", "mode", "frequency", "order", "median"],
    "interval": ["equality", "mode", "frequency", "order", "median",
                 "difference", "mean", "standard deviation"],
    "ratio": ["equality", "mode", "frequency", "order", "median",
              "difference", "mean", "standard deviation", "ratio",
              "geometric mean"],
}

PLOTS = {
    "nominal": ["bar chart", "pie chart"],
    "ordinal": ["bar chart", "box plot"],
    "interval": ["histogram", "line chart", "scatter plot"],
    "ratio": ["histogram", "line chart", "scatter plot", "log scale"],
}


def level(values, ordered=False, has_zero=False):
    """Bestimmt das Skalenniveau einer Merkmalsausprägung.

    Args:
        values: die beobachteten Werte.
        ordered: sagt, ob eine Reihenfolge der Kategorien gemeint ist.
        has_zero: sagt, ob der Nullpunkt eine Bedeutung hat.

    Returns:
        Einer der Namen ``nominal``, ``ordinal``, ``interval``, ``ratio``.

    Raises:
        ValueError: bei einer leeren Wertemenge.
    """
    if not values:
        raise ValueError("keine Werte")
    numeric = all(isinstance(value, (int, float)) for value in values)
    if not numeric:
        return "ordinal" if ordered else "nominal"
    return "ratio" if has_zero else "interval"


def admissible(scale):
    """Nennt die auf diesem Niveau zulässigen Operationen.

    Raises:
        ValueError: bei einem unbekannten Niveau.
    """
    if scale not in OPERATIONS:
        raise ValueError("unbekanntes Skalenniveau")
    return list(OPERATIONS[scale])


def plots(scale):
    """Nennt die auf diesem Niveau sinnvollen Diagrammarten."""
    if scale not in PLOTS:
        raise ValueError("unbekanntes Skalenniveau")
    return list(PLOTS[scale])


def ratio_is_meaningful(scale):
    """Sagt, ob der Quotient zweier Werte eine Aussage trägt.

    Auf einer Intervallskala liegt der Nullpunkt willkürlich, deshalb ist
    20 °C nicht doppelt so warm wie 10 °C. Erst mit einem echten Nullpunkt
    wird der Quotient sinnvoll.
    """
    if scale not in OPERATIONS:
        raise ValueError("unbekanntes Skalenniveau")
    return scale == "ratio"


def transformations_that_keep_the_level():
    """Nennt die Transformationen, unter denen ein Niveau erhalten bleibt."""
    return {"nominal": "any bijection of the categories",
            "ordinal": "any strictly increasing function",
            "interval": "a x + b with a > 0",
            "ratio": "a x with a > 0"}
