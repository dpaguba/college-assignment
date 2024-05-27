"""Silhouetten-Koeffizient zur Bewertung einer Gruppierung."""

import math


def _distance(first, second):
    """Euklidischer Abstand zweier Punkte."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(first, second)))


def per_point(points, labels):
    """Berechnet den Silhouettenwert jedes Punktes.

    Der Wert vergleicht den mittleren Abstand innerhalb der eigenen Gruppe
    mit dem zur nächstgelegenen fremden Gruppe: (b − a) / max(a, b).

    Returns:
        Liste der Werte in der Reihenfolge der Punkte.

    Raises:
        ValueError: wenn es weniger als zwei Gruppen gibt.
    """
    groups = sorted(set(labels))
    if len(groups) < 2:
        raise ValueError("mindestens zwei Gruppen noetig")
    values = []
    for index, point in enumerate(points):
        own = labels[index]
        inside = [_distance(point, other)
                  for position, other in enumerate(points)
                  if labels[position] == own and position != index]
        a = sum(inside) / len(inside) if inside else 0.0
        b = None
        for group in groups:
            if group == own:
                continue
            outside = [_distance(point, other)
                       for position, other in enumerate(points)
                       if labels[position] == group]
            if not outside:
                continue
            mean = sum(outside) / len(outside)
            b = mean if b is None else min(b, mean)
        if b is None or max(a, b) == 0:
            values.append(0.0)
        else:
            values.append((b - a) / max(a, b))
    return values


def coefficient(points, labels):
    """Mittelt die Silhouettenwerte über alle Punkte."""
    values = per_point(points, labels)
    return sum(values) / len(values)


def best_k(points, candidates):
    """Wählt die Gruppenzahl mit dem höchsten Koeffizienten.

    Args:
        points: die Datenpunkte.
        candidates: zu prüfende Gruppenzahlen, mindestens zwei je Wert.

    Returns:
        Die beste Gruppenzahl.

    Raises:
        ValueError: wenn keine Gruppenzahl geprüft werden konnte.
    """
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                    "k-means"))
    import k_means
    best = None
    for k in candidates:
        if not 2 <= k < len(points):
            continue
        labels = k_means.cluster(points, k, seed=0)["labels"]
        if len(set(labels)) < 2:
            continue
        score = coefficient(points, labels)
        if best is None or score > best[1]:
            best = (k, score)
    if best is None:
        raise ValueError("keine brauchbare Gruppenzahl")
    return best[0]


def interpretation():
    """Nennt die übliche Lesart der Werte."""
    return {"above 0.7": "strong structure",
            "0.5 to 0.7": "reasonable structure",
            "0.25 to 0.5": "weak structure",
            "below 0.25": "no substantial structure"}
