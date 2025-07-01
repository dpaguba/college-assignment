"""Polynom-Interpolation und die Grenzen der äquidistanten Stützstellen."""

import math


def _check(nodes):
    """Prüft, dass die Stützstellen paarweise verschieden sind.

    Raises:
        ValueError: bei doppelten x-Werten oder leerer Liste.
    """
    if not nodes:
        raise ValueError("keine Stuetzstellen")
    xs = [x for x, _ in nodes]
    if len(set(xs)) != len(xs):
        raise ValueError("Stuetzstellen muessen verschieden sein")


def lagrange(nodes, position):
    """Wertet das Interpolationspolynom in der Form von Lagrange aus.

    Jeder Stützstelle wird ein Basispolynom zugeordnet, das dort eins und
    an allen anderen null ist.

    Raises:
        ValueError: bei doppelten Stützstellen.
    """
    _check(nodes)
    total = 0.0
    for index, (x, y) in enumerate(nodes):
        factor = 1.0
        for other, (other_x, _) in enumerate(nodes):
            if other == index:
                continue
            factor *= (position - other_x) / (x - other_x)
        total += y * factor
    return total


def divided_differences(nodes):
    """Berechnet die Koeffizienten der Newtonschen Form."""
    _check(nodes)
    xs = [x for x, _ in nodes]
    table = [y for _, y in nodes]
    coefficients = [table[0]]
    for level in range(1, len(nodes)):
        for index in range(len(nodes) - level):
            table[index] = ((table[index + 1] - table[index])
                            / (xs[index + level] - xs[index]))
        coefficients.append(table[0])
    return coefficients


def newton(nodes, position):
    """Wertet dasselbe Polynom in der Form von Newton aus.

    Die Form ist rechnerisch günstiger, weil eine neue Stützstelle nur
    einen weiteren Summanden kostet; das Polynom ist dasselbe.
    """
    coefficients = divided_differences(nodes)
    xs = [x for x, _ in nodes]
    total = 0.0
    product = 1.0
    for index, coefficient in enumerate(coefficients):
        total += coefficient * product
        product *= position - xs[index]
    return total


def chebyshev_nodes(count, left, right):
    """Liefert die Tschebyscheff-Stützstellen im gegebenen Intervall.

    Sie liegen dichter am Rand, wo das äquidistante Polynom ausschlägt.

    Raises:
        ValueError: bei weniger als zwei Stützstellen.
    """
    if count < 2:
        raise ValueError("mindestens zwei Stuetzstellen noetig")
    values = []
    for index in range(count):
        angle = math.pi * (2 * index + 1) / (2 * count)
        values.append((left + right) / 2 + (right - left) / 2 * math.cos(angle))
    return sorted(values)


def runge_comparison(count=15):
    """Misst den Fehler beider Stützstellenwahlen an der Runge-Funktion.

    Die Funktion 1/(1 + 25x²) auf [−1, 1] ist das übliche Beispiel: mit
    äquidistanten Stützstellen wächst der Fehler am Rand mit dem Grad,
    mit Tschebyscheff-Stützstellen nicht.

    Returns:
        Abbildung mit dem grössten Fehler beider Wahlen.
    """
    def runge(x):
        """Die Funktion des Beispiels."""
        return 1.0 / (1.0 + 25.0 * x * x)

    equidistant = [(-1.0 + 2.0 * index / (count - 1),
                    runge(-1.0 + 2.0 * index / (count - 1)))
                   for index in range(count)]
    chebyshev = [(x, runge(x)) for x in chebyshev_nodes(count, -1.0, 1.0)]
    worst = {"equidistant": 0.0, "chebyshev": 0.0}
    for step in range(401):
        position = -1.0 + 2.0 * step / 400
        exact = runge(position)
        worst["equidistant"] = max(worst["equidistant"],
                                   abs(lagrange(equidistant, position)
                                       - exact))
        worst["chebyshev"] = max(worst["chebyshev"],
                                 abs(lagrange(chebyshev, position) - exact))
    return worst


def least_squares(nodes, degree):
    """Bestimmt die Ausgleichspolynom-Koeffizienten über die Normalgleichungen.

    Returns:
        Liste der Koeffizienten, beginnend beim konstanten Glied.

    Raises:
        ValueError: wenn der Grad zu hoch für die Zahl der Punkte ist.
    """
    if degree + 1 > len(nodes):
        raise ValueError("Grad ist zu hoch fuer die Punktzahl")
    size = degree + 1
    matrix = [[sum(x ** (row + column) for x, _ in nodes)
               for column in range(size)] for row in range(size)]
    right = [sum(y * x ** row for x, y in nodes) for row in range(size)]
    return _solve(matrix, right)


def _solve(matrix, right):
    """Löst ein lineares Gleichungssystem mit Gauss-Elimination."""
    size = len(matrix)
    rows = [list(matrix[index]) + [right[index]] for index in range(size)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(rows[row][column]))
        if abs(rows[pivot][column]) < 1e-12:
            raise ValueError("System ist singulaer")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        for row in range(size):
            if row == column:
                continue
            factor = rows[row][column] / rows[column][column]
            for position in range(column, size + 1):
                rows[row][position] -= factor * rows[column][position]
    return [rows[index][size] / rows[index][index] for index in range(size)]


def evaluate_polynomial(coefficients, position):
    """Wertet ein Polynom aus, dessen Koeffizienten aufsteigend stehen."""
    return sum(coefficient * position ** power
               for power, coefficient in enumerate(coefficients))


def approximation_versus_interpolation():
    """Stellt Ausgleichsrechnung und Interpolation gegenüber.

    Die Interpolation trifft jeden Punkt genau, die Ausgleichsgerade nicht;
    dafür folgt sie nicht jedem Messfehler.

    Returns:
        Abbildung mit den Residuen beider Wege.
    """
    nodes = [(0.0, 0.1), (1.0, 1.9), (2.0, 3.2), (3.0, 3.9), (4.0, 5.1)]
    line = least_squares(nodes, 1)
    approximation = sum((y - evaluate_polynomial(line, x)) ** 2
                        for x, y in nodes)
    interpolation = sum((y - lagrange(nodes, x)) ** 2 for x, y in nodes)
    return {"approximation residual": approximation,
            "interpolation residual": interpolation}
