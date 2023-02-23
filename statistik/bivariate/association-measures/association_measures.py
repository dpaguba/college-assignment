"""Measures of association for categorical data.

The chi-square statistic adds the squared deviations from independence,
weighted by what independence predicted. It grows with the sample size, so it
is not comparable across studies, and the coefficients derived from it are
attempts to remove that dependence: Pearson's C is bounded but its maximum
depends on the table shape, the corrected version divides that maximum out,
and Cramer's V does the same thing differently.

For the pizza data the published solution gives 33.191 and a corrected
coefficient of 0.366.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "contingency-tables"))
import contingency_tables


def chi_square(table, digits=None):
    """The sum of squared deviations from the expected counts.

    With ``digits`` the expected counts and each term are rounded as the
    published solution rounds them. Exact arithmetic gives 33.1924 for the
    pizza data and the rounded path gives the published 33.191, which is the
    size of the error that intermediate rounding introduces.
    """
    predicted = contingency_tables.expected(table)
    total = 0.0
    for name, row in table.items():
        for index, observed in enumerate(row):
            value = predicted[name][index]
            if digits is not None:
                value = round(value, 2)
            if value:
                term = (observed - value) ** 2 / value
                total += round(term, digits) if digits is not None else term
    return round(total, digits) if digits is not None else total


def chi_square_alternative(table):
    """The same statistic through the identity the third sheet asks to prove.

    Expanding the square gives a sum of squared counts over expected counts,
    minus the sample size. The two forms are algebraically equal, and
    computing both is the check that the algebra was done correctly.
    """
    predicted = contingency_tables.expected(table)
    size = contingency_tables.margins(table)["total"]
    total = 0.0
    for name, row in table.items():
        for index, observed in enumerate(row):
            value = predicted[name][index]
            if value:
                total += observed ** 2 / value
    return total - size


def pearson_c(table):
    """Pearson's contingency coefficient."""
    size = contingency_tables.margins(table)["total"]
    statistic = chi_square(table)
    return math.sqrt(statistic / (statistic + size))


def corrected_pearson(table, digits=None):
    """Pearson's coefficient divided by the largest value it can take.

    The maximum depends on the smaller of the two dimensions, so without the
    correction two tables of different shapes cannot be compared. With it the
    scale is the unit interval for every table.
    """
    smaller = min(len(table), len(next(iter(table.values()))))
    if digits is None:
        return pearson_c(table) * math.sqrt(smaller / (smaller - 1))
    size = contingency_tables.margins(table)["total"]
    statistic = chi_square(table, digits)
    inner = round(statistic / (statistic + size), 3)
    return round(math.sqrt(round(inner * smaller / (smaller - 1), 3)), 3)


def cramers_v(table):
    """Cramer's V, the other normalisation of the same statistic."""
    size = contingency_tables.margins(table)["total"]
    smaller = min(len(table), len(next(iter(table.values()))))
    return math.sqrt(chi_square(table) / (size * (smaller - 1)))
