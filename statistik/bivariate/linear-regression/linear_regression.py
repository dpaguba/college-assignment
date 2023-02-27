"""The least squares line, and why it is not symmetric.

The line minimises the squared vertical distances, so it treats one variable
as the one being explained. Regressing height on age and age on height gives
two different lines, and the product of their slopes is the squared
correlation, which is 1 exactly when the points lie on a line.

For the children's data of the third sheet the published line is
height = 103.5 + 3.5 · age.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "correlation"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "descriptive", "dispersion"))
import correlation
import dispersion


def fit(x, y):
    """The slope and intercept of the least squares line."""
    slope = correlation.covariance(x, y) / dispersion.variance(x)
    intercept = sum(y) / len(y) - slope * sum(x) / len(x)
    return {"slope": slope, "intercept": intercept}


def predict(line, value):
    """The value the line predicts."""
    return line["intercept"] + line["slope"] * value


def residuals(line, x, y):
    """The differences between the observed and the predicted values."""
    return [observed - predict(line, value) for value, observed in zip(x, y)]


def squared_error(line, x, y):
    """The quantity the fit minimises."""
    return sum(value ** 2 for value in residuals(line, x, y))


def r_squared(line, x, y):
    """The share of the variance the line explains."""
    average = sum(y) / len(y)
    total = sum((observed - average) ** 2 for observed in y)
    return 1 - squared_error(line, x, y) / total
