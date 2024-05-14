"""Lateinische Quadratpläne für Versuche mit mehreren Faktoren."""

import itertools


def cyclic(order):
    """Baut ein lateinisches Quadrat durch zyklisches Verschieben.

    Raises:
        ValueError: bei einer Ordnung kleiner als eins.
    """
    if order < 1:
        raise ValueError("Ordnung muss positiv sein")
    return [[(row + column) % order for column in range(order)]
            for row in range(order)]


def is_latin(square):
    """Prüft, ob jedes Symbol in jeder Zeile und Spalte genau einmal steht."""
    order = len(square)
    if any(len(row) != order for row in square):
        return False
    symbols = set(square[0])
    if len(symbols) != order:
        return False
    for row in square:
        if set(row) != symbols:
            return False
    for column in zip(*square):
        if set(column) != symbols:
            return False
    return True


def count(order):
    """Zählt alle lateinischen Quadrate einer Ordnung durch Aufzählung.

    Aufgezählt werden alle Belegungen zeilenweise; die Zahl wächst so
    schnell, dass jenseits der Ordnung fünf nichts mehr zu holen ist.

    Raises:
        ValueError: bei einer Ordnung über fünf.
    """
    if order > 5:
        raise ValueError("zu gross fuer die Aufzaehlung")
    symbols = list(range(order))
    total = 0

    def extend(rows):
        """Setzt eine weitere Zeile auf die bisherigen."""
        nonlocal total
        if len(rows) == order:
            total += 1
            return
        for candidate in itertools.permutations(symbols):
            if all(candidate[column] != row[column]
                   for row in rows for column in range(order)):
                extend(rows + [list(candidate)])

    extend([])
    return total


def reduced_count(order):
    """Zählt die reduzierten Quadrate, deren erste Zeile und Spalte geordnet sind.

    Die Gesamtzahl ergibt sich daraus als n! · (n − 1)! mal dieser Zahl.
    """
    if order > 5:
        raise ValueError("zu gross fuer die Aufzaehlung")
    factorial = 1
    for value in range(1, order + 1):
        factorial *= value
    smaller = 1
    for value in range(1, order):
        smaller *= value
    return count(order) // (factorial * smaller)


def concentration_plan():
    """Stellt den Plan der Übung auf: Schlaf, Kaffee und Sport.

    Drei Faktoren mit je drei Stufen ergäben 27 Versuchsgruppen; ein
    lateinisches Quadrat kommt mit neun aus, indem der dritte Faktor als
    Symbol in das Quadrat aus den ersten beiden eingetragen wird.

    Returns:
        Liste der neun Versuchsgruppen als Tripel (Schlaf, Kaffee, Sport).
    """
    sleep = ["8 hours", "4 hours", "none"]
    coffee = ["3 cups", "1 cup", "none"]
    sport = ["guided", "run", "none"]
    square = cyclic(3)
    plan = []
    for row in range(3):
        for column in range(3):
            plan.append((sleep[row], coffee[column], sport[square[row][column]]))
    return plan


def covers_all_pairs(plan):
    """Prüft, dass jedes Paar zweier Faktorstufen genau einmal vorkommt."""
    for first, second in itertools.combinations(range(3), 2):
        seen = {}
        for run in plan:
            key = (run[first], run[second])
            seen[key] = seen.get(key, 0) + 1
        if len(seen) != 9 or any(value != 1 for value in seen.values()):
            return False
    return True


def saving():
    """Vergleicht den Umfang beider Pläne.

    Returns:
        Abbildung mit der Zahl der Versuche im lateinischen Quadrat und im
        vollfaktoriellen Plan.
    """
    return {"latin square": 9, "full factorial": 27, "factors": 3,
            "levels": 3}


def can_estimate_interactions():
    """Sagt, ob sich aus dem Plan Wechselwirkungen schätzen lassen.

    Jede Kombination zweier Faktoren kommt genau einmal vor, deshalb lässt
    sich der Effekt einer Kombination nicht vom Haupteffekt trennen: der
    Plan setzt voraus, dass keine Wechselwirkungen bestehen.
    """
    return False


def graeco_latin(order):
    """Baut ein griechisch-lateinisches Quadrat für einen vierten Faktor.

    Zwei lateinische Quadrate heissen orthogonal, wenn jedes Symbolpaar
    genau einmal vorkommt; damit lässt sich ein weiterer Faktor
    unterbringen.

    Raises:
        ValueError: für die Ordnung zwei, für die es keines gibt.
    """
    if order == 2:
        raise ValueError("fuer die Ordnung zwei gibt es keines")
    first = cyclic(order)
    second = [[(row + 2 * column) % order for column in range(order)]
              for row in range(order)]
    pairs = {(first[row][column], second[row][column])
             for row in range(order) for column in range(order)}
    if len(pairs) != order * order:
        raise ValueError("die beiden Quadrate sind nicht orthogonal")
    return first, second
