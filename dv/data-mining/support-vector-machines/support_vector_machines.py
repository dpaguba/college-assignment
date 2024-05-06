"""Stützvektormaschinen: der breiteste Streifen zwischen zwei Klassen."""

import itertools
import math


def _dot(first, second):
    """Skalarprodukt zweier Vektoren."""
    return sum(a * b for a, b in zip(first, second))


def fit(samples, soft=True, penalty=1e6, rounds=2000, tolerance=1e-9):
    """Lernt eine trennende Hyperebene über das duale Problem.

    Gelöst wird mit paarweiser Koordinatenaufstiegs-Optimierung: zwei
    Multiplikatoren werden zugleich verändert, damit die Nebenbedingung
    Σ αᵢ yᵢ = 0 erhalten bleibt.

    Args:
        samples: Paare (Punkt, Klasse) mit Klassen +1 und −1.
        soft: lässt Verletzungen der Randbedingung zu.
        penalty: obere Schranke der Multiplikatoren.
        rounds: obere Schranke der Durchläufe.
        tolerance: Schranke, ab der eine Änderung als null gilt.

    Returns:
        Abbildung mit ``weights``, ``bias``, ``alphas`` und ``samples``.

    Raises:
        ValueError: wenn die Klassen ohne Schlupf nicht zu trennen sind.
    """
    points = [tuple(float(value) for value in point) for point, _ in samples]
    labels = [1 if label > 0 else -1 for _, label in samples]
    bound = penalty if soft else 1e9
    alphas = [0.0] * len(points)
    gram = [[_dot(first, second) for second in points] for first in points]
    for _ in range(rounds):
        changed = False
        for first in range(len(points)):
            for second in range(len(points)):
                if first == second or labels[first] == labels[second]:
                    continue
                step = gram[first][first] + gram[second][second] \
                    - 2 * gram[first][second]
                if step <= tolerance:
                    continue
                gradient = 1 - sum(alphas[index] * labels[index]
                                   * labels[first] * gram[index][first]
                                   for index in range(len(points)))
                other = 1 - sum(alphas[index] * labels[index]
                                * labels[second] * gram[index][second]
                                for index in range(len(points)))
                delta = (gradient + other) / step
                delta = max(-min(alphas[first], alphas[second]),
                            min(delta, bound - max(alphas[first],
                                                   alphas[second])))
                if abs(delta) < tolerance:
                    continue
                alphas[first] += delta
                alphas[second] += delta
                changed = True
        if not changed:
            break
    dimension = len(points[0])
    weights = [sum(alphas[index] * labels[index] * points[index][axis]
                   for index in range(len(points)))
               for axis in range(dimension)]
    support = [index for index in range(len(points))
               if alphas[index] > tolerance * 1e3]
    if not support:
        raise ValueError("keine trennende Ebene gefunden")
    bias = sum(labels[index] - _dot(weights, points[index])
               for index in support) / len(support)
    model = {"weights": weights, "bias": bias, "alphas": alphas,
             "points": points, "labels": labels}
    if not soft:
        for point, label in zip(points, labels):
            if label * (_dot(weights, point) + bias) < 1 - 1e-6:
                raise ValueError("Klassen sind nicht trennbar")
    return model


def predict(model, point):
    """Ordnet einen Punkt einer der beiden Klassen zu."""
    value = _dot(model["weights"], point) + model["bias"]
    return 1 if value >= 0 else -1


def margin(model):
    """Abstand der Hyperebene zum nächstgelegenen Punkt."""
    length = math.sqrt(sum(value * value for value in model["weights"]))
    if length == 0:
        raise ValueError("entartete Ebene")
    return 1.0 / length


def support_vectors(model, tolerance=1e-6):
    """Nennt die Punkte, die den Rand berühren."""
    return [point for point, alpha in zip(model["points"], model["alphas"])
            if alpha > tolerance]


def widest_margin_by_search(samples, directions=7200):
    """Sucht den breitesten trennenden Streifen durch Richtungsabtastung.

    Für jede Richtung werden beide Klassen darauf projiziert; die Hälfte
    des Abstands zwischen den beiden Projektionsbereichen ist der
    erreichbare Rand. Das Verfahren benutzt weder das duale Problem noch
    Ableitungen und ist damit vom Lernverfahren unabhängig.

    Returns:
        Der grösste erreichbare Rand.
    """
    best = 0.0
    for step in range(directions):
        angle = math.pi * step / directions
        direction = (math.cos(angle), math.sin(angle))
        positive = [_dot(direction, point) for point, label in samples
                    if label > 0]
        negative = [_dot(direction, point) for point, label in samples
                    if label <= 0]
        if not positive or not negative:
            continue
        gap = max(min(positive) - max(negative),
                  min(negative) - max(positive))
        best = max(best, gap / 2)
    return best


def far_point_is_irrelevant():
    """Prüft, dass ein weit entfernter Punkt die Ebene nicht verschiebt.

    Nur die Punkte am Rand bestimmen die Lösung; das ist der Grund für den
    Namen Stützvektor.

    Returns:
        Abbildung mit der Änderung der Normalenrichtung.
    """
    base = [((2.0, 2.0), 1), ((2.0, 3.0), 1), ((0.0, 0.0), -1),
            ((1.0, 0.0), -1)]
    extended = base + [((0.0, -50.0), -1)]
    first = fit(base)
    second = fit(extended)
    def normalise(model):
        """Bringt den Normalenvektor auf die Länge eins."""
        length = math.sqrt(sum(value ** 2 for value in model["weights"]))
        return [value / length for value in model["weights"]]
    a = normalise(first)
    b = normalise(second)
    return {"change": max(abs(x - y) for x, y in zip(a, b)),
            "support before": len(support_vectors(first)),
            "support after": len(support_vectors(second))}


def hull_distance(first, second, rounds=20000):
    """Kleinster Abstand zwischen den konvexen Hüllen zweier Punktmengen.

    Gerechnet wird mit dem Verfahren von Frank und Wolfe auf der
    Differenzmenge: gesucht ist der Punkt kleinster Norm in
    conv(first) − conv(second). Ist er der Ursprung, überschneiden sich
    die Hüllen.

    Returns:
        Der Abstand; null bedeutet Überschneidung.
    """
    dimension = len(first[0])
    current = tuple(a - b for a, b in zip(first[0], second[0]))
    for step in range(rounds):
        best_first = min(first, key=lambda point: _dot(current, point))
        best_second = max(second, key=lambda point: _dot(current, point))
        vertex = tuple(a - b for a, b in zip(best_first, best_second))
        direction = tuple(vertex[axis] - current[axis]
                          for axis in range(dimension))
        squared = sum(value * value for value in direction)
        if squared < 1e-24:
            break
        gamma = -_dot(current, direction) / squared
        gamma = max(0.0, min(1.0, gamma))
        if gamma == 0.0:
            break
        current = tuple(current[axis] + gamma * direction[axis]
                        for axis in range(dimension))
    return math.sqrt(sum(value * value for value in current))


def linearly_separable(samples, tolerance=1e-6):
    """Prüft die Trennbarkeit über die konvexen Hüllen beider Klassen.

    Zwei Klassen sind genau dann durch eine Hyperebene zu trennen, wenn
    ihre konvexen Hüllen sich nicht schneiden. Der Abstand der Hüllen wird
    unabhängig vom Lernverfahren bestimmt und gilt in jeder Dimension.
    """
    positive = [tuple(float(value) for value in point)
                for point, label in samples if label > 0]
    negative = [tuple(float(value) for value in point)
                for point, label in samples if label <= 0]
    if not positive or not negative:
        return True
    return hull_distance(positive, negative) > tolerance


def quadratic_features(point):
    """Bildet einen Punkt in den Raum der quadratischen Merkmale ab."""
    x, y = point
    return (x, y, x * x, y * y, x * y)


def kernel_example():
    """Zeigt Daten, die erst nach der Abbildung trennbar sind.

    Die vier Punkte des exklusiven Oder lassen sich durch keine Gerade
    trennen; im Raum der quadratischen Merkmale genügt eine Ebene.

    Returns:
        Abbildung mit beiden Antworten.
    """
    samples = [((0.0, 0.0), 1), ((1.0, 1.0), 1), ((0.0, 1.0), -1),
               ((1.0, 0.0), -1)]
    lifted = [(quadratic_features(point), label) for point, label in samples]
    return {"linear separable": linearly_separable(samples),
            "quadratic separable": linearly_separable(lifted)}


def slack_meaning():
    """Beschreibt, wozu die Schlupfvariablen dienen."""
    return {"slack": "allows a point to sit inside the margin or beyond it",
            "penalty": "how much such a point costs in the objective",
            "large penalty": "narrow margin, few violations",
            "small penalty": "wide margin, more violations"}
