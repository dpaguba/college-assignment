"""Linear programming: the optimum is at a vertex, and that is the algorithm.

The feasible region of a linear program is a convex polyhedron and the
objective is linear, so an optimum is always attained at a vertex when one
exists. Enumerating the vertices therefore solves the problem, and the
simplex method is the refinement that walks from vertex to vertex along
improving edges instead of visiting them all.

The tenth sheet's production problem is the running example. Its optimum is
300 units of the first product and 150 of the second, for a profit of 1500,
with the machine hours and the raw material both exhausted.
"""

import itertools
from fractions import Fraction


def solve(objective, constraints):
    """The optimum of a maximisation over the given constraints.

    Solved by enumerating the vertices, which is exact and exponential. For
    the two-variable problems of the lecture that is the right trade: the
    answer is certain and the run time is irrelevant.
    """
    if _is_unbounded(objective, constraints):
        return {"solution": None, "value": None, "binding": [],
                "status": "unbounded"}
    corners = vertices(constraints)
    if corners is None:
        return {"solution": None, "value": None, "binding": []}
    best, best_value = None, None
    for corner in corners:
        value = sum(Fraction(coefficient) * component
                    for coefficient, component in zip(objective, corner))
        if best_value is None or value > best_value:
            best, best_value = corner, value
    if best is None:
        return {"solution": None, "value": None, "binding": []}
    binding = [index for index, (row, bound) in enumerate(constraints)
               if sum(Fraction(coefficient) * component
                      for coefficient, component in zip(row, best)) == bound]
    return {"solution": [_as_number(value) for value in best],
            "value": _as_number(best_value), "binding": binding}


def _is_unbounded(objective, constraints, box=Fraction(10 ** 6)):
    """Whether the objective can grow without limit inside the region.

    Tested by adding a large box and seeing whether the optimum sits on it.
    A vertex enumeration alone cannot tell an unbounded problem from a
    bounded one, because an unbounded region still has vertices.
    """
    dimension = len(objective)
    boxed = list(constraints)
    for index in range(dimension):
        row = [1 if position == index else 0 for position in range(dimension)]
        boxed.append((row, box))
    corners = vertices(boxed)
    if corners is None:
        return False
    best = max(sum(Fraction(coefficient) * component
                   for coefficient, component in zip(objective, corner))
               for corner in corners)
    return best >= box / 2


def _as_number(value):
    """An integer where the fraction is whole, and a float otherwise."""
    if isinstance(value, Fraction) and value.denominator == 1:
        return int(value)
    return float(value) if isinstance(value, Fraction) else value


def vertices(constraints):
    """Every feasible intersection of two constraints, including the axes."""
    rows = [(list(map(Fraction, row)), Fraction(bound))
            for row, bound in constraints]
    dimension = len(rows[0][0])
    rows += [([Fraction(-1 if index == position else 0)
               for position in range(dimension)], Fraction(0))
             for index in range(dimension)]
    found = []
    for first, second in itertools.combinations(range(len(rows)), 2):
        point = _intersect(rows[first], rows[second])
        if point is None:
            continue
        if _feasible(point, rows):
            if point not in found:
                found.append(point)
    if not found:
        return None
    return found


def _intersect(first, second):
    """The intersection of two lines in two dimensions, or nothing."""
    (a1, b1), c1 = (first[0][0], first[0][1]), first[1]
    (a2, b2), c2 = (second[0][0], second[0][1]), second[1]
    determinant = a1 * b2 - a2 * b1
    if determinant == 0:
        return None
    return [(c1 * b2 - c2 * b1) / determinant,
            (a1 * c2 - a2 * c1) / determinant]


def _feasible(point, rows):
    """Whether a point satisfies every constraint."""
    for row, bound in rows:
        if sum(coefficient * component
               for coefficient, component in zip(row, point)) > bound:
            return False
    return True


def best_vertex(objective, constraints):
    """The best vertex, reported with the vertex itself."""
    result = solve(objective, constraints)
    return {"vertex": result["solution"], "value": result["value"]}


def normal_form(objective, constraints):
    """The problem in the normal form the sheet asks for.

    Minimisation, with the maximisation negated, the constraints as a matrix
    and the bounds as a vector. The transformation is mechanical and it is
    the step that lets one solver handle every linear program.
    """
    return {"c": [-value for value in objective],
            "A": [list(row) for row, _bound in constraints],
            "b": [bound for _row, bound in constraints],
            "sense": "min"}
