"""Branch predictors, from a fixed guess to a saturating counter.

A pipeline that resolves branches late must guess, and every wrong guess costs
the instructions fetched since. The predictors differ only in how much history
they keep, and each extra bit buys a specific failure it no longer makes.

The canonical measurement is a loop of `n` iterations, which is `n-1` taken
branches and one not taken:

| predictor | mispredictions per loop |
|---|---|
| always taken | 1, the exit |
| one bit | **2**, the exit and the next entry |
| two bit | **1**, only the exit |

The one-bit predictor's second miss is the one worth understanding: after the
exit it predicts not taken, so the first branch of the next loop is wrong too.
The second bit is exactly the memory needed to treat one exception as noise.

The first loop is cheaper than the rest, which is easy to miss when quoting the
table. Starting from "taken", four nested loops of five branches cost
`1 + 2 * 3 = 7` mispredictions, not 8: the initial state happens to be right,
so the first loop pays only for its exit.
"""

from __future__ import annotations


class Static:
    """A predictor that always guesses the same way."""

    def __init__(self, taken):
        """Fix the guess."""
        self.taken = taken

    def predict(self):
        """The fixed guess."""
        return self.taken

    def update(self, outcome):
        """Ignore the outcome, since nothing is learned."""


class OneBit:
    """Predict whatever happened last time."""

    def __init__(self, taken=True):
        """Start from an initial guess."""
        self.state = taken

    def predict(self):
        """The last outcome."""
        return self.state

    def update(self, outcome):
        """Remember the outcome, discarding the previous one."""
        self.state = outcome


class TwoBit:
    """A saturating counter: two wrong guesses are needed to change the mind.

    Four states, strongly and weakly taken and their opposites. The counter
    moves one step per outcome and the prediction is its top bit, so a single
    exception moves the state without flipping the prediction.
    """

    def __init__(self, state=3):
        """Start strongly taken, which is the usual initialisation."""
        self.state = state

    def predict(self):
        """Taken when the counter is in its upper half."""
        return self.state >= 2

    def update(self, outcome):
        """Saturate towards the outcome."""
        if outcome:
            self.state = min(3, self.state + 1)
        else:
            self.state = max(0, self.state - 1)


def evaluate(predictor, outcomes):
    """Run a predictor over a branch history, counting mispredictions."""
    wrong = 0
    trace = []

    for outcome in outcomes:
        guess = predictor.predict()
        trace.append((guess, outcome))
        if guess != outcome:
            wrong += 1
        predictor.update(outcome)

    total = len(outcomes)
    return {"mispredictions": wrong, "total": total,
            "accuracy": (total - wrong) / total if total else 1.0,
            "trace": trace}


def cpi_penalty(result, branch_fraction, penalty):
    """How much a misprediction rate adds to the CPI.

    The three factors multiply: how many instructions are branches, how often
    the prediction is wrong, and how many cycles a wrong one costs. Improving
    any one of them is worth the same, which is why deep pipelines invest so
    heavily in the middle factor: their penalty is fixed by the depth.
    """
    return branch_fraction * (1 - result["accuracy"]) * penalty


def loop_mispredictions(iterations, predictor_kind):
    """Mispredictions for one pass through a loop of a given length.

    The measurement the textbook table is built from, computed rather than
    quoted so that the claim can be checked at any loop length.
    """
    outcomes = [True] * (iterations - 1) + [False]
    predictor = OneBit() if predictor_kind == "one bit" else TwoBit()
    return evaluate(predictor, outcomes)["mispredictions"]
