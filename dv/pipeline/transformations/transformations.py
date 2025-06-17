"""Homogene Transformationen der zweidimensionalen Bilderzeugung."""

import math


def identity():
    """Liefert die Einheitsmatrix in homogenen Koordinaten."""
    return [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


def translation(dx, dy):
    """Liefert die Verschiebung um (dx, dy).

    In homogenen Koordinaten wird die Verschiebung zur Matrix; das ist der
    Grund, aus dem die dritte Zeile überhaupt mitgeführt wird.
    """
    return [[1.0, 0.0, float(dx)], [0.0, 1.0, float(dy)], [0.0, 0.0, 1.0]]


def scaling(sx, sy):
    """Liefert die Skalierung um die Faktoren sx und sy."""
    return [[float(sx), 0.0, 0.0], [0.0, float(sy), 0.0], [0.0, 0.0, 1.0]]


def rotation(angle):
    """Liefert die Drehung um den Ursprung im Bogenmass."""
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return [[cosine, -sine, 0.0], [sine, cosine, 0.0], [0.0, 0.0, 1.0]]


def shear(shx, shy):
    """Liefert die Scherung mit den Faktoren shx und shy."""
    return [[1.0, float(shx), 0.0], [float(shy), 1.0, 0.0], [0.0, 0.0, 1.0]]


def perspective(distance):
    """Liefert eine Zentralprojektion mit dem genannten Augabstand.

    Raises:
        ValueError: bei einem Abstand von null oder weniger.
    """
    if distance <= 0:
        raise ValueError("Augabstand muss positiv sein")
    return [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0 / distance]]


def compose(first, second):
    """Multipliziert zwei Matrizen, erst ``second``, dann ``first``."""
    return [[sum(first[row][index] * second[index][column]
                 for index in range(3))
             for column in range(3)] for row in range(3)]


def apply(matrix, point, depth=1.0):
    """Wendet eine Matrix auf einen Punkt an und teilt durch die Gewichtung.

    Args:
        matrix: Transformationsmatrix.
        point: Punkt als Paar.
        depth: homogene Koordinate, bei einer Zentralprojektion die Tiefe.

    Returns:
        Der abgebildete Punkt als Paar.

    Raises:
        ZeroDivisionError: wenn die Gewichtung null wird, der Punkt also im
            Fluchtpunkt liegt.
    """
    x, y = point
    values = [matrix[row][0] * x + matrix[row][1] * y + matrix[row][2] * depth
              for row in range(3)]
    if values[2] == 0:
        raise ZeroDivisionError("Punkt liegt in der Fluchtebene")
    return values[0] / values[2], values[1] / values[2]


def is_affine(matrix):
    """Sagt, ob eine Matrix affin ist, die letzte Zeile also (0, 0, 1) lautet.

    Eine affine Abbildung erhält Parallelität; eine Zentralprojektion tut
    das nicht, und genau daran ist sie in der Matrix zu erkennen.
    """
    return (abs(matrix[2][0]) < 1e-12 and abs(matrix[2][1]) < 1e-12
            and abs(matrix[2][2] - 1.0) < 1e-12)


def inverse_of_rotation(angle):
    """Liefert die Umkehrung einer Drehung, die Drehung um den Gegenwinkel."""
    return rotation(-angle)
