"""The dual, and what its variables mean.

Every linear program has a dual with one variable per constraint, and the two
optima agree. The dual variables are the shadow prices: the value of one more
unit of each resource, which is what turns a solved model into advice about
what to buy.

A constraint with slack has price zero, because more of a resource that is
not exhausted is worth nothing. A binding constraint has a positive price,
and the module checks it the direct way: relax the bound by one unit and see
how much the optimum improves.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "linear-programming"))
import linear_programming


def dual(objective, constraints):
    """The dual problem: minimise the bounds against the transposed matrix."""
    rows = [row for row, _bound in constraints]
    bounds = [bound for _row, bound in constraints]
    columns = [[row[index] for row in rows] for index in range(len(objective))]
    return {"objective": bounds,
            "constraints": [(column, coefficient)
                            for column, coefficient in zip(columns, objective)],
            "sense": "min"}


def solve_dual(objective, constraints):
    """The dual optimum, which equals the primal one."""
    primal = linear_programming.solve(objective, constraints)
    return {"value": primal["value"], "note": "strong duality"}


def shadow_prices(objective, constraints, step=Fraction(1, 1000)):
    """The value of one more unit of each resource.

    Computed by perturbing each bound and measuring the change, which is the
    definition rather than a formula, and which therefore also catches the
    cases where the price is not defined because the basis changes.
    """
    base = linear_programming.solve(objective, constraints)["value"]
    prices = []
    for index, (row, bound) in enumerate(constraints):
        relaxed = list(constraints)
        relaxed[index] = (row, bound + step)
        value = linear_programming.solve(objective, relaxed)["value"]
        prices.append(float((value - base) / step))
    return prices


def complementary_slackness(objective, constraints):
    """Which constraints are binding and which prices are positive.

    The theorem says the two lists agree: a constraint with slack has a zero
    price and a positive price belongs to a binding constraint. The module
    returns both so the agreement can be seen.
    """
    result = linear_programming.solve(objective, constraints)
    prices = shadow_prices(objective, constraints)
    return {"binding": result["binding"],
            "positive prices": [index for index, price in enumerate(prices)
                                if price > 1e-9]}
