"""Division der Relationenalgebra und ihre Rückführung auf Grundoperatoren."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "relational-algebra"))

import relational_algebra as algebra


def divide(dividend, dividend_positions, divisor, divisor_positions):
    """Teilt die Dividendenrelation durch die Divisorrelation.

    Die Stellen des Divisors werden mit den hinteren Stellen des
    Dividenden verglichen; übrig bleiben die Stellen des Dividenden, die
    nicht in ``divisor_positions`` genannt sind.

    Args:
        dividend: Tupel der zu teilenden Relation.
        dividend_positions: alle Stellen des Dividenden.
        divisor: Tupel der teilenden Relation.
        divisor_positions: die Stellen des Dividenden, die dem Divisor
            entsprechen.

    Returns:
        Die Tupel über den restlichen Stellen, die mit jedem Tupel des
        Divisors im Dividenden vorkommen.
    """
    rest = [position for position in dividend_positions
            if position not in divisor_positions]
    required = {tuple(row) for row in divisor}
    candidates = algebra.project(dividend, rest)
    result = []
    for candidate in candidates:
        partners = set()
        for row in dividend:
            if tuple(row[position] for position in rest) == candidate:
                partners.add(tuple(row[position]
                                   for position in divisor_positions))
        if required <= partners:
            result.append(candidate)
    return result


def by_basic_operators(dividend, divisor):
    """Berechnet dieselbe Division über Produkt, Differenz und Projektion.

    Erwartet einen zweistelligen Dividenden und einen einstelligen
    Divisor. Die Formel ist π₁(R) − π₁((π₁(R) × S) − R): abgezogen wird,
    wem eine Kombination fehlt.
    """
    left = algebra.project(dividend, [0])
    all_pairs = algebra.product(left, divisor)
    missing = algebra.difference(all_pairs, dividend)
    incomplete = algebra.project(missing, [0])
    return algebra.difference(left, incomplete)
