"""Variants of the Turing machine, and why none of them is stronger.

Multiple tapes, nondeterminism, a queue instead of a tape: each looks like more
power and each accepts exactly the same languages. That robustness is the real
argument for the Church-Turing thesis, much more than any single model.

What the variants **do** change is time. A multi-tape machine can be simulated
on one tape with a quadratic slowdown, and a nondeterministic one with an
exponential one, and those two costs are where the complexity questions of the
fourth block come from.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "turing-machines"))

from turing_machines import BLANK, LEFT, RIGHT, STAY, Tape, TuringMachine


@dataclass
class MultiTapeTM:
    """A machine with several tapes, each with its own head.

    A transition reads the tuple of symbols under the heads and writes a tuple
    back, moving each head independently.
    """

    states: set
    input_alphabet: tuple
    tape_alphabet: tuple
    transitions: dict
    start: str
    accept: str
    tapes: int = 2
    blank: str = BLANK
    name: str = "MT"

    def run(self, word, limit=10000):
        """Run on an input placed on the first tape."""
        tapes = [Tape.of(word, self.blank)] + [Tape() for _ in range(self.tapes - 1)]
        state = self.start

        for steps in range(limit):
            if state == self.accept:
                return {"outcome": "accept", "steps": steps, "tapes": tapes}

            read = tuple(tape.read(self.blank) for tape in tapes)
            move = self.transitions.get((state, read))
            if move is None:
                return {"outcome": "reject", "steps": steps, "tapes": tapes}

            state, written, directions = move
            for index, tape in enumerate(tapes):
                tape.write(written[index])
                tape.move(directions[index])

        return {"outcome": "limit", "steps": limit, "tapes": tapes}

    def accepts(self, word, limit=10000):
        """Whether the machine accepts the word."""
        return self.run(word, limit)["outcome"] == "accept"

    def language(self, max_length, limit=2000):
        """Every accepted word up to a length."""
        found = []
        queue = [""]
        while queue:
            word = queue.pop(0)
            if self.accepts(word, limit):
                found.append(word)
            if len(word) < max_length:
                queue.extend(word + symbol for symbol in self.input_alphabet)
        return found


def simulate_multitape(machine, word, limit=10000):
    """Run a multi-tape machine the way one tape would, and count the cost.

    A single-tape machine stores the k tapes in interleaved tracks and makes a
    full sweep over the used part for every step of the original. That is where
    the quadratic slowdown comes from: t steps of a k-tape machine become
    O(t²) steps on one tape, because each of the t steps costs a sweep whose
    length grows with t.

    The simulation here counts what those sweeps would cost rather than
    building the single-tape machine, which would be correct and unreadable.
    """
    result = machine.run(word, limit)
    used = sum(len(tape.cells) for tape in result["tapes"])

    return {
        "outcome": result["outcome"],
        "multitape steps": result["steps"],
        "single tape steps": result["steps"] * max(1, used) * machine.tapes,
        "cells used": used,
    }


@dataclass
class NondeterministicTM:
    """A machine whose transition function returns a **set** of moves."""

    states: set
    input_alphabet: tuple
    tape_alphabet: tuple
    transitions: dict
    start: str
    accept: str
    blank: str = BLANK
    name: str = "N"

    def accepts(self, word, limit=20000):
        """Search every computation path, breadth-first.

        Breadth-first and not depth-first, on purpose: one branch may run for
        ever, and depth-first would follow it and never come back. Breadth
        gives the standard result that a nondeterministic machine is simulated
        by a deterministic one, at an exponential cost in the branching depth.
        """
        start = (self.start, "", 0, word)
        queue = [start]
        seen = {start}
        explored = 0

        while queue and explored < limit:
            explored += 1
            state, written, position, tape_word = queue.pop(0)

            tape = Tape.of(tape_word, self.blank)
            tape.position = position
            for index, symbol in enumerate(written):
                if symbol != "\0":
                    tape.cells[index] = symbol

            if state == self.accept:
                return True, explored

            symbol = tape.read(self.blank)
            for target, write, direction in self.transitions.get((state, symbol), ()):
                copy = tape.copy()
                copy.write(write)
                copy.move(direction)

                low = min(list(copy.cells) + [copy.position])
                high = max(list(copy.cells) + [copy.position])
                if high - low > len(word) + 6:
                    continue

                snapshot = (target, "".join(copy.cells.get(index, self.blank)
                                            for index in range(low, high + 1)),
                            copy.position - low, tape_word)
                if snapshot not in seen:
                    seen.add(snapshot)
                    queue.append(snapshot)

        return False, explored

    def language(self, max_length, limit=6000):
        """Every accepted word up to a length."""
        found = []
        queue = [""]
        while queue:
            word = queue.pop(0)
            if self.accepts(word, limit)[0]:
                found.append(word)
            if len(word) < max_length:
                queue.extend(word + symbol for symbol in self.input_alphabet)
        return found


@dataclass
class QueueAutomaton:
    """A finite control with a queue, defined as the course defines it.

    ``A = (Q, Sigma, Gamma, delta, s, F)`` with
    ``delta subset Q x (Sigma + eps) x (Gamma + eps) x Q x Gamma*``, a queue
    that **starts empty**, and acceptance by final state.

    A transition with a queue symbol requires that symbol at the front and
    removes it. A transition with epsilon there fires whatever the queue holds
    and removes nothing. Either way the produced string is appended at the
    back.

    The exercise asks why this is as strong as a Turing machine. The answer is
    rotation: repeatedly taking the front and appending it at the back walks
    the whole content past the head, so the machine can inspect and rewrite
    everything. A stack cannot, because reading destroys, which is exactly the
    gap between this model and a pushdown automaton.
    """

    states: set
    input_alphabet: tuple
    queue_alphabet: tuple
    transitions: dict
    start: str
    accepting: set
    name: str = "Q"

    def accepts(self, word, limit=20000):
        """Breadth-first over configurations of state, remaining input and queue."""
        start = (self.start, word, "")
        queue = [start]
        seen = {start}
        steps = 0

        while queue and steps < limit:
            steps += 1
            state, rest, contents = queue.pop(0)

            if state in self.accepting and not rest:
                return True

            reads = [("", rest)] + ([(rest[0], rest[1:])] if rest else [])
            fronts = [("", contents)] + ([(contents[0], contents[1:])] if contents else [])

            for symbol, remaining in reads:
                for front, tail in fronts:
                    for target, appended in self.transitions.get((state, symbol, front), ()):
                        following = (target, remaining, tail + appended)
                        if following in seen or len(following[2]) > len(word) + 6:
                            continue
                        seen.add(following)
                        queue.append(following)

        return False

    def language(self, max_length, limit=8000):
        """Every accepted word up to a length."""
        found = []
        pending = [""]
        while pending:
            word = pending.pop(0)
            if self.accepts(word, limit):
                found.append(word)
            if len(word) < max_length:
                pending.extend(word + symbol for symbol in self.input_alphabet)
        return found


def two_tape_separator():
    """A two-tape machine deciding ``{ w # w }``.

    Copy everything before the separator to the second tape, rewind that tape,
    then walk both forward comparing symbol by symbol. Two heads make it one
    sweep each way; on a single tape the same job is a long back-and-forth,
    which is where the quadratic simulation cost comes from.
    """
    transitions = {}

    for symbol in ("a", "b"):
        transitions[("copy", (symbol, BLANK))] = ("copy", (symbol, symbol), (RIGHT, RIGHT))

    transitions[("copy", ("#", BLANK))] = ("rewind", ("#", BLANK), (RIGHT, LEFT))

    for first in ("a", "b", "#", BLANK):
        for second in ("a", "b"):
            transitions[("rewind", (first, second))] = ("rewind", (first, second), (STAY, LEFT))
        transitions[("rewind", (first, BLANK))] = ("compare", (first, BLANK), (STAY, RIGHT))

    for symbol in ("a", "b"):
        transitions[("compare", (symbol, symbol))] = ("compare", (symbol, symbol), (RIGHT, RIGHT))

    transitions[("compare", (BLANK, BLANK))] = ("accept", (BLANK, BLANK), (STAY, STAY))

    return MultiTapeTM({"copy", "rewind", "compare", "accept"}, ("a", "b", "#"),
                       ("a", "b", "#", BLANK), transitions, "copy", "accept", 2,
                       BLANK, "w # w on two tapes")


def nondeterministic_contains():
    """A nondeterministic machine accepting the words that contain ``aa``.

    At every position it may either move on or claim that the pattern starts
    here. The claim is then checked, and a wrong guess simply dies.

    Nondeterminism adds no power, and it does shorten descriptions: the
    deterministic version has to remember what it has just seen, this one
    guesses and verifies. The cost is paid at simulation time, in the number of
    branches the search explores.
    """
    transitions = {}

    for symbol in ("a", "b"):
        transitions[("scan", symbol)] = {("scan", symbol, RIGHT)}

    transitions[("scan", "a")] = {("scan", "a", RIGHT), ("first", "a", RIGHT)}
    transitions[("first", "a")] = {("accept", "a", STAY)}

    return NondeterministicTM({"scan", "first", "accept"}, ("a", "b"),
                              ("a", "b", BLANK), transitions, "scan", "accept",
                              BLANK, "contains aa, by guessing")


def queue_equal_counts():
    """A queue automaton accepting ``a^n b^n``, in the course's model.

    Append an ``A`` for each ``a``, then at some guessed moment append an end
    marker and start matching ``b`` against the front of the queue. Because the
    queue is first in first out, the marker can only reach the front after
    every ``A`` has been consumed, so the counts must agree exactly. Too many
    ``b`` and the marker blocks; too few and the input ends with the marker
    still buried.

    No rotation is needed here, which is worth noticing: this language is
    within reach of a stack too. The rotation argument is what the exercise
    needs for the general claim about Turing machines.
    """
    transitions = {
        ("push", "a", ""): {("push", "A")},
        ("push", "", ""): {("match", "#")},
        ("match", "b", "A"): {("match", "")},
        ("match", "", "#"): {("accept", "")},
    }
    return QueueAutomaton({"push", "match", "accept"}, ("a", "b"), ("A", "#"),
                          transitions, "push", {"accept"}, "queue a^n b^n")
