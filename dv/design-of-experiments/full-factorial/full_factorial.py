"""Vollfaktorielle Versuchspläne im 2^k-Design."""

import itertools


def design(factors):
    """Baut die Planmatrix mit allen Vorzeichenkombinationen.

    Die Versuche stehen in der Standardreihenfolge nach Yates: die erste
    Spalte wechselt in jeder Zeile das Vorzeichen, die zweite alle zwei
    Zeilen und so fort.

    Args:
        factors: Zahl der Faktoren.

    Returns:
        Liste der Versuche, jeder als Tupel aus −1 und +1.

    Raises:
        ValueError: bei einer nicht positiven Faktorzahl.
    """
    if factors < 1:
        raise ValueError("mindestens ein Faktor noetig")
    return [tuple(-1 if bit == 0 else 1 for bit in reversed(combination))
            for combination in itertools.product((0, 1), repeat=factors)]


def is_orthogonal(matrix):
    """Prüft, ob je zwei Spalten das Skalarprodukt null haben.

    Orthogonale Spalten bedeuten, dass sich die Effekte unabhängig
    voneinander schätzen lassen.
    """
    columns = list(zip(*matrix))
    for first, second in itertools.combinations(columns, 2):
        if sum(a * b for a, b in zip(first, second)) != 0:
            return False
    return True


def interaction_column(matrix, factors):
    """Bildet die Spalte einer Wechselwirkung als Produkt ihrer Faktoren."""
    column = []
    for row in matrix:
        value = 1
        for index in factors:
            value *= row[index]
        column.append(value)
    return column


def main_effect(matrix, responses, factor):
    """Schätzt den Haupteffekt eines Faktors.

    Der Effekt ist die Differenz der beiden Mittelwerte: alle Versuche mit
    der oberen Stufe gegen alle mit der unteren.

    Raises:
        ValueError: wenn die Zahl der Antworten nicht zum Plan passt.
    """
    if len(matrix) != len(responses):
        raise ValueError("Antworten passen nicht zum Plan")
    high = [value for row, value in zip(matrix, responses)
            if row[factor] > 0]
    low = [value for row, value in zip(matrix, responses) if row[factor] < 0]
    return sum(high) / len(high) - sum(low) / len(low)


def interaction_effect(matrix, responses, factors):
    """Schätzt den Effekt einer Wechselwirkung."""
    column = interaction_column(matrix, factors)
    high = [value for sign, value in zip(column, responses) if sign > 0]
    low = [value for sign, value in zip(column, responses) if sign < 0]
    return sum(high) / len(high) - sum(low) / len(low)


def all_effects(matrix, responses):
    """Schätzt alle Haupt- und Wechselwirkungseffekte.

    Returns:
        Abbildung von der Faktormenge auf ihren Effekt.
    """
    factors = len(matrix[0])
    effects = {}
    for size in range(1, factors + 1):
        for combination in itertools.combinations(range(factors), size):
            effects[combination] = interaction_effect(matrix, responses,
                                                      combination)
    return effects


def matches_regression():
    """Vergleicht die Effektschätzung mit einer Regression nach numpy.

    Die Koeffizienten der Regression auf die Vorzeichenspalten sind genau
    die halben Effekte; das ist der Zusammenhang, den die Vorlesung als
    Regressionsfunktion aufschreibt.
    """
    import numpy

    matrix = design(3)
    responses = [12.0, 18.0, 15.0, 27.0, 13.0, 22.0, 16.0, 34.0]
    columns = [[1.0] * len(matrix)]
    names = []
    for size in range(1, 4):
        for combination in itertools.combinations(range(3), size):
            columns.append([float(value) for value in
                            interaction_column(matrix, combination)])
            names.append(combination)
    model = numpy.array(columns).T
    coefficients, *_ = numpy.linalg.lstsq(model,
                                          numpy.array(responses), rcond=None)
    effects = all_effects(matrix, responses)
    for index, name in enumerate(names, start=1):
        if abs(2 * coefficients[index] - effects[name]) > 1e-9:
            return False
    return True


def clinic_example():
    """Stellt den Plan der Aufgabe 6.3 auf: Operation, Diagnose, Klinik.

    Returns:
        Abbildung mit der Zahl der Versuche, den Faktoren und dem Plan als
        lesbare Kombinationen.
    """
    factors = ["operation", "diagnosis", "clinic"]
    levels = {"operation": ("A", "B"), "diagnosis": ("X", "Y"),
              "clinic": ("1", "2")}
    matrix = design(3)
    runs = []
    for row in matrix:
        runs.append(tuple(levels[name][0] if sign < 0 else levels[name][1]
                          for name, sign in zip(factors, row)))
    return {"runs": len(matrix), "factors": factors, "plan": runs,
            "matrix": matrix}


def full_reduction():
    """Beschreibt, was bei vollständiger Reduzierung geschieht.

    Wird ein 2^k-Plan bis auf einen Versuch je Faktorstufe verkleinert,
    fallen Haupteffekte mit Wechselwirkungen zusammen und lassen sich
    nicht mehr trennen.
    """
    return {"main effects": "confounded with interactions",
            "reason": "there are more effects than runs"}
