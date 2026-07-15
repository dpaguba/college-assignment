"""Der nächste Punkt mit einer anderen Antwort."""

import numpy as np

NORMS = ("l1", "l2")


def example_model(point):
    """Ein Modell mit einer krummen Grenze.

    Es gibt eine Kreditzusage, wenn Einkommen und Laufzeit zusammen
    über einer Schwelle liegen, wobei das Einkommen stärker zählt.
    """
    values = np.asarray(point, dtype=float)
    return "yes" if 2.0 * values[0] + values[1] > 1.2 else "no"


def _grid(values, steps, low, high):
    """Baut je Merkmal ein Gitter, das den Ausgangswert enthält.

    Ohne den Ausgangswert im Gitter kann ein Merkmal nicht unverändert
    bleiben, und dann sieht jede Antwort so aus, als würde sie alle
    Merkmale anfassen. Das ist ein Artefakt der Diskretisierung und
    keine Eigenschaft der Norm.
    """
    return [np.unique(np.concatenate([np.linspace(low, high, steps),
                                      [value]]))
            for value in values]


def _distance(one, two, norm):
    """Misst den Abstand in der gewählten Norm.

    Raises:
        ValueError: bei einer unbekannten Norm.
    """
    difference = np.asarray(one, dtype=float) - np.asarray(two,
                                                           dtype=float)
    if norm == "l1":
        return float(np.sum(np.abs(difference)))
    if norm == "l2":
        return float(np.sqrt(np.sum(difference ** 2)))
    raise ValueError("unbekannte Norm: %s" % norm)


def nearest(point, model, norm="l2", steps=200, low=0.0, high=1.0,
            fixed=()):
    """Sucht den nächsten Punkt, den das Modell anders beantwortet.

    Gesucht wird auf einem Gitter über den zulässigen Bereich. Merkmale,
    die nicht verändert werden dürfen, bleiben stehen; das ist die
    einzige Stelle, an der die Suche etwas über die Welt wissen muss,
    und ohne sie liefert sie regelmässig Antworten, die niemand umsetzen
    kann.

    Args:
        point: der Ausgangspunkt.
        model: eine Funktion, die eine Antwort liefert.
        norm: das Abstandsmass.
        steps: die Feinheit des Gitters.
        low: die untere Grenze jedes Merkmals.
        high: die obere Grenze.
        fixed: die Indizes der unveränderlichen Merkmale.

    Returns:
        Abbildung mit dem gefundenen Punkt und dem Abstand.

    Raises:
        ValueError: bei einer unbekannten Norm oder wenn das Modell im
            ganzen Bereich dieselbe Antwort gibt.
    """
    if norm not in NORMS:
        raise ValueError("unbekannte Norm: %s" % norm)
    values = np.asarray(point, dtype=float)
    answer = model(values)
    grid = _grid(values, steps, low, high)
    best = None
    for first in grid[0]:
        for second in grid[1]:
            candidate = np.array([first, second])
            for index in fixed:
                candidate[index] = values[index]
            if model(candidate) == answer:
                continue
            measured = _distance(values, candidate, norm)
            if best is None or measured < best[0]:
                best = (measured, candidate)
    if best is None:
        raise ValueError("das Modell antwortet überall gleich")
    return {"point": best[1], "distance": best[0], "norm": norm,
            "from": values, "answer before": answer,
            "answer after": model(best[1])}


def nearest_by_search(point, model, norm="l2", steps=200, low=0.0,
                      high=1.0):
    """Sucht dasselbe durch Sortieren aller Gitterpunkte.

    Diese Rechnung baut die vollständige Liste der Abstände und
    sortiert sie. Sie ist langsamer und geht anders vor, deshalb ist
    die Übereinstimmung eine Probe.

    Raises:
        ValueError: wie bei ``nearest``.
    """
    if norm not in NORMS:
        raise ValueError("unbekannte Norm: %s" % norm)
    values = np.asarray(point, dtype=float)
    answer = model(values)
    grid = _grid(values, steps, low, high)
    found = []
    for first in grid[0]:
        for second in grid[1]:
            candidate = np.array([first, second])
            if model(candidate) != answer:
                found.append((_distance(values, candidate, norm),
                              candidate))
    if not found:
        raise ValueError("das Modell antwortet überall gleich")
    found.sort(key=lambda row: row[0])
    return {"point": found[0][1], "distance": found[0][0], "norm": norm}


def sparse_or_close(point=(0.2, 0.2), steps=300):
    """Vergleicht, was die beiden Normen als Antwort geben.

    Die eine Norm sucht die kleinste Summe der Änderungen und ändert
    deshalb möglichst wenige Merkmale, meist genau eines. Die andere
    sucht die kleinste Strecke und verteilt die Änderung auf alle.

    Für einen Menschen, der etwas tun soll, ist die erste Antwort
    brauchbar und die zweite nicht: «erhöhen Sie Ihr Einkommen um
    dreihundert Euro» lässt sich umsetzen, «ändern Sie alle sieben
    Angaben ein wenig» nicht.

    Returns:
        Abbildung mit beiden Antworten.
    """
    start = np.asarray(point, dtype=float)
    found = {}
    for norm in NORMS:
        report = nearest(start, example_model, norm=norm, steps=steps)
        changed = int(np.sum(np.abs(report["point"] - start) > 1e-6))
        found[norm] = {"point": report["point"].tolist(),
                       "changed": changed, "distance": report["distance"]}
    return {"features touched by the l1 answer": found["l1"]["changed"],
            "features touched by the l2 answer": found["l2"]["changed"],
            "l1 answer": found["l1"]["point"],
            "l2 answer": found["l2"]["point"],
            "why it matters": "eine Anweisung mit einer Änderung lässt "
                              "sich befolgen"}


def the_nearest_is_not_the_useful_one(steps=200):
    """Zeigt eine nächste Antwort, die niemand umsetzen kann.

    Das erste Merkmal steht für etwas Unveränderliches, etwa das Alter.
    Die nächste Antwort ändert genau dieses Merkmal, weil das Modell
    dort am stärksten reagiert. Sie ist richtig gerechnet und nutzlos.

    Wird die Suche eingeschränkt, so wird die Antwort weiter entfernt
    und brauchbar. Der Abstand ist damit das falsche Ziel, solange nicht
    gesagt wird, was sich ändern darf.

    Returns:
        Abbildung mit beiden Antworten.
    """
    start = np.array([0.2, 0.2])
    free = nearest(start, example_model, steps=steps)
    bound = nearest(start, example_model, steps=steps, fixed=(0,))
    return {"nearest changes a fixed feature":
            bool(abs(free["point"][0] - start[0]) > 1e-6),
            "usable changes a fixed feature":
                bool(abs(bound["point"][0] - start[0]) > 1e-6),
            "distance of the nearest one": free["distance"],
            "distance of the usable one": bound["distance"],
            "why": "der Abstand ist das falsche Ziel, solange nicht "
                   "gesagt wird, was sich ändern darf"}


def what_a_counterfactual_does_not_explain():
    """Grenzt ein, was diese Erklärung leistet.

    Sie sagt, was sich ändern müsste, damit die Antwort anders ausfällt.
    Sie sagt nicht, warum das Modell so entscheidet, und sie sagt schon
    gar nicht, ob die Entscheidung richtig ist. Ein Modell, das eine
    unzulässige Grösse verwendet, liefert dazu genauso saubere
    Gegenbeispiele wie ein zulässiges.
    """
    return {"answers": "was sich ändern müsste",
            "does not answer": ["warum das Modell so entscheidet",
                                "ob die Entscheidung richtig ist"],
            "the trap": "auch ein unzulässiges Modell liefert saubere "
                        "Gegenbeispiele"}
