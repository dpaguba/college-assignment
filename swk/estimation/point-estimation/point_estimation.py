"""Two-point and three-point estimation, with the spread that comes with it.

The question the lecture starts from: the effort of a work package is a random
variable with an unknown density, so how is it estimated in practice? By
asking for a smallest and a largest value, and optionally a middle one, then
**assuming a distribution** and computing from there.

    E(x) = (a + r*c + b) / (2 + r)        S(x) = (b - a) / u

The pair (r, u) is the assumption. The lecture's table gives several, and the
PERT approximation of a beta distribution, r = 4 and u = 6, is the one the
exercises use.

Two points is the same formula with r = 0, so the middle value simply does not
enter the expectation. The standard deviation stays (b - a) / 6, which is the
lecture's choice and worth noticing: the spread comes entirely from the range,
so two estimators who disagree only about the middle value report the same
uncertainty.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

DISTRIBUTIONS = {
    "two-point": (0, 6),
    "pert": (4, 6),
    "beta-quadratic": (4, 5.29),
    "beta-cubic": (6, 6),
    "beta-skewed": (4, 5.6),
}
"""The (r, u) pairs from the lecture's table of assumed distributions."""


@dataclass(frozen=True)
class WorkPackage:
    """One estimated piece of work: optimistic, likely and pessimistic effort."""

    name: str
    optimistic: float
    likely: float = None
    pessimistic: float = None

    def __post_init__(self):
        """Fills in the missing bound and rejects an inconsistent triple."""
        if self.pessimistic is None:
            raise ValueError("a package needs at least a smallest and a largest value")
        if self.optimistic > self.pessimistic:
            raise ValueError(f"{self.name}: the smallest value exceeds the largest")


@dataclass(frozen=True)
class Estimate:
    """The expectation, variance and standard deviation of an estimate."""

    expectation: float
    variance: float

    @property
    def deviation(self):
        """The standard deviation, which is the square root of the variance."""
        return math.sqrt(self.variance)

    def interval(self, sigmas=1.0):
        """The range within the given number of standard deviations.

        One sigma covers about 68 per cent of a normal distribution, two about
        95. Quoting an estimate as a single number throws this away, and it is
        the part a plan actually needs: 200 hours plus or minus 5 and 200 plus
        or minus 60 are different promises.
        """
        spread = sigmas * self.deviation
        return self.expectation - spread, self.expectation + spread

    def __str__(self):
        """The expectation and the deviation."""
        return f"E = {self.expectation:.2f}, S = {self.deviation:.2f}"


def estimate(package, distribution="pert"):
    """Expectation and variance for one package under an assumed distribution.

    With ``two-point`` the middle value is ignored, which is the point of the
    two-point estimate: it asks for less and assumes more.
    """
    r, u = DISTRIBUTIONS[distribution]
    middle = package.likely if package.likely is not None else 0

    if r and package.likely is None:
        raise ValueError(f"{package.name}: {distribution} needs a middle value")

    expectation = (package.optimistic + r * middle + package.pessimistic) / (2 + r)
    variance = ((package.pessimistic - package.optimistic) / u) ** 2
    return Estimate(expectation, variance)


def aggregate(packages, distribution="pert"):
    """Combine independent packages into one project estimate.

    Expectations add. Standard deviations do **not**: variances add, so the
    total deviation is the square root of their sum. That is why a project of
    many small packages is proportionally more predictable than one large
    package of the same size, and it holds only while the packages are
    independent. A shared bottleneck breaks it, and no formula here will say
    so.
    """
    estimates = [estimate(package, distribution) for package in packages]
    return Estimate(sum(item.expectation for item in estimates),
                    sum(item.variance for item in estimates))


def table(packages, distribution="pert"):
    """Per package expectation and deviation, plus the total."""
    rows = []
    for package in packages:
        item = estimate(package, distribution)
        rows.append((package.name, item.expectation, item.deviation))
    total = aggregate(packages, distribution)
    rows.append(("total", total.expectation, total.deviation))
    return rows


def simulate(packages, runs=20000, seed=20260831):
    """Monte Carlo over beta-PERT samples, as an independent check of the formulas.

    Each package is sampled from a beta distribution shaped to its three
    points, the samples are summed, and the mean and deviation of the sum are
    reported. If the closed form is right, the two agree.

    It also does something the formulas cannot: it produces the whole
    distribution of the total, so a question like "how likely is 400 hours"
    has an answer without assuming normality.
    """
    generator = random.Random(seed)
    totals = []

    for _ in range(runs):
        total = 0.0
        for package in packages:
            total += _sample_pert(generator, package)
        totals.append(total)

    mean = sum(totals) / len(totals)
    variance = sum((value - mean) ** 2 for value in totals) / (len(totals) - 1)
    totals.sort()
    return {
        "mean": mean,
        "deviation": math.sqrt(variance),
        "p10": totals[len(totals) // 10],
        "p50": totals[len(totals) // 2],
        "p90": totals[9 * len(totals) // 10],
    }


def _sample_pert(generator, package, shape=4.0):
    """One sample from a beta-PERT distribution over the package's range."""
    low, high = package.optimistic, package.pessimistic
    middle = package.likely if package.likely is not None else (low + high) / 2

    if high == low:
        return low

    alpha = 1 + shape * (middle - low) / (high - low)
    beta = 1 + shape * (high - middle) / (high - low)
    return low + generator.betavariate(alpha, beta) * (high - low)


def probability_within(packages, budget, runs=20000, seed=20260831):
    """The simulated chance of finishing inside a budget.

    The number a plan is usually missing. An estimate of 300 hours says
    nothing about the odds of 300 being enough, and here they are counted.
    """
    generator = random.Random(seed)
    inside = 0

    for _ in range(runs):
        total = sum(_sample_pert(generator, package) for package in packages)
        if total <= budget:
            inside += 1

    return inside / runs


GAME_PROJECT = (
    WorkPackage("Datenverwaltung", 8, 20, 25),
    WorkPackage("Gamelogik", 30, 64, 128),
    WorkPackage("Grafikengine", 42, 121, 180),
    WorkPackage("Gamepad-Interface", 8, 16, 20),
    WorkPackage("Security", 10, 30, 45),
)
"""The five components of the game project from exercise sheet 2."""
