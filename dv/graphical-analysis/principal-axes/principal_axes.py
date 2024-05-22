"""Hauptachsentransformation über das charakteristische Polynom."""

import math


def mean(points):
    """Berechnet den Schwerpunkt einer Punktmenge.

    Raises:
        ValueError: bei einer leeren Punktmenge.
    """
    if not points:
        raise ValueError("keine Punkte")
    dimension = len(points[0])
    return tuple(sum(point[axis] for point in points) / len(points)
                 for axis in range(dimension))


def centred(points):
    """Verschiebt die Punkte so, dass ihr Schwerpunkt im Ursprung liegt."""
    centre = mean(points)
    return [tuple(value - offset for value, offset in zip(point, centre))
            for point in points]


def covariance(points):
    """Berechnet die Kovarianzmatrix mit dem Nenner n − 1.

    Der Nenner n − 1 ist die erwartungstreue Schätzung und stimmt mit dem
    überein, was `cov` in R und `numpy.cov` liefern.

    Raises:
        ValueError: bei weniger als zwei Punkten.
    """
    if len(points) < 2:
        raise ValueError("mindestens zwei Punkte noetig")
    data = centred(points)
    dimension = len(points[0])
    divisor = len(points) - 1
    return [[sum(row[i] * row[j] for row in data) / divisor
             for j in range(dimension)] for i in range(dimension)]


def characteristic_polynomial(matrix):
    """Liefert die Koeffizienten des charakteristischen Polynoms einer 2×2-Matrix.

    Das Polynom lautet λ² − (Spur) λ + (Determinante).

    Returns:
        Tripel (1, −Spur, Determinante).

    Raises:
        ValueError: wenn die Matrix nicht zweireihig ist.
    """
    if len(matrix) != 2 or len(matrix[0]) != 2:
        raise ValueError("nur fuer 2x2-Matrizen")
    trace = matrix[0][0] + matrix[1][1]
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return (1.0, -trace, determinant)


def eigenvalues(matrix):
    """Bestimmt die Eigenwerte als Nullstellen des charakteristischen Polynoms.

    Returns:
        Liste der Eigenwerte, absteigend sortiert.

    Raises:
        ValueError: wenn die Diskriminante negativ ist, die Matrix also
            nicht symmetrisch ist.
    """
    _, linear, constant = characteristic_polynomial(matrix)
    discriminant = linear * linear - 4 * constant
    if discriminant < -1e-12:
        raise ValueError("komplexe Eigenwerte")
    root = math.sqrt(max(discriminant, 0.0))
    return sorted([(-linear + root) / 2, (-linear - root) / 2], reverse=True)


def eigenvectors(matrix):
    """Bestimmt die normierten Eigenvektoren einer symmetrischen 2×2-Matrix.

    Returns:
        Liste der Eigenvektoren in der Reihenfolge der Eigenwerte.
    """
    result = []
    for value in eigenvalues(matrix):
        a = matrix[0][0] - value
        b = matrix[0][1]
        if abs(b) > 1e-12:
            vector = (b, -a)
        else:
            c = matrix[1][0]
            d = matrix[1][1] - value
            vector = (-d, c) if abs(c) > 1e-12 or abs(d) > 1e-12 else (1.0, 0.0)
        length = math.hypot(*vector)
        if length < 1e-12:
            vector = (1.0, 0.0)
            length = 1.0
        result.append((vector[0] / length, vector[1] / length))
    return result


def explained_variance(points):
    """Gibt den Anteil der Gesamtvarianz je Hauptachse an.

    Returns:
        Liste der Anteile, absteigend, mit Summe eins.
    """
    values = eigenvalues(covariance(points))
    total = sum(values)
    if total == 0:
        raise ValueError("Punktmenge hat keine Varianz")
    return [value / total for value in values]


def transform(points):
    """Projiziert die zentrierten Punkte auf die Hauptachsen."""
    axes = eigenvectors(covariance(points))
    return [tuple(sum(value * component
                      for value, component in zip(point, axis))
                  for axis in axes) for point in centred(points)]


def reduce_to(points, dimensions):
    """Behält nur die ersten Hauptachsen.

    Raises:
        ValueError: wenn mehr Achsen verlangt werden als vorhanden.
    """
    transformed = transform(points)
    if dimensions > len(transformed[0]):
        raise ValueError("so viele Achsen gibt es nicht")
    return [row[:dimensions] for row in transformed]


def exercise_points():
    """Liefert die vier Punkte der ersten Übungsaufgabe."""
    return [(0, 1), (1, 1), (2, 1), (3, 2)]
