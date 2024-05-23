"""Kohonenkarte: eine Gitterstruktur, die sich an die Daten anlegt."""

import math
import random


def _distance(first, second):
    """Euklidischer Abstand zweier Vektoren."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(first, second)))


def best_matching_unit(weights, sample):
    """Sucht die Gitterzelle mit dem kleinsten Abstand zum Datenpunkt.

    Args:
        weights: Gitter als Liste von Zeilen mit Gewichtsvektoren.
        sample: der Datenpunkt.

    Returns:
        Paar (Zeile, Spalte) der Gewinnerzelle.
    """
    best = None
    for row, line in enumerate(weights):
        for column, weight in enumerate(line):
            value = _distance(weight, sample)
            if best is None or value < best[0]:
                best = (value, (row, column))
    return best[1]


def neighbourhood_radius(step, total, start):
    """Berechnet den Nachbarschaftsradius zum Zeitpunkt ``step``.

    Der Radius fällt exponentiell, damit die Karte zuerst grob ausgerichtet
    und später fein angepasst wird.

    Raises:
        ValueError: wenn die Gesamtzahl der Schritte nicht positiv ist.
    """
    if total <= 0:
        raise ValueError("Schrittzahl muss positiv sein")
    return start * math.exp(-step / (total / math.log(start + 1)))


def train(data, width, height, epochs=50, seed=0, start_radius=2.0,
          start_rate=0.5):
    """Lernt eine Karte an.

    Je Schritt wird ein Datenpunkt gezogen, die Gewinnerzelle bestimmt und
    sie samt ihrer Nachbarschaft in Richtung des Punktes gezogen. Lernrate
    und Radius nehmen mit der Zeit ab.

    Returns:
        Das gelernte Gitter als Liste von Zeilen.
    """
    generator = random.Random(seed)
    dimension = len(data[0])
    weights = [[tuple(generator.uniform(0, 1) for _ in range(dimension))
                for _ in range(width)] for _ in range(height)]
    total = epochs * len(data)
    step = 0
    for _ in range(epochs):
        for sample in generator.sample(list(data), len(data)):
            radius = neighbourhood_radius(step, total, start_radius)
            rate = start_rate * math.exp(-step / total)
            row, column = best_matching_unit(weights, sample)
            for other_row in range(height):
                for other_column in range(width):
                    grid = math.hypot(other_row - row, other_column - column)
                    if grid > radius:
                        continue
                    influence = math.exp(-(grid ** 2) / (2 * radius ** 2))
                    weight = weights[other_row][other_column]
                    weights[other_row][other_column] = tuple(
                        value + rate * influence * (target - value)
                        for value, target in zip(weight, sample))
            step += 1
    return weights


def quantisation_error(weights, data):
    """Mittlerer Abstand der Daten zu ihrer Gewinnerzelle."""
    total = 0.0
    for sample in data:
        row, column = best_matching_unit(weights, sample)
        total += _distance(weights[row][column], sample)
    return total / len(data)


def training_reduces_error():
    """Misst den Quantisierungsfehler vor und nach dem Anlernen.

    Returns:
        Abbildung mit beiden Fehlern.
    """
    data = [(0.1, 0.1), (0.15, 0.05), (0.9, 0.9), (0.85, 0.95),
            (0.1, 0.9), (0.05, 0.85)]
    before = train(data, 2, 2, epochs=0, seed=1)
    after = train(data, 2, 2, epochs=60, seed=1)
    return {"before": quantisation_error(before, data),
            "after": quantisation_error(after, data)}


def topology_is_preserved():
    """Prüft, ob benachbarte Zellen benachbarte Gewichte tragen.

    Auf Daten entlang einer Linie soll eine eindimensionale Karte die
    Reihenfolge übernehmen: die Gewichte müssen entlang der Kette monoton
    verlaufen.
    """
    data = [(value / 20.0, 0.0) for value in range(21)]
    weights = train(data, 6, 1, epochs=120, seed=2, start_radius=3.0)
    row = [weight[0] for weight in weights[0]]
    increasing = all(a < b for a, b in zip(row, row[1:]))
    decreasing = all(a > b for a, b in zip(row, row[1:]))
    return increasing or decreasing
