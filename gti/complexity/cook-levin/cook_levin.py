"""Cook and Levin: a computation becomes a formula.

The theorem that starts everything: SAT is NP-complete, proved directly rather
than by reduction from something else. The construction encodes an accepting
computation of a nondeterministic machine as a propositional formula, so that

    the formula is satisfiable  <=>  the machine accepts the input in t steps

A satisfying assignment **is** the computation, written out cell by cell.

The encoding is a tableau: one row per step, one column per tape cell, with
variables saying what is in each cell, where the head is and what state the
machine is in. Four groups of clauses then say that the first row is the start,
that every row follows from the one above it, that the machine ends up
accepting, and that each cell holds exactly one thing.

Only small machines and small step bounds are feasible here. The point is not
to run it but to see that the formula exists and that the assignment can be
read back as a run.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "computability" / "turing-machines"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "np-problems"))

import np_problems as problems
from turing_machines import BLANK, LEFT, RIGHT, STAY, TuringMachine


@dataclass
class Encoding:
    """The formula, plus the dictionary that names its variables."""

    clauses: list
    names: dict
    steps: int
    width: int

    def variable(self, kind, *arguments):
        """The number of the variable for one fact about the tableau."""
        return self.names[(kind, *arguments)]

    def decode(self, assignment):
        """Read a satisfying assignment back as a sequence of configurations."""
        configurations = []

        for step in range(self.steps + 1):
            state = next((name[2] for name, number in self.names.items()
                          if name[0] == "state" and name[1] == step
                          and assignment.get(number)), None)
            head = next((name[2] for name, number in self.names.items()
                         if name[0] == "head" and name[1] == step
                         and assignment.get(number)), None)
            tape = []
            for cell in range(self.width):
                symbol = next((name[3] for name, number in self.names.items()
                               if name[0] == "cell" and name[1] == step
                               and name[2] == cell and assignment.get(number)), "?")
                tape.append(symbol)

            configurations.append({"step": step, "state": state, "head": head,
                                   "tape": "".join(tape)})

        return configurations


def encode(machine, word, steps, width=None):
    """Build the tableau formula for a machine, an input and a step bound.

    Variables:

    - ``cell(t, i, s)``: at time t, tape cell i holds symbol s
    - ``head(t, i)``: at time t, the head is on cell i
    - ``state(t, q)``: at time t, the machine is in state q

    Clauses:

    1. **start**: the first row spells the input, the head is at 0, the state
       is the start state
    2. **uniqueness**: each cell holds exactly one symbol, the head is in
       exactly one place, the machine is in exactly one state
    3. **transitions**: the row at t+1 follows the row at t by the transition
       function, and cells away from the head do not change
    4. **acceptance**: the accepting state appears somewhere

    The size is polynomial in the step bound, which is the whole point: an
    accepting run of polynomial length becomes a formula of polynomial size, so
    every problem in NP reduces to SAT.
    """
    width = width or (len(word) + steps + 2)
    alphabet = tuple(sorted(set(machine.tape_alphabet) | {machine.blank}))
    states = sorted(machine.states)

    names = {}

    def number(key):
        """The variable number for a key, allocated on first use."""
        if key not in names:
            names[key] = len(names) + 1
        return names[key]

    clauses = []

    for step in range(steps + 1):
        for cell in range(width):
            options = [number(("cell", step, cell, symbol)) for symbol in alphabet]
            clauses.append(options)
            for first in range(len(options)):
                for second in range(first + 1, len(options)):
                    clauses.append([-options[first], -options[second]])

        heads = [number(("head", step, cell)) for cell in range(width)]
        clauses.append(heads)
        for first in range(len(heads)):
            for second in range(first + 1, len(heads)):
                clauses.append([-heads[first], -heads[second]])

        state_options = [number(("state", step, state)) for state in states]
        clauses.append(state_options)
        for first in range(len(state_options)):
            for second in range(first + 1, len(state_options)):
                clauses.append([-state_options[first], -state_options[second]])

    for cell in range(width):
        symbol = word[cell] if cell < len(word) else machine.blank
        clauses.append([number(("cell", 0, cell, symbol))])

    clauses.append([number(("head", 0, 0))])
    clauses.append([number(("state", 0, machine.start))])

    for step in range(steps):
        for cell in range(width):
            for symbol in alphabet:
                clauses.append([number(("head", step, cell)),
                                -number(("cell", step, cell, symbol)),
                                number(("cell", step + 1, cell, symbol))])

        for cell in range(width):
            for state in states:
                for symbol in alphabet:
                    move = machine.transitions.get((state, symbol))
                    guard = [-number(("state", step, state)),
                             -number(("head", step, cell)),
                             -number(("cell", step, cell, symbol))]

                    if move is None:
                        clauses.append(guard + [number(("state", step + 1, state))])
                        clauses.append(guard + [number(("head", step + 1, cell))])
                        clauses.append(guard + [number(("cell", step + 1, cell, symbol))])
                        continue

                    target, written, direction = move
                    shift = {LEFT: -1, RIGHT: 1, STAY: 0}[direction]
                    landing = min(max(cell + shift, 0), width - 1)

                    clauses.append(guard + [number(("state", step + 1, target))])
                    clauses.append(guard + [number(("head", step + 1, landing))])
                    clauses.append(guard + [number(("cell", step + 1, cell, written))])

    clauses.append([number(("state", step, machine.accept)) for step in range(steps + 1)])

    return Encoding(clauses, names, steps, width)


def accepts_by_sat(machine, word, steps, solver=None):
    """Decide acceptance by solving the tableau formula instead of running the machine.

    The two must agree, and checking that they do on small inputs is the whole
    verification available for this construction: the theorem is about all
    machines, and a test is about these.
    """
    encoding = encode(machine, word, steps)
    solve = solver or problems.satisfiable_dpll
    assignment = solve(encoding.clauses)

    return assignment is not None, encoding, assignment


def size_report(machine, word, steps):
    """How big the formula gets, which is the polynomial the theorem promises."""
    encoding = encode(machine, word, steps)
    return {"steps": steps, "width": encoding.width,
            "variables": len(encoding.names), "clauses": len(encoding.clauses)}
