"""Mealy machines: the models the course tests systems against.

A Mealy machine reads an input symbol and answers with an output symbol on the
same step, so a word of length n produces a word of length n. That is what
makes it the natural model of a reactive component: every call gets an answer.

    M = <Q, Sigma, Omega, delta, lambda, q0>

with states Q, inputs Sigma, outputs Omega, a transition function delta and an
output function lambda. Both are written together here as one table entry
``(target, output)``, exactly as the exercise sheets draw them.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MealyMachine:
    """A deterministic Mealy machine given by its transition table."""

    transitions: dict
    start: str
    name: str = "M"

    @property
    def states(self):
        """Every state, in a stable order."""
        return sorted(self.transitions)

    @property
    def alphabet(self):
        """Every input symbol, in a stable order."""
        symbols = set()
        for row in self.transitions.values():
            symbols |= set(row)
        return sorted(symbols)

    @property
    def outputs(self):
        """Every output symbol that appears in the table."""
        return sorted({output for row in self.transitions.values()
                       for _, output in row.values()})

    def step(self, state, symbol):
        """One transition: the state reached and the symbol answered."""
        return self.transitions[state][symbol]

    def run(self, word, state=None):
        """Feed a word and return the states passed through and the output word.

        The output has the same length as the input, which is the defining
        property of a Mealy machine and the reason a test oracle can compare
        them symbol by symbol.
        """
        current = self.start if state is None else state
        visited = [current]
        produced = []

        for symbol in word:
            current, output = self.step(current, symbol)
            visited.append(current)
            produced.append(output)

        return visited, "".join(str(output) for output in produced)

    def output(self, word, state=None):
        """The output word for an input word."""
        return self.run(word, state)[1]

    def last_output(self, word, state=None):
        """The final output symbol, which is what an observation table cell holds.

        The lecture fills the table with the last symbol only. It loses
        information the full word carries, and it is enough to separate states,
        which is all the table has to do.
        """
        produced = self.output(word, state)
        return produced[-1] if produced else ""

    def state_after(self, word, state=None):
        """The state the machine is in after reading a word."""
        return self.run(word, state)[0][-1]

    def reachable(self):
        """Every state reachable from the start, with a shortest word reaching it.

        The words form the *access sequences* the test generation needs: one
        way to get the machine into each state, chosen shortest so the tests
        stay short.
        """
        access = {self.start: ""}
        queue = [self.start]

        while queue:
            state = queue.pop(0)
            for symbol in self.alphabet:
                target, _ = self.step(state, symbol)
                if target not in access:
                    access[target] = access[state] + symbol
                    queue.append(target)

        return access

    def is_connected(self):
        """True when every state can be reached from the start."""
        return len(self.reachable()) == len(self.transitions)

    def __str__(self):
        """The transition table, one row per state."""
        rows = [f"{self.name}: start {self.start}"]
        header = "  state | " + " | ".join(f"on {symbol}" for symbol in self.alphabet)
        rows.append(header)
        for state in self.states:
            cells = []
            for symbol in self.alphabet:
                target, output = self.step(state, symbol)
                cells.append(f"{target}/{output}")
            rows.append(f"  {state:5} | " + " | ".join(cells))
        return "\n".join(rows)


def distinguishing_word(first, second, limit=None):
    """A shortest input word on which two machines produce different output.

    Breadth-first over pairs of states, which is the standard product
    construction: two machines disagree exactly when some reachable pair of
    states answers one symbol differently. The first such pair found gives the
    shortest word, and there is nothing shorter to find later.

    Returns None when the two machines are equivalent, which for finite
    machines this search decides: the number of state pairs is finite, so the
    search either finds a difference or exhausts them.
    """
    limit = limit or len(first.transitions) * len(second.transitions)
    alphabet = sorted(set(first.alphabet) | set(second.alphabet))

    start = (first.start, second.start)
    seen = {start}
    queue = [(start, "")]

    while queue:
        (left, right), word = queue.pop(0)
        if len(word) > limit:
            continue

        for symbol in alphabet:
            left_target, left_output = first.step(left, symbol)
            right_target, right_output = second.step(right, symbol)

            if left_output != right_output:
                return word + symbol

            pair = (left_target, right_target)
            if pair not in seen:
                seen.add(pair)
                queue.append((pair, word + symbol))

    return None


def equivalent(first, second):
    """True when no input word separates the two machines."""
    return distinguishing_word(first, second) is None


def minimise(machine):
    """Merge states no input word can tell apart, by partition refinement.

    Start with all states in one block and split whenever two states in a block
    answer some symbol differently or lead into different blocks. Repeat until
    nothing splits. That is Moore's algorithm, and the partition it ends with
    is the coarsest one that respects behaviour, so the quotient machine is the
    smallest machine with the same behaviour.
    """
    states = machine.states
    alphabet = machine.alphabet

    signature = {state: tuple(machine.step(state, symbol)[1] for symbol in alphabet)
                 for state in states}
    blocks = {}
    for state in states:
        blocks.setdefault(signature[state], []).append(state)
    block_of = {state: index for index, block in enumerate(blocks.values()) for state in block}

    while True:
        refined = {}
        for state in states:
            key = (block_of[state],) + tuple(
                block_of[machine.step(state, symbol)[0]] for symbol in alphabet)
            refined.setdefault(key, []).append(state)

        new_block_of = {state: index
                        for index, block in enumerate(refined.values())
                        for state in block}
        if new_block_of == block_of:
            break
        block_of = new_block_of

    representatives = {}
    for state in states:
        representatives.setdefault(block_of[state], state)

    transitions = {}
    for index, representative in sorted(representatives.items()):
        name = f"m{index}"
        row = {}
        for symbol in alphabet:
            target, output = machine.step(representative, symbol)
            row[symbol] = (f"m{block_of[target]}", output)
        transitions[name] = row

    return MealyMachine(transitions, f"m{block_of[machine.start]}",
                        name=f"min({machine.name})")


M1 = MealyMachine(
    transitions={
        "q0": {"a": ("q1", "0"), "b": ("q2", "1")},
        "q1": {"a": ("q1", "1"), "b": ("q2", "0")},
        "q2": {"a": ("q0", "0"), "b": ("q2", "1")},
    },
    start="q0",
    name="M1",
)
"""The machine from exercise sheet 5, used by the other folders in this topic."""

M3 = MealyMachine(
    transitions={
        "t0": {"a": ("t1", "0"), "b": ("t0", "0")},
        "t1": {"a": ("t1", "1"), "b": ("t2", "0")},
        "t2": {"a": ("t0", "0"), "b": ("t2", "0")},
    },
    start="t0",
    name="M3",
)
"""The target machine of the counterexample exercise."""

HYPOTHESIS = MealyMachine(
    transitions={
        "h0": {"a": ("h1", "0"), "b": ("h0", "0")},
        "h1": {"a": ("h1", "1"), "b": ("h0", "0")},
    },
    start="h0",
    name="H",
)
"""The wrong hypothesis of the counterexample exercise, two states instead of three."""
