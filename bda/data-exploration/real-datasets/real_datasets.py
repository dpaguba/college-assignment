"""A real data set, and the questions a summary answers about it.

The lecture uses the Palmer penguins: three species measured on three
islands. Thirty-six rows are embedded here, twelve per species, so the module
runs without the file, and the loader reads the full file when a path is
given.

The point of using real data is the shape of the answer. The mean body mass
over all penguins is a number no penguin is near, because the species differ
by more than a kilogram, and a summary that ignores the grouping describes
nothing that exists.
"""

import csv
import io

COLUMNS = ["species", "island", "bill_length_mm", "bill_depth_mm",
           "flipper_length_mm", "body_mass_g", "sex"]
"""The columns of the data set."""

SAMPLE = [
    ("Adelie", "Dream", 39.2, 21.1, 196, 4150, "MALE"),
    ("Adelie", "Dream", 39.2, 18.6, 190, 4250, "MALE"),
    ("Adelie", "Torgersen", 42.5, 20.7, 197, 4500, "MALE"),
    ("Adelie", "Biscoe", 35.5, 16.2, 195, 3350, "FEMALE"),
    ("Adelie", "Dream", 37.2, 18.1, 178, 3900, "MALE"),
    ("Adelie", "Torgersen", 41.5, 18.3, 195, 4300, "MALE"),
    ("Adelie", "Torgersen", 38.6, 17, 188, 2900, "FEMALE"),
    ("Adelie", "Torgersen", 37.7, 19.8, 198, 3500, "MALE"),
    ("Adelie", "Dream", 33.1, 16.1, 178, 2900, "FEMALE"),
    ("Adelie", "Biscoe", 34.5, 18.1, 187, 2900, "FEMALE"),
    ("Adelie", "Biscoe", 35.3, 18.9, 187, 3800, "FEMALE"),
    ("Adelie", "Torgersen", 40.6, 19, 199, 4000, "MALE"),
    ("Chinstrap", "Dream", 45.4, 18.7, 188, 3525, "FEMALE"),
    ("Chinstrap", "Dream", 49.8, 17.3, 198, 3675, "FEMALE"),
    ("Chinstrap", "Dream", 52.2, 18.8, 197, 3450, "MALE"),
    ("Chinstrap", "Dream", 46.5, 17.9, 192, 3500, "FEMALE"),
    ("Chinstrap", "Dream", 49.3, 19.9, 203, 4050, "MALE"),
    ("Chinstrap", "Dream", 58, 17.8, 181, 3700, "FEMALE"),
    ("Chinstrap", "Dream", 50.1, 17.9, 190, 3400, "FEMALE"),
    ("Chinstrap", "Dream", 51.4, 19, 201, 3950, "MALE"),
    ("Chinstrap", "Dream", 45.9, 17.1, 190, 3575, "FEMALE"),
    ("Chinstrap", "Dream", 52, 20.7, 210, 4800, "MALE"),
    ("Chinstrap", "Dream", 46.1, 18.2, 178, 3250, "FEMALE"),
    ("Chinstrap", "Dream", 42.4, 17.3, 181, 3600, "FEMALE"),
    ("Gentoo", "Biscoe", 50, 15.2, 218, 5700, "MALE"),
    ("Gentoo", "Biscoe", 48.7, 14.1, 210, 4450, "FEMALE"),
    ("Gentoo", "Biscoe", 50, 15.9, 224, 5350, "MALE"),
    ("Gentoo", "Biscoe", 50.7, 15, 223, 5550, "MALE"),
    ("Gentoo", "Biscoe", 50, 16.3, 230, 5700, "MALE"),
    ("Gentoo", "Biscoe", 50.4, 15.7, 222, 5750, "MALE"),
    ("Gentoo", "Biscoe", 43.5, 15.2, 213, 4650, "FEMALE"),
    ("Gentoo", "Biscoe", 44.9, 13.3, 213, 5100, "FEMALE"),
    ("Gentoo", "Biscoe", 51.3, 14.2, 218, 5300, "MALE"),
    ("Gentoo", "Biscoe", 47.8, 15, 215, 5650, "MALE"),
    ("Gentoo", "Biscoe", 46.5, 14.4, 217, 4900, "FEMALE"),
    ("Gentoo", "Biscoe", 45.5, 14.5, 212, 4750, "FEMALE"),
]
"""Twelve rows per species, drawn from the full file."""


def rows(path=None):
    """The embedded sample, or the full file when a path is given."""
    if path is None:
        return [dict(zip(COLUMNS, row)) for row in SAMPLE]
    with io.open(path, encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if row["body_mass_g"]]


def numeric(values, column):
    """One numeric column as a list of floats."""
    return [float(row[column]) for row in values if row[column] not in ("", None)]


def by_species(values):
    """The rows grouped by species."""
    groups = {}
    for row in values:
        groups.setdefault(row["species"], []).append(row)
    return groups


def group_means(values, column):
    """The mean of a column within each species."""
    return {name: sum(numeric(group, column)) / len(group)
            for name, group in by_species(values).items()}


def overall_mean(values, column):
    """The mean over everything, which the group means straddle."""
    numbers = numeric(values, column)
    return sum(numbers) / len(numbers)
