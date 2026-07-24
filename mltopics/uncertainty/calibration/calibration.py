"""Wie gut die ausgegebenen Wahrscheinlichkeiten stimmen."""

import numpy as np


def _check(probability, labels):
    """Prüft Wahrscheinlichkeiten und Marken.

    Raises:
        ValueError: bei verschiedenen Längen oder Werten ausserhalb von
            null bis eins.
    """
    values = np.asarray(probability, dtype=float)
    marks = np.asarray(labels, dtype=int)
    if values.shape != marks.shape or values.size == 0:
        raise ValueError("zu jeder Wahrscheinlichkeit gehört eine Marke")
    if np.any(values < 0.0) or np.any(values > 1.0):
        raise ValueError("Wahrscheinlichkeiten liegen zwischen null und "
                         "eins")
    return values, marks


def reliability(probability, labels, bins=10):
    """Teilt die Fälle in Körbe und misst je Korb Anspruch und Wirklichkeit.

    Ein gut geeichtes Modell sagt: von den Fällen, denen ich siebzig
    Prozent gebe, treffen siebzig Prozent zu. Der Korb prüft genau
    diesen Satz.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Körben.
    """
    values, marks = _check(probability, labels)
    if bins <= 0:
        raise ValueError("es braucht mindestens einen Korb")
    edges = np.linspace(0.0, 1.0, bins + 1)
    found = []
    for low, high in zip(edges, edges[1:]):
        inside = (values > low) & (values <= high)
        if low == 0.0:
            inside = inside | (values == 0.0)
        count = int(inside.sum())
        found.append({"from": float(low), "to": float(high),
                      "count": count,
                      "claimed": float(values[inside].mean())
                      if count else 0.0,
                      "observed": float(marks[inside].mean())
                      if count else 0.0})
    return found


def expected_calibration_error(probability, labels, bins=10):
    """Mittelt den Abstand zwischen Anspruch und Wirklichkeit.

    Gewichtet wird nach der Besetzung der Körbe, sodass ein fast leerer
    Korb das Ergebnis nicht bestimmt.

    Raises:
        ValueError: wie bei der Prüfung.
    """
    values, _ = _check(probability, labels)
    rows = reliability(probability, labels, bins)
    total = len(values)
    return float(sum(row["count"] / total
                     * abs(row["claimed"] - row["observed"])
                     for row in rows))


def _sample(size, seed):
    """Zieht geeichte Wahrscheinlichkeiten und die zugehörigen Marken."""
    rng = np.random.default_rng(seed)
    probability = rng.uniform(0.0, 1.0, size=size)
    labels = (rng.uniform(size=size) < probability).astype(int)
    return probability, labels


def perfectly_calibrated(size=20000, seed=0, bins=10):
    """Misst den Fehler eines Modells, das nach Bauart stimmt.

    Raises:
        ValueError: bei einer nicht positiven Grösse.
    """
    if size <= 0:
        raise ValueError("die Grösse muss positiv sein")
    probability, labels = _sample(size, seed)
    return {"expected calibration error":
            expected_calibration_error(probability, labels, bins),
            "accuracy": float(np.mean((probability >= 0.5) == labels)),
            "size": size}


def sharpened(power=3.0, size=20000, seed=0, bins=10):
    """Schärft die Wahrscheinlichkeiten und misst, was das kostet.

    Die Vorhersagen werden zu den Rändern gezogen, ohne dass sich die
    Reihenfolge ändert. Damit bleibt jede Entscheidung dieselbe und die
    Trefferquote auch; nur die ausgegebenen Zahlen stimmen nicht mehr.

    Das ist der Grund, warum Kalibrierung eine eigene Messung braucht:
    die Trefferquote sieht sie nicht.

    Raises:
        ValueError: bei einer nicht positiven Schärfe.
    """
    if power <= 0.0:
        raise ValueError("die Schärfe muss positiv sein")
    probability, labels = _sample(size, seed)
    odds = np.clip(probability, 1e-9, 1.0 - 1e-9)
    sharp = odds ** power / (odds ** power + (1.0 - odds) ** power)
    return {"expected calibration error":
            expected_calibration_error(sharp, labels, bins),
            "error before": expected_calibration_error(probability,
                                                       labels, bins),
            "accuracy": float(np.mean((sharp >= 0.5) == labels)),
            "accuracy before": float(np.mean((probability >= 0.5)
                                             == labels)),
            "power": power}


def brier_decomposition(size=20000, seed=0, bins=10):
    """Zerlegt den Brier-Score in seine drei Teile.

    Der mittlere quadratische Fehler der Wahrscheinlichkeiten ist gleich
    Zuverlässigkeit minus Auflösung plus Grundunsicherheit. Die
    Zuverlässigkeit misst, wie weit Anspruch und Wirklichkeit je Korb
    auseinanderliegen, die Auflösung, wie stark die Körbe sich vom
    Gesamtdurchschnitt unterscheiden, und die Grundunsicherheit hängt
    nur an der Häufigkeit der Fälle.

    Die Zerlegung ist eine Identität und damit die Probe auf die ganze
    Rechnung.

    Raises:
        ValueError: bei einer nicht positiven Grösse.
    """
    if size <= 0:
        raise ValueError("die Grösse muss positiv sein")
    probability, labels = _sample(size, seed)
    rows = reliability(probability, labels, bins)
    base = float(labels.mean())
    total = len(labels)
    grouped = np.zeros(total)
    for row in rows:
        inside = (probability > row["from"]) & (probability <= row["to"])
        if row["from"] == 0.0:
            inside = inside | (probability == 0.0)
        grouped[inside] = row["claimed"]
    reliability_part = float(sum(row["count"] / total
                                 * (row["claimed"] - row["observed"]) ** 2
                                 for row in rows))
    resolution = float(sum(row["count"] / total
                           * (row["observed"] - base) ** 2
                           for row in rows))
    return {"brier": float(np.mean((grouped - labels) ** 2)),
            "reliability": reliability_part, "resolution": resolution,
            "uncertainty": base * (1.0 - base), "bins": bins}


def temperature_repairs_it(power=3.0, size=20000, seed=0, bins=10):
    """Dreht die Schärfung mit einem einzigen Parameter zurück.

    Gesucht wird die Zahl, mit der die Werte wieder auseinandergezogen
    werden, sodass der Kalibrierungsfehler am kleinsten wird. Weil die
    Umformung streng steigend ist, bleibt die Trefferquote unberührt:
    Kalibrierung und Trennschärfe sind zwei getrennte Eigenschaften, und
    die eine lässt sich nachträglich reparieren, die andere nicht.

    Returns:
        Abbildung mit dem Fehler vor und nach der Anpassung.
    """
    probability, labels = _sample(size, seed)
    odds = np.clip(probability, 1e-9, 1.0 - 1e-9)
    sharp = odds ** power / (odds ** power + (1.0 - odds) ** power)
    before = expected_calibration_error(sharp, labels, bins)
    best = (before, 1.0)
    for temperature in np.linspace(0.2, 3.0, 57):
        cooled = (sharp ** (1.0 / temperature)
                  / (sharp ** (1.0 / temperature)
                     + (1.0 - sharp) ** (1.0 / temperature)))
        error = expected_calibration_error(cooled, labels, bins)
        if error < best[0]:
            best = (error, temperature)
    temperature = best[1]
    cooled = (sharp ** (1.0 / temperature)
              / (sharp ** (1.0 / temperature)
                 + (1.0 - sharp) ** (1.0 / temperature)))
    return {"error before": before, "error after": best[0],
            "temperature": temperature,
            "accuracy before": float(np.mean((sharp >= 0.5) == labels)),
            "accuracy after": float(np.mean((cooled >= 0.5) == labels)),
            "why the accuracy cannot change": "die Umformung ist streng "
                                              "steigend"}


def what_calibration_is_not():
    """Trennt Kalibrierung von Trennschärfe.

    Ein Modell, das jedem Fall die Grundrate zuweist, ist perfekt
    geeicht und völlig nutzlos. Ein Modell, das perfekt trennt, kann
    beliebig schlecht geeicht sein. Beide Eigenschaften werden gebraucht
    und beide werden getrennt gemessen; wer nur eine berichtet, sagt
    nichts über die andere.
    """
    return {"calibrated and useless": "jedem Fall die Grundrate geben",
            "sharp and miscalibrated": "perfekt trennen und die Zahlen "
                                       "danebenlegen",
            "what follows": "beide Eigenschaften getrennt messen",
            "which one is repairable": "die Kalibrierung, nachträglich "
                                       "mit einem Parameter"}
