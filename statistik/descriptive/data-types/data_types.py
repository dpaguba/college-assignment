"""Scales of measurement, and what each one permits.

The scale decides which computations are meaningful, and the ordering of the
scales is an ordering of permissions: whatever may be done with nominal data
may be done with ordinal data, and whatever may be done with ordinal data may
be done with metric data. Averaging shirt numbers is arithmetically possible
and answers nothing, which is why the check exists.
"""

SCALES = {
    "nominal": ["mode"],
    "binary": ["mode"],
    "ordinal": ["mode", "median", "quantile"],
    "discrete": ["mode", "median", "quantile", "mean", "variance"],
    "continuous": ["mode", "median", "quantile", "mean", "variance"],
    "metric": ["mode", "median", "quantile", "mean", "variance"],
}
"""Which measures each scale admits."""


def allowed(scale):
    """The measures that may be computed on this scale."""
    if scale not in SCALES:
        raise ValueError("unknown scale: %s" % scale)
    return SCALES[scale]


def check(measure, scale):
    """Raises when the measure is not defined for the scale."""
    if measure not in allowed(scale):
        raise ValueError("%s is not defined for %s data" % (measure, scale))
    return True


def classify(name):
    """The scale of a variable, by the examples the first sheet asks for."""
    table = {
        "Name des Stadions": "nominal", "Name der Stadt": "nominal",
        "Wochentag": "nominal", "Tabellenplatz": "ordinal",
        "Weltranglistenplatz": "ordinal", "Anzahl Tore": "discrete",
        "Anzahl gelbe Karten": "discrete", "Zuschauerzahl": "discrete",
        "Temperatur": "continuous", "Laufstrecke": "continuous",
        "Flutlicht": "binary",
    }
    if name not in table:
        raise ValueError("no classification for: %s" % name)
    return table[name]


def is_qualitative(scale):
    """Whether the values are labels rather than quantities."""
    return scale in ("nominal", "ordinal", "binary")
