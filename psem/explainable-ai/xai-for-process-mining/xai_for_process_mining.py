"""Erklärungen für Vorhersagen über laufende Prozesse."""

import itertools

TRACES = (
    (("annehmen", "prüfen", "genehmigen", "auszahlen"), 1),
    (("annehmen", "prüfen", "ablehnen"), 0),
    (("annehmen", "prüfen", "nachfordern", "prüfen", "genehmigen",
      "auszahlen"), 1),
    (("annehmen", "prüfen", "nachfordern", "prüfen", "ablehnen"), 0),
    (("annehmen", "prüfen", "eskalieren", "genehmigen", "auszahlen"), 1),
    (("annehmen", "prüfen", "eskalieren", "ablehnen"), 0),
    (("annehmen", "ablehnen"), 0),
)

FEATURES = ("nachfordern", "eskalieren", "länge über vier")


def features_of(trace):
    """Bildet eine Spur auf ihre Merkmale ab.

    Aus einer laufenden Spur werden wenige Merkmale gemacht, weil ein
    Modell über Spuren sonst nichts hat, worauf es sich stützen könnte.
    Genau diese Abbildung ist die Stelle, an der eine Erklärung später
    verständlich wird oder nicht: sie erklärt die Merkmale, nicht die
    Spur.
    """
    return {"nachfordern": 1 if "nachfordern" in trace else 0,
            "eskalieren": 1 if "eskalieren" in trace else 0,
            "länge über vier": 1 if len(trace) > 4 else 0}


def model(values):
    """Ein einfaches Modell für den Ausgang eines Falles.

    Es sagt Auszahlung voraus, wenn der Fall lang ist oder eskaliert
    wurde, und stützt sich damit auf Merkmale, die im Prozess selbst
    nichts bedeuten. Das ist Absicht: die Erklärung soll das zeigen.
    """
    score = (0.6 * values["länge über vier"]
             + 0.3 * values["eskalieren"]
             - 0.1 * values["nachfordern"] + 0.2)
    return score


def shapley_for(trace, background=None):
    """Rechnet die Beiträge der Merkmale für eine Spur aus.

    Args:
        trace: die Spur.
        background: die Spuren, aus denen fehlende Merkmale gezogen
            werden; ohne Angabe alle bekannten.

    Returns:
        Abbildung vom Merkmal auf seinen Beitrag.
    """
    rows = [features_of(other) for other, _ in
            (TRACES if background is None else background)]
    point = features_of(trace)
    count = len(FEATURES)
    import math
    result = {}
    for name in FEATURES:
        others = [other for other in FEATURES if other != name]
        total = 0.0
        for size in range(len(others) + 1):
            weight = (math.factorial(size)
                      * math.factorial(count - size - 1)
                      / math.factorial(count))
            for group in itertools.combinations(others, size):
                present = set(group)
                with_him = _expected(point, rows, present | {name})
                without = _expected(point, rows, present)
                total += weight * (with_him - without)
        result[name] = total
    return result


def _expected(point, rows, present):
    """Die erwartete Vorhersage bei bekannten Merkmalen."""
    total = 0.0
    for other in rows:
        mixed = {name: point[name] if name in present else other[name]
                 for name in FEATURES}
        total += model(mixed)
    return total / len(rows)


def explain(trace):
    """Erklärt die Vorhersage für eine Spur.

    Returns:
        Abbildung mit der Vorhersage, den Beiträgen und der Probe.
    """
    point = features_of(trace)
    base = sum(model(features_of(other)) for other, _ in TRACES) \
        / len(TRACES)
    contributions = shapley_for(trace)
    return {"trace": list(trace), "features": point,
            "prediction": model(point), "base": base,
            "contributions": contributions,
            "adds up": abs(base + sum(contributions.values())
                           - model(point)) < 1e-9}


def what_the_explanation_shows():
    """Nennt, was an der Erklärung dieses Modells auffällt.

    Der grösste Beitrag kommt von der Länge des Falles. Die Länge ist
    aber keine Ursache für die Auszahlung, sondern eine Folge desselben
    Vorgangs: genehmigte Fälle haben einen Schritt mehr, weil die
    Auszahlung darin vorkommt. Das Modell hat also gelernt, das Ergebnis
    am Ergebnis zu erkennen.

    Die Erklärung deckt das auf, und das ist ihr eigentlicher Nutzen bei
    Prozessdaten: nicht die Vorhersage plausibel zu machen, sondern zu
    zeigen, dass ein Merkmal benutzt wird, das zur Vorhersagezeit noch
    gar nicht bekannt sein kann.

    Returns:
        Abbildung mit dem Befund.
    """
    long_case = ("annehmen", "prüfen", "nachfordern", "prüfen",
                 "genehmigen", "auszahlen")
    report = explain(long_case)
    largest = max(report["contributions"],
                  key=lambda name: abs(report["contributions"][name]))
    return {"largest contribution": largest,
            "contributions": {name: round(value, 4) for name, value
                              in report["contributions"].items()},
            "problem": "die Länge ist eine Folge des Ausgangs, keine "
                       "Ursache",
            "name": "Datenleck aus der Zukunft",
            "the use of the explanation": "sie zeigt ein Merkmal, das zur "
                                          "Vorhersagezeit nicht bekannt "
                                          "sein kann"}
