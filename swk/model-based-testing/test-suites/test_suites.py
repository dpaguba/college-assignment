"""Generating tests from a model, and using the model as the oracle.

Model-based testing turns a state machine into two things: a set of input
words worth running, and a prediction for each of them. The prediction is the
part that makes the tests automatic. Without a model, a test suite is a list
of inputs and someone has to say what the right answer is.

The covers here get progressively stronger and progressively larger:

- **state cover**: reach every state at least once
- **transition cover**: take every transition at least once
- **transition-switch cover**: take every executable *pair* of consecutive
  transitions, which catches faults that depend on where you came from
- **W-method**: transition cover followed by a distinguishing set, which is
  complete for machines with no more states than assumed
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mealy-machines"))

from mealy_machines import MealyMachine


def state_cover(machine):
    """One shortest word per reachable state.

    These are the access sequences every other cover is built on: to test
    something about a state, you first have to get there.
    """
    return sorted(machine.reachable().values(), key=lambda word: (len(word), word))


def transition_cover(machine):
    """Every access word extended by one symbol.

    Running these takes each transition at least once. It is the weakest cover
    that touches the whole table, and it misses anything that only goes wrong
    on the second step.
    """
    access = machine.reachable()
    words = set()

    for state, word in access.items():
        for symbol in machine.alphabet:
            words.add(word + symbol)

    return sorted(words, key=lambda word: (len(word), word))


def transition_pairs(machine):
    """Every executable pair of consecutive transitions.

    A pair is identified by where it starts and which two symbols are read:
    ``(state, first symbol, second symbol)``. For a deterministic machine with
    n states over an alphabet of size k there are exactly n * k * k of them,
    which for the exercise machine is 3 * 2 * 2 = 12.
    """
    found = []
    for state in machine.states:
        for first, second in product(machine.alphabet, repeat=2):
            middle, _ = machine.step(state, first)
            found.append((state, first, second, middle))
    return found


def transition_switch_cover(machine):
    """A suite covering every pair of consecutive transitions.

    Built systematically from the access sequences: for each state q and each
    pair of symbols xy, the word ``access(q) + x + y`` executes exactly that
    pair. The suite is the set of those words.

    This is the cover the exercise asks for, and the construction is the one
    its solution uses.
    """
    access = machine.reachable()
    words = set()

    for state, word in access.items():
        for first, second in product(machine.alphabet, repeat=2):
            words.add(word + first + second)

    return sorted(words, key=lambda word: (len(word), word))


def characterising_set(machine):
    """A set of words that tells any two different states apart.

    The W of the W-method. For each pair of states, a shortest word on which
    they answer differently is found by breadth-first search and added. The
    set is what turns a transition cover into a complete test suite.
    """
    words = set()
    states = machine.states

    for index, first in enumerate(states):
        for second in states[index + 1:]:
            separator = _separate(machine, first, second)
            if separator is not None:
                words.add(separator)

    return sorted(words, key=lambda word: (len(word), word))


def _separate(machine, first, second, limit=None):
    """The shortest word on which the two states differ."""
    limit = limit or len(machine.states) ** 2
    seen = {(first, second)}
    queue = [((first, second), "")]

    while queue:
        (left, right), word = queue.pop(0)
        if len(word) > limit:
            continue

        for symbol in machine.alphabet:
            left_target, left_output = machine.step(left, symbol)
            right_target, right_output = machine.step(right, symbol)

            if left_output != right_output:
                return word + symbol

            pair = (left_target, right_target)
            if pair not in seen:
                seen.add(pair)
                queue.append((pair, word + symbol))

    return None


def w_method(machine, extra_states=0):
    """The W-method suite: transition cover, then every distinguishing word.

    Complete under one assumption: the system under test has at most
    ``len(states) + extra_states`` states. Under that assumption, passing every
    test in this suite proves equivalence, which is a rare thing for a finite
    test suite to be able to claim.

    The suite grows quickly. With extra states allowed it includes every
    intermediate word of that length, so the size is multiplied by the alphabet
    raised to that power, which is why the assumption is usually kept small.
    """
    middles = [""]
    for length in range(1, extra_states + 1):
        middles.extend("".join(word) for word in product(machine.alphabet, repeat=length))

    suite = set()
    for prefix in transition_cover(machine):
        for middle in middles:
            for suffix in characterising_set(machine):
                suite.add(prefix + middle + suffix)

    return sorted(suite, key=lambda word: (len(word), word))


@dataclass
class OracleResult:
    """The verdict for one test: the input, what was expected, what came back."""

    word: str
    expected: str
    actual: str

    @property
    def passed(self):
        """True when the system answered exactly what the model predicts."""
        return self.expected == self.actual

    def __str__(self):
        """The verdict with the expected and the observed output."""
        verdict = "pass" if self.passed else "FAIL"
        return f"{verdict}  {self.word}: expected {self.expected}, got {self.actual}"


def oracle(model, system, word):
    """Compare one run of the system against the model's prediction.

    ``system`` is any function from an input word to an output word. In the
    exercise it is a claim written on paper; in practice it is the real
    implementation.
    """
    expected = model.output(word)
    actual = system(word) if callable(system) else system.output(word)
    return OracleResult(word, expected, actual)


def run_suite(model, system, suite):
    """Run every test and return the results, failures first."""
    results = [oracle(model, system, word) for word in suite]
    return sorted(results, key=lambda result: result.passed)


def covered_pairs(machine, suite):
    """Which transition pairs a suite actually executes.

    The check that a suite delivers what it claims. Running it against the
    generator is how a cover is validated: build the suite, walk it on the
    machine, and confirm that every pair shows up.
    """
    covered = set()

    for word in suite:
        states, _ = machine.run(word)
        for index in range(len(word) - 1):
            covered.add((states[index], word[index], word[index + 1],
                         states[index + 1]))

    return covered
