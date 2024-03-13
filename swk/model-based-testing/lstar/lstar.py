"""L*: learning a Mealy machine from queries alone.

Angluin's algorithm, 1987. The learner sees no code and no states. It may ask
two kinds of question:

- a **membership query**: run this input word, what comes back?
- an **equivalence query**: is this hypothesis right? If not, give me a word
  where it differs.

The loop is short: fill an observation table, close it, make it consistent,
build the hypothesis, ask whether it is right, and on a counterexample refine
the table and go round again. Each round adds at least one state, and the
target has finitely many, so it terminates.

Where the equivalence query comes from in practice is the real problem. No
real system answers it, so it is approximated by a test suite, and the learned
model is then only as good as those tests. That is exactly why the test
generation folder next door exists.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mealy-machines"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "observation-table"))

from mealy_machines import MealyMachine, distinguishing_word
from observation_table import ObservationTable


@dataclass
class Statistics:
    """What the learning run cost, which is how learners are compared."""

    rounds: int = 0
    membership_queries: int = 0
    equivalence_queries: int = 0
    counterexamples: list = field(default_factory=list)

    def __str__(self):
        """The query counts that describe one run of the algorithm."""
        return (f"rounds {self.rounds}, membership queries {self.membership_queries}, "
                f"equivalence queries {self.equivalence_queries}, "
                f"counterexamples {self.counterexamples}")


def learn(alphabet, membership, equivalence, strategy="suffixes", limit=50):
    """Learn a Mealy machine from a membership and an equivalence oracle.

    ``membership`` takes an input word and returns the last output symbol.
    ``equivalence`` takes a hypothesis and returns None when it is correct or a
    counterexample word when it is not.

    ``strategy`` decides how a counterexample is used:

    - ``suffixes`` adds every suffix of it as a new column, which is simple and
      can add many columns at once
    - ``rivest-schapire`` binary searches for the single suffix that carries
      the difference, which adds one column per counterexample and is what
      makes the algorithm practical on larger systems
    """
    statistics = Statistics()
    table = ObservationTable(tuple(alphabet), membership)

    while statistics.rounds < limit:
        statistics.rounds += 1

        while True:
            table.close()
            if table.make_consistent() == 0:
                break

        hypothesis = table.hypothesis()
        statistics.equivalence_queries += 1
        counterexample = equivalence(hypothesis)

        if counterexample is None:
            statistics.membership_queries = table.queries
            return hypothesis, table, statistics

        statistics.counterexamples.append(counterexample)

        if strategy == "rivest-schapire":
            table.add_suffix(_rivest_schapire(table, hypothesis, counterexample, membership))
        else:
            for index in range(len(counterexample)):
                table.add_suffix(counterexample[index:])

    raise RuntimeError("the learner did not converge within the round limit")


def _rivest_schapire(table, hypothesis, counterexample, membership):
    """Find one suffix that explains a counterexample, by binary search.

    The idea: walking the counterexample, the hypothesis and the real system
    agree at the start and disagree at the end, so somewhere there is a
    position where the prediction breaks. Binary search finds it in log(n)
    membership queries instead of adding all n suffixes.
    """
    def prediction(index):
        """What the hypothesis answers for the split at this position."""
        prefix, suffix = counterexample[:index], counterexample[index:]
        state = hypothesis.state_after(prefix)
        access = _access_word(table, hypothesis, state)
        return membership(access + suffix)

    low, high = 0, len(counterexample)
    target = membership(counterexample)

    while high - low > 1:
        middle = (low + high) // 2
        if prediction(middle) == target:
            low = middle
        else:
            high = middle

    return counterexample[high:] or counterexample[-1:]


def _access_word(table, hypothesis, state):
    """The row word of the upper part that reaches a given hypothesis state."""
    for prefix in table.prefixes:
        if hypothesis.state_after(prefix) == state:
            return prefix
    return ""


def perfect_oracle(target):
    """An equivalence oracle that knows the answer, for studying the algorithm.

    Real learning never has this. It is here so the learner can be run against
    a known machine and checked, and so the cost of learning can be separated
    from the cost of approximating the oracle.
    """
    def ask(hypothesis):
        """The oracle: a distinguishing word, or None when they agree."""
        return distinguishing_word(hypothesis, target)
    return ask


def testing_oracle(target, suite):
    """An equivalence oracle backed by a finite test suite.

    This is what a real learner uses. It returns the first word in the suite on
    which the hypothesis and the system disagree, and None when the suite finds
    nothing, which is not the same as the hypothesis being correct: an
    incomplete suite makes the learner stop early and confidently.
    """
    def ask(hypothesis):
        """The oracle restricted to a finite suite, which may miss a difference."""
        for word in suite:
            if hypothesis.output(word) != target.output(word):
                return word
        return None
    return ask
