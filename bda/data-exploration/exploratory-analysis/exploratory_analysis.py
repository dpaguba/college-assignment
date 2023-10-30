"""Looking at the data before modelling it, and what a summary hides.

A histogram depends on the number of bins, a scatter shows a grouping a
correlation cannot, and Simpson's paradox is the case where every group shows
one trend and the pooled data shows the opposite. All three say the same
thing: a number computed over everything describes a population that may not
exist.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "real-datasets"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "descriptive-statistics"))
import descriptive_statistics
import real_datasets


def histogram(values, bins):
    """The counts per bin over the range of the values."""
    low, high = min(values), max(values)
    width = (high - low) / bins if high > low else 1.0
    counts = {}
    for value in values:
        index = min(bins - 1, int((value - low) / width))
        counts[index] = counts.get(index, 0) + 1
    return counts


def scatter_separation(rows, first, second):
    """How much of the spread lies between the species and how much within.

    The quantity a scatter plot shows at a glance: when the between part
    dominates, the groups are visibly separated, and when it does not, the
    plot is a cloud.
    """
    groups = real_datasets.by_species(rows)
    overall = [real_datasets.overall_mean(rows, first),
               real_datasets.overall_mean(rows, second)]
    between = 0.0
    within = 0.0
    for group in groups.values():
        centre = [real_datasets.overall_mean(group, first),
                  real_datasets.overall_mean(group, second)]
        between += len(group) * sum((a - b) ** 2
                                    for a, b in zip(centre, overall))
        for row in group:
            point = [float(row[first]), float(row[second])]
            within += sum((a - b) ** 2 for a, b in zip(point, centre))
    return {"between": between, "within": within,
            "ratio": between / within if within else float("inf")}


def simpsons_paradox():
    """A data set where every group trends down and the pool trends up.

    Two groups, each with a negative relation between the two variables, and
    the groups placed so that the pooled relation is positive. Nothing is
    wrong with either computation, and reporting only one of them is
    misleading.
    """
    first_group = [(1.0, 4.0), (2.0, 3.5), (3.0, 3.0)]
    second_group = [(6.0, 8.0), (7.0, 7.5), (8.0, 7.0)]
    pooled = first_group + second_group
    return {"overall": descriptive_statistics.correlation(
        [point[0] for point in pooled], [point[1] for point in pooled]),
        "by group": {
            "first": descriptive_statistics.correlation(
                [point[0] for point in first_group],
                [point[1] for point in first_group]),
            "second": descriptive_statistics.correlation(
                [point[0] for point in second_group],
                [point[1] for point in second_group])}}
