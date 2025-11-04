"""Kreuzvalidierung und die Grenzen ihrer Aussage."""

import numpy as np


def folds(count, parts):
    """Teilt die Indizes in möglichst gleich grosse Teile.

    Die Teile überschneiden sich nicht und decken alles ab, also wird
    jedes Beispiel genau einmal validiert und in allen übrigen
    Durchläufen zum Training verwendet.

    Args:
        count: die Anzahl der Beispiele.
        parts: die Anzahl der Teile.

    Returns:
        Liste der Indexlisten.

    Raises:
        ValueError: bei weniger als zwei Teilen oder mehr Teilen als
            Beispielen.
    """
    if parts < 2:
        raise ValueError("mindestens zwei Teile")
    if parts > count:
        raise ValueError("mehr Teile als Beispiele")
    return [list(range(index, count, parts)) for index in range(parts)]


def _nearest_labels(train, labels, query, k):
    """Nennt die Kategorien der k nächsten Nachbarn.

    Der Klassifikator steht hier noch einmal in wenigen Zeilen, damit das
    Modul für sich lauffähig bleibt.
    """
    points = np.asarray(train, dtype=float)
    target = np.asarray(query, dtype=float)
    measured = np.sqrt(((points - target) ** 2).sum(axis=1))
    order = np.argsort(measured, kind="stable")[:k]
    return [labels[index] for index in order]


def _majority(chosen):
    """Bestimmt die häufigste Kategorie, bei Gleichstand die nächste."""
    counts = {}
    for label in chosen:
        counts[label] = counts.get(label, 0) + 1
    best = max(counts.values())
    for label in chosen:
        if counts[label] == best:
            return label
    return None


def run(matrix, labels, parts=5, k=1):
    """Führt die Kreuzvalidierung durch und mittelt die Fehlerraten.

    Args:
        matrix: die Merkmalsvektoren.
        labels: ihre Kategorien.
        parts: die Anzahl der Teile.
        k: die Anzahl der Nachbarn.

    Returns:
        Abbildung mit der mittleren Fehlerrate und den einzelnen Läufen.

    Raises:
        ValueError: bei unpassend vielen Kategorien oder unzulässiger
            Teilung.
    """
    points = np.asarray(matrix, dtype=float)
    if len(points) != len(labels):
        raise ValueError("zu jedem Vektor gehört genau eine Kategorie")
    parted = folds(len(points), parts)
    rates = []
    validated = 0
    for part in parted:
        keep = [index for index in range(len(points)) if index not in part]
        train = points[keep]
        train_labels = [labels[index] for index in keep]
        wrong = 0
        for index in part:
            chosen = _nearest_labels(train, train_labels, points[index],
                                     min(k, len(train)))
            if _majority(chosen) != labels[index]:
                wrong += 1
        validated += len(part)
        rates.append(wrong / len(part))
    return {"error rate": float(np.mean(rates)), "rates": rates,
            "validated": validated, "parts": parts, "k": k}


def base_rate(labels):
    """Nennt die Fehlerrate, die ohne jedes Lernen erreichbar ist.

    Wer immer die häufigste Kategorie nennt, irrt so oft, wie die
    übrigen Kategorien zusammen vorkommen. Jede gemessene Fehlerrate ist
    gegen diese Zahl zu halten und nicht gegen null.

    Raises:
        ValueError: bei einer leeren Liste.
    """
    if not labels:
        raise ValueError("leere Liste")
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    best = max(counts.values())
    return {"majority": max(counts, key=lambda name: counts[name]),
            "majority share": best / len(labels),
            "error of always guessing it": 1.0 - best / len(labels)}


def the_optimistic_bias(seed=17):
    """Zeigt, was passiert, wenn k auf den Validierungsdaten gewählt wird.

    Die Daten hier tragen keine Struktur: die Kategorien sind gewürfelt,
    also ist jede Fehlerrate unter der Hälfte Zufall. Wer über mehrere k
    hinweg das beste Ergebnis nimmt, findet trotzdem eines, das deutlich
    besser aussieht. Auf frischen Daten mit demselben k verschwindet der
    Vorteil.

    Das ist der Grund für den Satz auf der Folie, dass sich Fehlerraten
    aus der Validierung in der Regel nicht auf unbekannte Daten
    verallgemeinern lassen.

    Returns:
        Abbildung mit beiden Fehlerraten und dem gewählten k.
    """
    rng = np.random.default_rng(seed)
    points = rng.normal(size=(120, 5))
    labels = [str(int(value)) for value in rng.integers(0, 2, size=120)]
    fresh = rng.normal(size=(120, 5))
    fresh_labels = [str(int(value)) for value
                    in rng.integers(0, 2, size=120)]
    tried = {}
    for k in (1, 3, 5, 7, 9, 11, 15, 21):
        tried[k] = run(points, labels, parts=6, k=k)["error rate"]
    chosen = min(tried, key=lambda key: tried[key])
    wrong = 0
    for vector, label in zip(fresh, fresh_labels):
        chosen_labels = _nearest_labels(points, labels, vector, chosen)
        if _majority(chosen_labels) != label:
            wrong += 1
    return {"tried": tried, "chosen k": chosen,
            "error on the validation data": tried[chosen],
            "error on fresh data": wrong / len(fresh_labels),
            "what it means": "die Wahl von k wurde mit denselben Daten "
                             "gemessen, mit denen sie getroffen wurde"}


def what_the_lecture_warns_about():
    """Nennt die Warnung von der Folie und ihren Grund.

    Ohne getrennten Testdatensatz misst die Validierung zwei Dinge auf
    einmal: wie gut das Verfahren ist und wie gut seine Einstellungen zu
    genau diesen Daten passen. Der zweite Teil überträgt sich nicht.
    """
    return {"the warning": "Fehlerraten aus der Validierung "
                           "verallgemeinern sich in der Regel nicht",
            "the reason": "die Einstellungen wurden auf denselben Daten "
                          "gewählt",
            "the fix": "ein dritter, nie angefasster Datensatz"}
