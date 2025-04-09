"""Die Kennlinie und ihre Fläche."""

import numpy as np


def _check(scores, labels):
    """Prüft Bewertungen und Klassen.

    Raises:
        ValueError: bei verschiedenen Längen oder nur einer Klasse.
    """
    values = np.asarray(scores, dtype=float)
    marks = np.asarray(labels, dtype=int)
    if values.shape != marks.shape or values.size == 0:
        raise ValueError("zu jeder Bewertung gehört genau eine Klasse")
    if set(marks.tolist()) != {0, 1}:
        raise ValueError("es braucht beide Klassen")
    return values, marks


def curve(scores, labels):
    """Rechnet die Punkte der Kennlinie aus.

    Durchlaufen werden alle Schwellen von der höchsten zur niedrigsten.
    Bei jeder wird gezählt, welcher Anteil der positiven und welcher
    Anteil der negativen Beispiele als positiv gilt. Der erste Anteil
    ist die Trefferrate, der zweite die Fehlalarmrate.

    Raises:
        ValueError: wie bei der Prüfung.
    """
    values, marks = _check(scores, labels)
    order = np.argsort(-values, kind="stable")
    positives = float(marks.sum())
    negatives = float(len(marks) - positives)
    hits = 0.0
    alarms = 0.0
    true_rate = [0.0]
    false_rate = [0.0]
    previous = None
    for index in order:
        if previous is not None and values[index] != previous:
            true_rate.append(hits / positives)
            false_rate.append(alarms / negatives)
        if marks[index] == 1:
            hits += 1.0
        else:
            alarms += 1.0
        previous = values[index]
    true_rate.append(hits / positives)
    false_rate.append(alarms / negatives)
    return {"true positive rate": true_rate,
            "false positive rate": false_rate,
            "positives": int(positives), "negatives": int(negatives)}


def auc(scores, labels):
    """Die Fläche unter der Kennlinie, nach der Trapezregel.

    Raises:
        ValueError: wie bei der Prüfung.
    """
    points = curve(scores, labels)
    return float(np.trapezoid(points["true positive rate"],
                              points["false positive rate"]))


def auc_by_pairs(scores, labels):
    """Dieselbe Zahl, gezählt über alle Paare.

    Die Fläche ist die Wahrscheinlichkeit, dass ein zufällig gewähltes
    positives Beispiel höher bewertet wird als ein zufällig gewähltes
    negatives, wobei ein Gleichstand als halber Treffer zählt. Diese
    Rechnung hat mit der Trapezregel nichts gemein und ist deshalb die
    Probe.

    Raises:
        ValueError: wie bei der Prüfung.
    """
    values, marks = _check(scores, labels)
    positives = values[marks == 1]
    negatives = values[marks == 0]
    better = 0.0
    for value in positives:
        better += float(np.sum(value > negatives))
        better += 0.5 * float(np.sum(value == negatives))
    return better / (len(positives) * len(negatives))


def guessing(points=400, seed=0):
    """Misst die Fläche für Bewertungen ohne Information.

    Raises:
        ValueError: bei zu wenigen Punkten.
    """
    if points < 4:
        raise ValueError("zu wenige Punkte")
    rng = np.random.default_rng(seed)
    labels = list(rng.integers(0, 2, size=points))
    if len(set(labels)) < 2:
        raise ValueError("es braucht beide Klassen")
    scores = rng.normal(size=points)
    return {"auc": auc(scores, labels), "points": points,
            "what it means": "die Kennlinie liegt auf der Diagonalen"}


def monotone_invariance(scores, labels):
    """Zeigt, dass nur die Reihenfolge zählt.

    Jede streng steigende Umformung der Bewertungen lässt die Fläche
    unverändert, denn sie ändert keine Reihenfolge. Deshalb misst die
    Fläche die Güte der Sortierung und nicht die Güte der
    Wahrscheinlichkeiten: ein Verfahren mit völlig falsch geeichten
    Wahrscheinlichkeiten kann eine Fläche von eins erreichen.

    Raises:
        ValueError: wie bei der Prüfung.
    """
    values, _ = _check(scores, labels)
    turned = np.exp(values / 3.0)
    return {"auc": auc(values, labels), "after": auc(turned, labels),
            "transform": "exp(x/3), streng steigend",
            "what it means": "die Fläche misst die Sortierung, nicht die "
                             "Eichung"}


def imbalance_does_not_move_it(seed=0):
    """Vergleicht die Fläche mit der Präzision bei schiefen Klassen.

    Dieselbe Trennschärfe, einmal mit gleich vielen und einmal mit
    einem Zwanzigstel positiven Beispielen. Die Fläche bleibt fast
    gleich, weil sie beide Klassen getrennt normiert. Die Präzision
    bricht ein, weil sie die Fehlalarme an der Zahl der positiven misst
    und davon plötzlich sehr wenige da sind.

    Beide Zahlen sind richtig; sie beantworten verschiedene Fragen, und
    die Fläche beantwortet die Frage nach dem Nutzen für den Anwender
    gerade nicht.

    Returns:
        Abbildung mit beiden Massen in beiden Lagen.
    """
    rng = np.random.default_rng(seed)
    found = {}
    for name, positives, negatives in (("balanced", 500, 500),
                                       ("imbalanced", 50, 1000)):
        scores = np.concatenate([rng.normal(1.0, 1.0, positives),
                                 rng.normal(-1.0, 1.0, negatives)])
        labels = [1] * positives + [0] * negatives
        chosen = scores > 0.0
        hits = float(np.sum(chosen[:positives]))
        alarms = float(np.sum(chosen[positives:]))
        found[name] = {"auc": auc(scores, labels),
                       "precision": hits / max(1.0, hits + alarms)}
    return {"auc balanced": found["balanced"]["auc"],
            "auc imbalanced": found["imbalanced"]["auc"],
            "precision balanced": found["balanced"]["precision"],
            "precision imbalanced": found["imbalanced"]["precision"],
            "why": "die Fläche normiert beide Klassen getrennt"}
