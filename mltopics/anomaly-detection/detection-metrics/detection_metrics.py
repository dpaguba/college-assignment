"""Messen, wenn der gesuchte Fall sehr selten ist."""

import numpy as np


def _check(scores, labels):
    """Prüft Bewertungen und Marken.

    Raises:
        ValueError: bei verschiedenen Längen oder nur einer Klasse.
    """
    values = np.asarray(scores, dtype=float)
    marks = np.asarray(labels, dtype=int)
    if values.shape != marks.shape or values.size == 0:
        raise ValueError("zu jeder Bewertung gehört genau eine Marke")
    if set(marks.tolist()) != {0, 1}:
        raise ValueError("es braucht beide Klassen")
    return values, marks


def average_precision(scores, labels):
    """Die mittlere Präzision über die Rangliste.

    Aufaddiert wird die Präzision an jeder Stelle, an der ein wirklicher
    Fall steht, geteilt durch die Anzahl der wirklichen Fälle. Anders
    als die Fläche unter der Kennlinie hängt sie an der Häufigkeit, und
    genau deshalb ist sie bei seltenen Fällen die aussagekräftigere
    Zahl.

    Raises:
        ValueError: wie bei der Prüfung.
    """
    values, marks = _check(scores, labels)
    order = np.argsort(-values, kind="stable")
    found = 0
    total = 0.0
    for position, index in enumerate(order, start=1):
        if marks[index] == 1:
            found += 1
            total += found / position
    return float(total / marks.sum())


def auc(scores, labels):
    """Die Fläche unter der Kennlinie, über Paare gezählt.

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


def f1(scores, labels, threshold):
    """Das harmonische Mittel aus Präzision und Trefferquote.

    Raises:
        ValueError: wie bei der Prüfung.
    """
    values, marks = _check(scores, labels)
    chosen = values >= threshold
    hits = float(np.sum(chosen & (marks == 1)))
    if hits == 0.0:
        return 0.0
    precision = hits / float(np.sum(chosen))
    recall = hits / float(np.sum(marks == 1))
    return 2.0 * precision * recall / (precision + recall)


def best_f1(steps=200, seed=0, size=4000, rate=0.02):
    """Sucht die Schwelle mit dem höchsten Mass.

    Raises:
        ValueError: bei einer unzulässigen Häufigkeit.
    """
    scores, labels = _sample(size, rate, seed)
    thresholds = np.linspace(float(scores.min()), float(scores.max()),
                             steps)
    values = [f1(scores, labels, threshold) for threshold in thresholds]
    best = int(np.argmax(values))
    return {"best threshold": float(thresholds[best]),
            "best f1": values[best],
            "f1 at one half": f1(scores, labels, 0.5),
            "rate": rate}


def _sample(size, rate, seed, separation=2.0):
    """Zieht Bewertungen mit einem gegebenen Anteil wirklicher Fälle.

    Raises:
        ValueError: bei einer Häufigkeit ausserhalb von null bis eins.
    """
    if not 0.0 < rate < 1.0:
        raise ValueError("der Anteil liegt zwischen null und eins")
    rng = np.random.default_rng(seed)
    positives = max(2, int(size * rate))
    negatives = size - positives
    scores = np.concatenate([rng.normal(separation, 1.0, positives),
                             rng.normal(0.0, 1.0, negatives)])
    labels = np.array([1] * positives + [0] * negatives)
    return scores, labels


def chance_level(rate=0.01, size=20000, seed=0):
    """Misst beide Masse für einen Detektor ohne Information.

    Die Fläche unter der Kennlinie liegt bei einem halben, gleich wie
    selten der Fall ist. Die mittlere Präzision liegt bei der
    Häufigkeit selbst. Damit hat die eine Zahl einen festen Nullpunkt
    und die andere nicht, und eine mittlere Präzision von 0.05 kann
    hervorragend oder wertlos sein, je nachdem, wie selten der Fall ist.

    Raises:
        ValueError: bei einer unzulässigen Häufigkeit.
    """
    scores, labels = _sample(size, rate, seed, separation=0.0)
    return {"rate": rate, "auc": auc(scores, labels),
            "average precision": average_precision(scores, labels),
            "why": "die mittlere Präzision hat keinen festen Nullpunkt"}


def roc_stays_the_curve_moves(seed=0, size=20000):
    """Vergleicht beide Masse bei zwei Häufigkeiten.

    Dieselbe Trennschärfe, einmal mit einem Zehntel und einmal mit einem
    Hundertstel wirklicher Fälle. Die Fläche unter der Kennlinie bleibt
    stehen, die mittlere Präzision bricht ein. Wer die erste Zahl
    berichtet, verschweigt damit die für den Anwender entscheidende
    Eigenschaft der Aufgabe.

    Returns:
        Abbildung mit beiden Massen bei beiden Häufigkeiten.
    """
    found = {}
    for rate in (0.1, 0.01):
        scores, labels = _sample(size, rate, seed)
        found[rate] = {"auc": auc(scores, labels),
                       "average precision": average_precision(scores,
                                                              labels)}
    return {"auc at ten percent": found[0.1]["auc"],
            "auc at one percent": found[0.01]["auc"],
            "average precision at ten percent":
                found[0.1]["average precision"],
            "average precision at one percent":
                found[0.01]["average precision"],
            "why": "die Fläche normiert beide Klassen getrennt"}


def point_adjustment(length=2000, segments=10, width=20, seed=0):
    """Misst, was das übliche Anpassen bei Zeitreihen anrichtet.

    Bei der verbreiteten Auswertung gilt ein ganzer auffälliger
    Abschnitt als erkannt, sobald irgendein Punkt darin gemeldet wurde.
    Das soll berücksichtigen, dass die genaue Grenze eines Abschnitts
    unscharf ist, und es hebt die Zahlen weit über das Verdiente.

    Der Beleg ist ein Detektor, der rein zufällig meldet. Ohne Anpassung
    liegt sein Mass bei der Häufigkeit; mit Anpassung kommt er auf einen
    Wert, den man für ein gutes Verfahren halten würde, denn bei zwanzig
    Punkten je Abschnitt genügt ein Treffer.

    Returns:
        Abbildung mit den Massen vor und nach der Anpassung.

    Raises:
        ValueError: bei unzulässigen Angaben.
    """
    if segments * width >= length or width < 1:
        raise ValueError("die Abschnitte passen nicht in die Reihe")
    rng = np.random.default_rng(seed)
    truth = np.zeros(length, dtype=int)
    starts = rng.choice(length - width, size=segments, replace=False)
    for start in starts:
        truth[start:start + width] = 1
    detector = (rng.uniform(size=length) < 0.05).astype(int)
    good = truth.copy()
    good[rng.uniform(size=length) < 0.3] = 0
    found = {}
    for name, guess in (("random", detector), ("weak", good)):
        found[name] = {"plain": _f1_of(truth, guess),
                       "adjusted": _f1_of(truth, _adjust(truth, guess))}
    return {"f1 before adjusting": found["weak"]["plain"],
            "f1 after adjusting": found["weak"]["adjusted"],
            "f1 of a random detector before adjusting":
                found["random"]["plain"],
            "f1 of a random detector after adjusting":
                found["random"]["adjusted"],
            "segments": segments, "width": width,
            "why": "ein einziger Treffer erklärt einen ganzen Abschnitt "
                   "für erkannt"}


def _adjust(truth, guess):
    """Erklärt einen Abschnitt für erkannt, wenn ein Punkt gemeldet ist."""
    adjusted = np.asarray(guess).copy()
    inside = False
    start = 0
    for index in range(len(truth) + 1):
        marked = index < len(truth) and truth[index] == 1
        if marked and not inside:
            inside, start = True, index
        elif not marked and inside:
            if np.any(np.asarray(guess)[start:index] == 1):
                adjusted[start:index] = 1
            inside = False
    return adjusted


def _f1_of(truth, guess):
    """Das Mass zweier binärer Folgen."""
    hits = float(np.sum((truth == 1) & (guess == 1)))
    if hits == 0.0:
        return 0.0
    precision = hits / float(np.sum(guess == 1))
    recall = hits / float(np.sum(truth == 1))
    return 2.0 * precision * recall / (precision + recall)


def what_to_report():
    """Sagt, welche Zahlen zusammen gehören.

    Die Häufigkeit der wirklichen Fälle, denn ohne sie ist die mittlere
    Präzision nicht einzuordnen. Beide Masse, denn sie beantworten
    verschiedene Fragen. Und die Auswertungsvorschrift, denn die
    Anpassung bei Zeitreihen verändert die Zahlen um ein Vielfaches.
    """
    return {"always with": ["die Häufigkeit der Fälle",
                            "beide Masse",
                            "die Auswertungsvorschrift"],
            "why the rate": "ohne sie ist die mittlere Präzision nicht "
                            "einzuordnen",
            "why the protocol": "das Anpassen verändert die Zahlen um "
                                "ein Vielfaches"}
