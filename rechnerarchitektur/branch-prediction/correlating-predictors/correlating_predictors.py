"""Correlating and tournament predictors.

A saturating counter learns the bias of one branch. It cannot learn a pattern,
because it keeps no history: on an alternating sequence it is wrong every time,
which is worse than guessing.

A correlating predictor keeps the last `k` outcomes and uses them to select
among `2^k` counters. With one bit of history the alternating pattern becomes
two constant sub-patterns and is predicted almost perfectly. The cost is
exponential: each history bit doubles the table.

A tournament predictor runs two predictors and a third that learns which of
them to trust, per branch. It is the answer to the fact that different branches
want different predictors, and it is what shipped in the Alpha 21264.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "dynamic-predictors"))
import dynamic_predictors as dp


class Correlating:
    """A two-level predictor: a shift register selecting a counter."""

    def __init__(self, history_bits=2):
        """Allocate one saturating counter per history pattern."""
        self.history_bits = history_bits
        self.history = 0
        self.counters = [dp.TwoBit() for _ in range(2 ** history_bits)]

    def table_size(self):
        """How many counters the history length requires."""
        return len(self.counters)

    def predict(self):
        """The prediction of the counter this history selects."""
        return self.counters[self.history].predict()

    def update(self, outcome):
        """Update the selected counter, then shift the outcome into the history."""
        self.counters[self.history].update(outcome)
        mask = (1 << self.history_bits) - 1
        self.history = ((self.history << 1) | int(outcome)) & mask


class Tournament:
    """Two predictors and a chooser that learns which one to believe.

    The chooser is itself a saturating counter, updated only when the two
    disagree: agreement carries no information about which is better. That
    detail is what keeps the chooser from drifting on branches where both are
    right.
    """

    def __init__(self, history_bits=2):
        """Create the two component predictors and the chooser."""
        self.local = dp.TwoBit()
        self.global_predictor = Correlating(history_bits)
        self.chooser = dp.TwoBit(state=2)

    def predict(self):
        """The prediction of whichever component the chooser currently trusts."""
        if self.chooser.predict():
            return self.global_predictor.predict()
        return self.local.predict()

    def update(self, outcome):
        """Update both components, and the chooser only when they disagreed."""
        local_guess = self.local.predict()
        global_guess = self.global_predictor.predict()

        if local_guess != global_guess:
            self.chooser.update(global_guess == outcome)

        self.local.update(outcome)
        self.global_predictor.update(outcome)


def evaluate(predictor, outcomes):
    """Run any predictor over a branch history."""
    return dp.evaluate(predictor, outcomes)


def compare(outcomes, history_bits=2):
    """Every predictor's accuracy on one history, for the same input.

    The comparison is the point. No predictor wins on every pattern: the
    two-bit counter is best on a strongly biased branch and worst on an
    alternating one, and the correlating predictor is the other way round on
    short patterns with a small table.
    """
    return {
        "always taken": dp.evaluate(dp.Static(True), outcomes)["accuracy"],
        "one bit": dp.evaluate(dp.OneBit(), outcomes)["accuracy"],
        "two bit": dp.evaluate(dp.TwoBit(), outcomes)["accuracy"],
        "correlating": dp.evaluate(Correlating(history_bits), outcomes)["accuracy"],
        "tournament": dp.evaluate(Tournament(history_bits), outcomes)["accuracy"],
    }
