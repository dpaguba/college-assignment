"""Der k-Nächste-Nachbarn Klassifikator."""

import numpy as np


def _distance(first, second, measure):
    """Rechnet einen Abstand nach dem gewählten Mass aus.

    Raises:
        ValueError: bei einem unbekannten Mass oder einem Nullvektor.
    """
    one = np.asarray(first, dtype=float)
    two = np.asarray(second, dtype=float)
    if measure == "euclidean":
        return float(np.sqrt(np.sum((one - two) ** 2)))
    if measure == "cityblock":
        return float(np.sum(np.abs(one - two)))
    if measure == "cosine":
        lengths = np.linalg.norm(one) * np.linalg.norm(two)
        if lengths == 0.0:
            raise ValueError("der Nullvektor hat keine Richtung")
        return float(1.0 - np.dot(one, two) / lengths)
    raise ValueError("unbekanntes Mass: %s" % measure)


def vote(train, labels, query, k=1, measure="euclidean"):
    """Sucht die k nächsten Nachbarn und lässt sie abstimmen.

    Bei Stimmengleichheit entscheidet der nächste Nachbar unter den
    gleichauf liegenden Klassen. Die Regel ist eine Setzung; sie ist
    nachvollziehbar und hängt nicht von der Reihenfolge der
    Trainingsdaten ab, was für ein zufälliges Auswürfeln nicht gilt.

    Args:
        train: die Trainingsvektoren.
        labels: ihre Kategorien.
        query: der zu klassifizierende Vektor.
        k: die Anzahl der Nachbarn.
        measure: das Abstandsmass.

    Returns:
        Abbildung mit der Entscheidung, den Nachbarn und den Stimmen.

    Raises:
        ValueError: bei einem nicht positiven k, einem k über der Anzahl
            der Trainingsdaten oder unpassend vielen Kategorien.
    """
    if k <= 0:
        raise ValueError("k muss positiv sein")
    if len(train) != len(labels):
        raise ValueError("zu jedem Vektor gehört genau eine Kategorie")
    if k > len(train):
        raise ValueError("k ist grösser als die Trainingsmenge")
    measured = sorted(((_distance(row, query, measure), index)
                       for index, row in enumerate(train)),
                      key=lambda row: (row[0], row[1]))
    neighbours = measured[:k]
    counts = {}
    for _, index in neighbours:
        counts[labels[index]] = counts.get(labels[index], 0) + 1
    best = max(counts.values())
    winners = {label for label, count in counts.items() if count == best}
    chosen = None
    for _, index in neighbours:
        if labels[index] in winners:
            chosen = labels[index]
            break
    return {"label": chosen, "counts": counts,
            "tie": len(winners) > 1,
            "neighbours": [(labels[index], distance)
                           for distance, index in neighbours]}


def classify(train, labels, query, k=1, measure="euclidean"):
    """Nennt die Kategorie eines einzelnen Vektors.

    Raises:
        ValueError: wie bei ``vote``.
    """
    return vote(train, labels, query, k, measure)["label"]


def classify_all(train, labels, queries, k=1, measure="euclidean"):
    """Klassifiziert eine ganze Menge von Vektoren.

    Raises:
        ValueError: wie bei ``vote``.
    """
    return [classify(train, labels, query, k, measure) for query in queries]


def error_rate(predicted, truth):
    """Misst den Anteil der falschen Entscheidungen.

    Raises:
        ValueError: bei einem leeren Vergleich oder verschiedenen Längen.
    """
    if not predicted or len(predicted) != len(truth):
        raise ValueError("leerer Vergleich oder verschiedene Längen")
    wrong = sum(1 for one, two in zip(predicted, truth) if one != two)
    return wrong / len(truth)


def confusion(predicted, truth):
    """Zählt, welche Kategorie mit welcher verwechselt wird.

    Die Fehlerrate sagt, wie oft der Klassifikator irrt; die Matrix sagt,
    wobei. Zwei Verfahren mit derselben Fehlerrate können sich hier stark
    unterscheiden, und für die Frage, was zu verbessern ist, zählt nur
    die Matrix.

    Raises:
        ValueError: bei einem leeren Vergleich oder verschiedenen Längen.
    """
    if not predicted or len(predicted) != len(truth):
        raise ValueError("leerer Vergleich oder verschiedene Längen")
    matrix = {}
    for one, two in zip(truth, predicted):
        matrix.setdefault(one, {})
        matrix[one][two] = matrix[one].get(two, 0) + 1
    return matrix


def why_k_matters():
    """Sagt, was die Wahl von k entscheidet.

    Ein Nachbar folgt jedem Ausreisser und liefert auf den eigenen Daten
    immer null Fehler, was nichts bedeutet. Viele Nachbarn glätten und
    ziehen die Entscheidung zur häufigsten Kategorie hin; bei k gleich
    der Anzahl der Trainingsdaten kommt immer die häufigste Kategorie
    heraus. Dazwischen liegt ein Bereich, der sich nur messen lässt.
    """
    return {"k = 1": "folgt jedem Ausreisser, auf den eigenen Daten "
                     "immer fehlerfrei",
            "k = N": "immer die häufigste Kategorie",
            "in between": "lässt sich nur messen, nicht herleiten",
            "the trap": "wer k auf den Validierungsdaten wählt, misst "
                        "die Wahl mit denselben Daten"}
