"""Planning poker: turning several opinions into one number, and why it works.

Everyone estimates a story at the same time, the extremes explain themselves,
and the round is repeated. The lecture's point is that the discussion, not the
number, is the product: the highest and the lowest estimator each know
something the others do not, and the re-estimate is where that knowledge moves.

The deck is not linear. Larger stories are estimated less precisely, and the
gaps in the sequence say so plainly instead of pretending that 17 and 18 are
distinguishable.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field

FIBONACCI = (1, 2, 3, 5, 8, 13, 21)
"""The usual deck: gaps grow with size, because precision does not."""

MODIFIED_FIBONACCI = (0, 0.5, 1, 2, 3, 5, 8, 13, 20, 40, 100)
"""The commercial variant, with a zero, a half, and a "too big to estimate" card."""

TSHIRT = ("XS", "S", "M", "L", "XL")
"""Sizes for when numbers invite false arithmetic."""


@dataclass
class Round:
    """One round of estimates, with the spread that decides whether to repeat."""

    estimates: dict

    @property
    def values(self):
        """The numbers offered, sorted."""
        return sorted(self.estimates.values())

    @property
    def lowest(self):
        """The estimator with the smallest number, who speaks first."""
        return min(self.estimates, key=self.estimates.get)

    @property
    def highest(self):
        """The estimator with the largest number, who speaks second."""
        return max(self.estimates, key=self.estimates.get)

    @property
    def spread(self):
        """The ratio between the largest and the smallest estimate.

        A ratio rather than a difference, because on an exponential deck the
        distance from 1 to 2 and from 13 to 21 mean the same thing.
        """
        low, high = self.values[0], self.values[-1]
        return high / low if low else float("inf")

    def consensus(self, tolerance=2.0):
        """Whether the round is close enough to stop.

        The usual rule is that the extremes must be within one card of each
        other; the ratio form here is the same rule stated so it also works on
        a deck with different gaps.
        """
        return self.spread <= tolerance

    def __str__(self):
        """The estimates offered in this round and their spread."""
        offered = ", ".join(f"{name}={value}" for name, value in sorted(self.estimates.items()))
        return f"{offered}  (spread {self.spread:.1f})"


def result(rounds, deck=FIBONACCI):
    """The agreed number after the last round, rounded to a card on the deck.

    The median, not the mean: an average of 3 and 13 is 8, which nobody
    offered, while the median keeps the answer inside what the team actually
    said.
    """
    final = rounds[-1].values
    middle = statistics.median(final)
    return min(deck, key=lambda card: (abs(card - middle), card))


def run(rounds, deck=FIBONACCI, tolerance=2.0):
    """Report the progress of a session, round by round.

    Returns the rounds with their spread, whether each reached consensus, and
    the number the session settled on.
    """
    report = []
    for number, round_ in enumerate(rounds, start=1):
        report.append({
            "round": number,
            "estimates": dict(round_.estimates),
            "spread": round(round_.spread, 2),
            "consensus": round_.consensus(tolerance),
            "explains": (round_.lowest, round_.highest),
        })
    return report, result(rounds, deck)


def triangulate(stories, deck=FIBONACCI):
    """Check estimates against each other rather than against hours.

    The lecture's own advice: a two-point story should look about twice a
    one-point story, and two five-point stories should look alike. This lists
    the pairs where the ratio of points is far from the ratio of the reference
    sizes given, which is where a scale has drifted.

    ``stories`` maps a name to (points, reference size in whatever unit the
    team compares in).
    """
    names = sorted(stories)
    suspicious = []

    for index, first in enumerate(names):
        for second in names[index + 1:]:
            first_points, first_size = stories[first]
            second_points, second_size = stories[second]
            if not (first_points and second_points and first_size and second_size):
                continue

            point_ratio = first_points / second_points
            size_ratio = first_size / second_size
            if point_ratio / size_ratio > 2 or size_ratio / point_ratio > 2:
                suspicious.append((first, second, round(point_ratio, 2), round(size_ratio, 2)))

    return suspicious


def to_hours(points, velocity, sprint_length_days=10):
    """Convert story points to a duration through velocity, never directly.

    Points have no time in them. The only bridge is measured velocity, which
    is why this function needs it as an argument and why a team that has not
    measured yet cannot answer the question at all.
    """
    if velocity <= 0:
        raise ValueError("velocity must be positive to convert points into time")
    return points / velocity * sprint_length_days
