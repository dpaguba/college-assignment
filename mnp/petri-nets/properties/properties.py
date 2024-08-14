"""Liveness, boundedness, safety, and place invariants.

The first three are read off the reachability graph. The fourth is computed
from the incidence matrix by linear algebra, and it proves a bound for every
reachable marking at once, including the ones nobody enumerated. That is the
reason the course teaches invariants alongside the graph.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "net-structure"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "reachability"))
import net_structure as nets
import reachability as reach


def deadlocks(net, limit=20000):
    """Reachable markings in which no transition is enabled."""
    result = []
    for node in sorted(reach.reachable(net, limit), key=lambda item: sorted(item)):
        state = net.with_marking(dict(node))
        if not state.enabled_transitions():
            result.append(node)
    return result


def is_live(net, limit=20000):
    """Liveness: from every reachable marking, every transition is still possible."""
    structure = reach.graph(net, limit)
    for node in structure["nodes"]:
        state = net.with_marking(dict(node))
        forward = reach.reachable(state, limit)
        available = set()
        for marking in forward:
            available.update(net.with_marking(dict(marking)).enabled_transitions())
        if set(net.transitions) - available:
            return False
    return True


def is_bounded(net, limit=200):
    """Boundedness, tested by exploring up to a limit of markings."""
    try:
        reach.reachable(net, limit)
    except ValueError:
        return False
    return True


def bound(net, limit=20000):
    """The largest token count any single place ever holds."""
    largest = 0
    for node in reach.reachable(net, limit):
        for _, count in node:
            largest = max(largest, count)
    return largest


def is_safe(net, limit=20000):
    """One-boundedness, which makes the net a condition/event net."""
    return is_bounded(net, limit) and bound(net, limit) <= 1


def incidence_matrix(net):
    """The incidence matrix, one row per place and one column per transition."""
    return [[net.weight(transition, place) - net.weight(place, transition)
             for transition in net.transitions] for place in net.places]


def place_invariants(net):
    """A basis of the solutions of x*C = 0, computed over the rationals.

    Each solution is a weighting of places whose weighted token count is
    unchanged by every firing. Scaling the basis back to integers keeps the
    vectors readable, and a vector that came out entirely negative is flipped,
    since a weighting and its negation express the same invariant.
    """
    matrix = [[Fraction(value) for value in row] for row in incidence_matrix(net)]
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    augmented = [row + [Fraction(1 if index == position else 0)
                        for position in range(rows)]
                 for index, row in enumerate(matrix)]
    pivot_row = 0
    for column in range(columns):
        pivot = next((index for index in range(pivot_row, rows)
                      if augmented[index][column] != 0), None)
        if pivot is None:
            continue
        augmented[pivot_row], augmented[pivot] = augmented[pivot], augmented[pivot_row]
        divisor = augmented[pivot_row][column]
        augmented[pivot_row] = [value / divisor for value in augmented[pivot_row]]
        for index in range(rows):
            if index != pivot_row and augmented[index][column] != 0:
                factor = augmented[index][column]
                augmented[index] = [value - factor * other for value, other
                                    in zip(augmented[index], augmented[pivot_row])]
        pivot_row += 1
    invariants = []
    for row in augmented[pivot_row:]:
        coefficients = row[columns:]
        denominators = [value.denominator for value in coefficients if value]
        scale = 1
        for denominator in denominators:
            scale = scale * denominator // _gcd(scale, denominator)
        vector = {place: int(value * scale) for place, value
                  in zip(net.places, coefficients) if value}
        if vector:
            if all(value < 0 for value in vector.values()):
                vector = {place: -value for place, value in vector.items()}
            invariants.append(vector)
    return invariants


def _gcd(first, second):
    """The greatest common divisor, used to scale invariants to integers."""
    while second:
        first, second = second, first % second
    return first


def invariant_value(net, vector, marking=None):
    """The value of an invariant in a marking."""
    marking = net.marking if marking is None else marking
    return sum(weight * marking.get(place, 0) for place, weight in vector.items())


def bounded_by_invariant(net):
    """Whether a positive invariant covers every place, which bounds the net."""
    for vector in place_invariants(net):
        if all(weight > 0 for weight in vector.values()) and \
                set(vector) == set(net.places):
            return True
    return False
