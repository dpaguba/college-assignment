"""Die Wahl des Arbeitspunkts nach den Kosten."""

import numpy as np

CASES = ("tp", "fp", "fn", "tn")


def expected_cost(counts, matrix):
    """Die mittleren Kosten je Fall.

    Raises:
        ValueError: bei fehlenden Angaben oder einer leeren Zählung.
    """
    for name in CASES:
        if name not in counts or name not in matrix:
            raise ValueError("es fehlt der Fall: %s" % name)
    total = sum(counts[name] for name in CASES)
    if total <= 0:
        raise ValueError("es wurde nichts gezählt")
    return sum(counts[name] * matrix[name] for name in CASES) / total


def _sample(points=2000, seed=0, share=0.3):
    """Zieht geeichte Wahrscheinlichkeiten und die zugehörigen Klassen."""
    rng = np.random.default_rng(seed)
    probability = rng.uniform(0.0, 1.0, size=points) ** (1.0 / share)
    labels = (rng.uniform(size=points) < probability).astype(int)
    return probability, labels


def counts_at(probability, labels, threshold):
    """Zählt die vier Fälle bei einer Schwelle."""
    chosen = np.asarray(probability) >= threshold
    marks = np.asarray(labels).astype(bool)
    return {"tp": int(np.sum(chosen & marks)),
            "fp": int(np.sum(chosen & ~marks)),
            "fn": int(np.sum(~chosen & marks)),
            "tn": int(np.sum(~chosen & ~marks))}


def best_threshold(miss=5.0, alarm=1.0, steps=200, seed=0, points=2000):
    """Sucht die Schwelle mit den kleinsten Kosten.

    Gesucht wird durch Durchprobieren, ohne Regel. Die Regel kommt
    danach und wird dagegen gehalten.

    Args:
        miss: die Kosten eines übersehenen positiven Falls.
        alarm: die Kosten eines Fehlalarms.
        steps: die Feinheit der Suche.
        seed: der Startwert.
        points: die Grösse der Stichprobe.

    Returns:
        Abbildung mit der besten Schwelle und den Kosten.

    Raises:
        ValueError: bei negativen Kosten.
    """
    if miss < 0 or alarm < 0:
        raise ValueError("Kosten dürfen nicht negativ sein")
    matrix = {"tp": 0.0, "tn": 0.0, "fp": alarm, "fn": miss}
    probability, labels = _sample(points, seed)
    best = None
    for step in range(steps + 1):
        threshold = step / steps
        cost = expected_cost(counts_at(probability, labels, threshold),
                             matrix)
        if best is None or cost < best[0]:
            best = (cost, threshold)
    half = expected_cost(counts_at(probability, labels, 0.5), matrix)
    return {"best threshold": best[1], "cost at the best threshold":
            best[0], "cost at one half": half, "miss": miss,
            "alarm": alarm, "by rule": alarm / (alarm + miss)}


def the_rule_matches_the_search(seed=0, points=40000, steps=400):
    """Prüft die Regel gegen die Suche.

    Bei geeichten Wahrscheinlichkeiten lohnt sich ein Alarm genau dann,
    wenn die Wahrscheinlichkeit mal den Kosten eines Fehlers grösser ist
    als die Kosten des Alarms. Daraus folgt die Schwelle als Verhältnis
    der beiden Kosten, und keine Suche ist nötig.

    Die Suche wird trotzdem gemacht, denn die Regel gilt nur, wenn die
    Wahrscheinlichkeiten geeicht sind, und das ist eine Annahme über das
    Modell und keine über die Kosten.

    Verglichen werden am Ende die Kosten und nicht die Schwellen. Die
    Kostenkurve ist in der Nähe ihres Minimums sehr flach, also wandert
    die gefundene Schwelle mit der Stichprobe, während die Kosten kaum
    reagieren: bei viertausend Beispielen liegt die Suche bei 0.2125 und
    die Regel bei 0.2, und der Unterschied in den Kosten beträgt weniger
    als ein Prozent. Wer nur die Schwellen vergleicht, hält das für eine
    Abweichung; wer die Kosten vergleicht, sieht, dass es keine ist.

    Returns:
        Abbildung mit beiden Schwellen und beiden Kosten.
    """
    miss, alarm = 4.0, 1.0
    matrix = {"tp": 0.0, "tn": 0.0, "fp": alarm, "fn": miss}
    report = best_threshold(miss=miss, alarm=alarm, steps=steps,
                            seed=seed, points=points)
    probability, labels = _sample(points, seed)
    rule = alarm / (alarm + miss)
    at_rule = expected_cost(counts_at(probability, labels, rule), matrix)
    best = report["cost at the best threshold"]
    return {"by rule": rule, "by search": report["best threshold"],
            "cost at the rule": at_rule, "best cost": best,
            "excess of the rule": at_rule / best - 1.0,
            "tolerance": 0.02,
            "the rule": "die Schwelle ist das Verhältnis der Kosten",
            "what it assumes": "geeichte Wahrscheinlichkeiten",
            "why the thresholds differ": "die Kostenkurve ist um ihr "
                                         "Minimum herum sehr flach"}


def accuracy_is_a_cost_matrix(seed=0, points=20000, steps=200):
    """Zeigt, dass die Trefferquote selbst eine Kostenmatrix ist.

    Wer die Trefferquote maximiert, setzt beide Fehlerarten auf
    dieselben Kosten. Das ist eine Entscheidung, auch wenn sie nicht
    ausgesprochen wird, und sie ist meist falsch: einen Zug zu
    verpassen, der das Spiel gewinnt, kostet mehr als einen Zug zu
    machen, der nichts bringt.

    Returns:
        Abbildung mit beiden Schwellen.
    """
    probability, labels = _sample(points, seed)
    even = {"tp": 0.0, "tn": 0.0, "fp": 1.0, "fn": 1.0}
    skewed = {"tp": 0.0, "tn": 0.0, "fp": 1.0, "fn": 9.0}
    found = {}
    for name, matrix in (("accuracy", even), ("cost", skewed)):
        best = None
        for step in range(steps + 1):
            threshold = step / steps
            cost = expected_cost(counts_at(probability, labels,
                                           threshold), matrix)
            if best is None or cost < best[0]:
                best = (cost, threshold)
        found[name] = best[1]
    return {"threshold by accuracy": found["accuracy"],
            "threshold by cost": found["cost"],
            "what accuracy assumes": "beide Fehler kosten gleich viel",
            "why that is a decision": "sie wird getroffen, auch wenn sie "
                                      "nicht ausgesprochen wird"}


def what_it_means_for_a_game_ai():
    """Überträgt die Kostenfrage auf die Zugauswahl.

    Eine KI, die Züge bewertet, wählt ständig einen Arbeitspunkt: wie
    sicher muss ein Zug aussehen, damit er gespielt wird. Die Kosten
    sind hier keine Zahlen aus einer Tabelle, sondern der Verlauf der
    Partie, und sie ändern sich mit dem Stand: wer führt, zahlt für
    einen Fehlschlag mehr als wer zurückliegt.

    Daraus folgt, dass eine feste Schwelle über die ganze Partie
    genauso wenig taugt wie feste Gewichte in der Bewertungsfunktion.
    """
    return {"the operating point": "wie sicher muss ein Zug aussehen",
            "the costs": "der Verlauf der Partie, nicht eine Tabelle",
            "they move": "wer führt, zahlt für einen Fehlschlag mehr",
            "the conclusion": "eine feste Schwelle taugt so wenig wie "
                              "feste Gewichte"}
