"""k-Mittelwert-Clustering nach Lloyd."""

import itertools
import math
import random


def _distance(first, second):
    """Euklidischer Abstand zweier Punkte."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(first, second)))


def _centroid(points):
    """Schwerpunkt einer nichtleeren Punktmenge."""
    dimension = len(points[0])
    return tuple(sum(point[axis] for point in points) / len(points)
                 for axis in range(dimension))


def inertia(points, labels, centres):
    """Summe der quadrierten Abstände zum jeweils zugeordneten Zentrum."""
    return sum(_distance(point, centres[label]) ** 2
               for point, label in zip(points, labels))


def cluster(points, k, seed=0, iterations=100):
    """Führt das Verfahren von Lloyd aus.

    Zufällig gewählte Punkte dienen als Startzentren; danach wechseln
    Zuordnung und Neuberechnung, bis sich nichts mehr ändert.

    Args:
        points: die zu gruppierenden Punkte.
        k: gewünschte Anzahl der Gruppen.
        seed: Startwert des Zufallsgenerators.
        iterations: obere Schranke für die Durchläufe.

    Returns:
        Abbildung mit ``labels``, ``centres``, ``inertia`` und der
        ``history`` der Zielfunktionswerte.

    Raises:
        ValueError: wenn k nicht zwischen eins und der Punktzahl liegt.
    """
    if not 1 <= k <= len(points):
        raise ValueError("k passt nicht zur Punktzahl")
    generator = random.Random(seed)
    centres = [tuple(point)
               for point in generator.sample(list(points), k)]
    history = []
    labels = [0] * len(points)
    for _ in range(iterations):
        labels = [min(range(k), key=lambda index: _distance(point,
                                                            centres[index]))
                  for point in points]
        history.append(inertia(points, labels, centres))
        moved = []
        for index in range(k):
            members = [point for point, label in zip(points, labels)
                       if label == index]
            moved.append(_centroid(members) if members else centres[index])
        if all(_distance(a, b) < 1e-12 for a, b in zip(centres, moved)):
            centres = moved
            break
        centres = moved
    history.append(inertia(points, labels, centres))
    return {"labels": labels, "centres": centres,
            "inertia": inertia(points, labels, centres), "history": history}


def exhaustive_best(points, k):
    """Bestimmt die beste Aufteilung durch vollständige Aufzählung.

    Das Verfahren geht alle Zuordnungen durch und dient als Prüfstein für
    das Ergebnis von Lloyd; es ist nur für wenige Punkte brauchbar.

    Raises:
        ValueError: bei mehr als zwölf Punkten.
    """
    if len(points) > 12:
        raise ValueError("zu viele Punkte fuer die Aufzaehlung")
    best = None
    for assignment in itertools.product(range(k), repeat=len(points)):
        if len(set(assignment)) != k:
            continue
        centres = []
        for index in range(k):
            members = [point for point, label in zip(points, assignment)
                       if label == index]
            centres.append(_centroid(members))
        value = inertia(points, assignment, centres)
        if best is None or value < best["inertia"]:
            best = {"labels": list(assignment), "centres": centres,
                    "inertia": value}
    return best


def depends_on_the_start(seeds=range(20)):
    """Misst, wie oft verschiedene Startwerte verschiedene Ergebnisse geben.

    Die Punktmenge ist so gewählt, dass zwei lokale Minima erreichbar
    sind; das beantwortet die Frage der Übung, ob mehrere Aufrufe immer
    dasselbe liefern.

    Returns:
        Abbildung mit der Zahl verschiedener Zielfunktionswerte und dem
        besten sowie dem schlechtesten davon.
    """
    points = [(0, 0), (0, 1), (1, 0), (1, 1), (4, 0), (8, 0), (8, 1)]
    values = set()
    for seed in seeds:
        values.add(round(cluster(points, 3, seed=seed)["inertia"], 6))
    return {"distinct results": len(values), "best": min(values),
            "worst": max(values)}


def elbow(points, candidates):
    """Berechnet die Zielfunktion für mehrere Gruppenzahlen.

    Returns:
        Abbildung von k auf den erreichten Wert der Zielfunktion.
    """
    return {k: cluster(points, k, seed=0)["inertia"] for k in candidates}
