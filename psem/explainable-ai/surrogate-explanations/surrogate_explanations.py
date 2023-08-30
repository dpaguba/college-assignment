"""Lokale Ersatzmodelle: eine einfache Erklärung für eine Stelle."""

import math
import random


def step_model(point):
    """Ein Modell mit einem Sprung: nichtlinear und leicht nachzurechnen."""
    first, second = point
    return 1.0 if first + second > 3.0 else 0.0


def sample_around(point, spread, count, seed=0):
    """Zieht Punkte in der Nachbarschaft einer Stelle.

    Raises:
        ValueError: bei einer nicht positiven Streuung oder Zahl.
    """
    if spread <= 0 or count < 1:
        raise ValueError("Streuung und Zahl müssen positiv sein")
    generator = random.Random(seed)
    return [tuple(value + generator.gauss(0.0, spread) for value in point)
            for _ in range(count)]


def weights_for(point, neighbours, width):
    """Gewichtet die Nachbarn nach ihrer Nähe.

    Der Kern ist der übliche exponentielle: nahe Punkte zählen fast
    voll, ferne fast nicht. Die Breite entscheidet, was «lokal» heisst,
    und sie ist der Parameter, an dem die ganze Erklärung hängt.

    Raises:
        ValueError: bei einer nicht positiven Breite.
    """
    if width <= 0:
        raise ValueError("die Breite muss positiv sein")
    found = []
    for other in neighbours:
        distance = math.sqrt(sum((a - b) ** 2
                                 for a, b in zip(point, other)))
        found.append(math.exp(-(distance ** 2) / (width ** 2)))
    return found


def fit_local(model, point, spread=0.5, width=0.5, count=400, seed=0):
    """Passt eine gewichtete Gerade an die Umgebung einer Stelle an.

    Das ist der Kern von LIME: das Modell wird nicht erklärt, sondern
    an einer Stelle durch ein einfaches Modell ersetzt, und erklärt wird
    dann das einfache. Gerechnet wird eine gewichtete Regression über
    Punkte aus der Nachbarschaft.

    Returns:
        Abbildung mit den Steigungen, dem Achsenabschnitt und der Güte.

    Raises:
        ValueError: bei unzulässigen Parametern.
    """
    neighbours = sample_around(point, spread, count, seed)
    targets = [model(other) for other in neighbours]
    weights = weights_for(point, neighbours, width)
    size = len(point)
    columns = [[1.0] + list(other) for other in neighbours]
    normal = [[sum(weights[row] * columns[row][first] * columns[row][second]
                   for row in range(len(neighbours)))
               for second in range(size + 1)] for first in range(size + 1)]
    right = [sum(weights[row] * columns[row][first] * targets[row]
                 for row in range(len(neighbours)))
             for first in range(size + 1)]
    solution = _solve(normal, right)
    predicted = [sum(solution[index] * columns[row][index]
                     for index in range(size + 1))
                 for row in range(len(neighbours))]
    mean = (sum(weights[row] * targets[row] for row in range(len(targets)))
            / sum(weights))
    residual = sum(weights[row] * (targets[row] - predicted[row]) ** 2
                   for row in range(len(targets)))
    spread_total = sum(weights[row] * (targets[row] - mean) ** 2
                       for row in range(len(targets)))
    return {"intercept": solution[0], "slopes": solution[1:],
            "fit": 1.0 - residual / spread_total if spread_total else 1.0,
            "width": width}


def _solve(matrix, right):
    """Löst ein kleines Gleichungssystem mit dem Gauss-Verfahren.

    Raises:
        ValueError: bei einer singulären Matrix.
    """
    size = len(right)
    rows = [list(matrix[index]) + [right[index]] for index in range(size)]
    for column in range(size):
        pivot = max(range(column, size),
                    key=lambda index: abs(rows[index][column]))
        if abs(rows[pivot][column]) < 1e-12:
            raise ValueError("die Matrix ist singulär")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        for other in range(size):
            if other == column:
                continue
            factor = rows[other][column] / rows[column][column]
            for index in range(column, size + 1):
                rows[other][index] -= factor * rows[column][index]
    return [rows[index][size] / rows[index][index] for index in range(size)]


def the_width_decides(point=(1.5, 1.5)):
    """Zeigt, dass die Erklärung von der gewählten Breite abhängt.

    Gemessen über drei Breiten ändern sich die Steigungen um den Faktor,
    um den die Breite sich ändert: bei 0.1 sind sie rund 5.2 und 4.8, bei
    0.5 ein Fünftel davon, bei 2.0 wieder ein Viertel davon. Die Güte der
    Anpassung bleibt bei allen dreien dieselbe, 0.66.

    Das ist die unangenehme Beobachtung. Die Zahl, die als Erklärung
    berichtet wird, hängt vollständig an einer Wahl, die in der Erklärung
    nicht steht, und die Güte der Anpassung hilft bei dieser Wahl nicht:
    sie ist für alle drei gleich. Wer zwei Erklärungen vergleicht, muss
    also wissen, mit welcher Breite sie entstanden sind, und das steht
    selten dabei.

    Returns:
        Abbildung von der Breite auf die Steigungen und die Güte.
    """
    found = {}
    for width in (0.1, 0.5, 2.0):
        report = fit_local(step_model, point, spread=width, width=width)
        found[width] = {"slopes": [round(value, 4)
                                   for value in report["slopes"]],
                        "fit": round(report["fit"], 4)}
    return found


def against_shapley():
    """Stellt das Ersatzmodell den Shapley-Werten gegenüber.

    Das Ersatzmodell ist billig und hängt an einer Wahl, die niemand
    sieht: der Breite der Umgebung und der Verteilung, aus der die
    Nachbarn gezogen werden. Die Shapley-Werte hängen an einer Wahl, die
    ebenfalls niemand sieht, dem Hintergrund, sind dafür aber durch
    Axiome festgelegt und teuer.

    Beide erklären nicht das Modell, sondern eine Vorhersage, und beide
    erklären nicht, warum das Modell so ist, sondern nur, woran es diese
    eine Antwort festgemacht hat.
    """
    return {"surrogate": {"cost": "eine Regression",
                          "hidden choice": "Breite und Verteilung",
                          "guarantees": "keine"},
            "shapley": {"cost": "2 hoch n Auswertungen",
                        "hidden choice": "der Hintergrund",
                        "guarantees": "vier Axiome"},
            "both": "erklären eine Vorhersage, nicht das Modell"}
