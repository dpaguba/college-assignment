"""Contingency tables, margins, and the two conditional distributions.

A table of counts answers three different questions depending on what it is
divided by. Dividing by the total gives the joint distribution, dividing by a
row total gives the distribution of the column variable given that row, and
dividing by a column total gives the other conditional distribution. The
third sheet computes all three for the pizza data, and the numbers differ
enough that using the wrong one is a visible error.
"""


def margins(table):
    """The row sums, the column sums and the total."""
    rows = {name: sum(row) for name, row in table.items()}
    width = len(next(iter(table.values())))
    columns = [sum(row[index] for row in table.values()) for index in range(width)]
    return {"rows": rows, "columns": columns, "total": sum(rows.values())}


def relative(table, digits=None):
    """The joint distribution: every count divided by the total."""
    size = margins(table)["total"]
    return {name: [round(value / size, digits) if digits is not None
                   else value / size for value in row]
            for name, row in table.items()}


def conditional_on_rows(table, digits=None):
    """The distribution of the columns within each row.

    With ``digits`` the joint distribution and the margins are rounded
    first, which is what the published solution does when it divides the
    rounded relative frequencies by the rounded row total. The two paths
    differ in the third decimal, and reproducing the published numbers needs
    the rounding to happen in exactly the same places.
    """
    if digits is None:
        return {name: [value / sum(row) for value in row]
                for name, row in table.items()}
    source = relative(table, digits)
    summary = margins(table)
    size = summary["total"]
    return {name: [value / round(summary["rows"][name] / size, digits)
                   for value in row]
            for name, row in source.items()}


def conditional_on_columns(table, digits=None):
    """The distribution of the rows within each column."""
    summary = margins(table)
    if digits is None:
        totals = summary["columns"]
        return {name: [value / totals[index] if totals[index] else 0.0
                       for index, value in enumerate(row)]
                for name, row in table.items()}
    source = relative(table, digits)
    size = summary["total"]
    totals = [round(column / size, digits) for column in summary["columns"]]
    return {name: [value / totals[index] if totals[index] else 0.0
                   for index, value in enumerate(row)]
            for name, row in source.items()}


def expected(table):
    """The counts that independence would predict.

    Row total times column total over the grand total, which is the joint
    distribution one gets by multiplying the two marginal distributions. The
    difference between these and the observed counts is what every measure of
    association reads.
    """
    summary = margins(table)
    size = summary["total"]
    return {name: [summary["rows"][name] * column / size
                   for column in summary["columns"]]
            for name in table}


def is_independent(table, tolerance=1e-9):
    """Whether the observed counts equal the expected ones."""
    predicted = expected(table)
    return all(abs(observed - predicted[name][index]) < tolerance
               for name, row in table.items()
               for index, observed in enumerate(row))
