"""Structural operational semantics for While, with the derivation trace.

The lecture gives seven rules. Two are axioms that finish a statement and turn
a configuration into a state (SKIP, ASS), two pick a branch (IF_T, IF_F), two
unroll a loop once (WH_T, WH_F), and two propagate a step through a sequence
(COMP_1, COMP_2).

A configuration is a statement together with a state. A step either produces
another configuration, when something is left to run, or a state, when nothing
is.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "while-language"))

from while_language import Assign, If, Seq, Skip, While, parse


@dataclass(frozen=True)
class Step:
    """One rule application: the configuration before, after, and the rule used."""

    rule: str
    before: str
    after: str

    def __str__(self):
        """One step, with the rule that justified it."""
        return f"{self.before}  =>  {self.after}   [{self.rule}]"


def step(statement, state):
    """Apply exactly one rule and return (rule name, rest, state).

    ``rest`` is None when the rule produced a state rather than a
    configuration, which is how the axioms are distinguished from the rules in
    the lecture: after SKIP, ASS and WH_F nothing is left to run.

    The composition rules are where the recursion happens. COMP_1 fires when
    the first statement itself stepped to another configuration, COMP_2 when
    the first statement finished. That is the whole of sequencing: there is no
    separate rule for what a sequence means.
    """
    if isinstance(statement, Skip):
        return "SKIP", None, state

    if isinstance(statement, Assign):
        value = statement.expression.evaluate(state)
        return "ASS", None, {**state, statement.variable: value}

    if isinstance(statement, If):
        if statement.condition.evaluate(state):
            return "IF_T", statement.then_branch, state
        return "IF_F", statement.else_branch, state

    if isinstance(statement, While):
        if statement.condition.evaluate(state):
            return "WH_T", Seq(statement.body, statement), state
        return "WH_F", None, state

    if isinstance(statement, Seq):
        rule, rest, new_state = step(statement.first, state)
        if rest is None:
            return f"COMP_2 + {rule}", statement.second, new_state
        return f"COMP_1 + {rule}", Seq(rest, statement.second), new_state

    raise TypeError(f"not a While statement: {statement!r}")


def trace(statement, state, limit=10000):
    """Run the program one rule at a time and record every step.

    This is the derivation the exam asks to be written out by hand. Each line
    names the rule and shows the configuration before and after it.
    """
    steps = []
    current = statement
    current_state = dict(state)

    while current is not None:
        before = f"<{current}, {_show(current_state)}>"
        rule, rest, current_state = step(current, current_state)
        after = (f"<{rest}, {_show(current_state)}>" if rest is not None
                 else _show(current_state))
        steps.append(Step(rule, before, after))
        current = rest

        if len(steps) > limit:
            raise RuntimeError("the program did not terminate within the step limit")

    return steps, current_state


def execute(statement, state, limit=100000):
    """Run the program to completion and return the final state.

    Non-termination is real here: ``while [true]1 do [skip]2`` never finishes,
    and no analysis in this folder can decide in general whether it will. The
    step limit turns that into an exception instead of a hang.
    """
    current = statement
    current_state = dict(state)
    steps = 0

    while current is not None:
        _, current, current_state = step(current, current_state)
        steps += 1
        if steps > limit:
            raise RuntimeError("the program did not terminate within the step limit")

    return current_state


def _show(state):
    """The state as a mapping, sorted so traces compare."""
    return "{" + ", ".join(f"{name} -> {value}" for name, value in sorted(state.items())) + "}"


def run(source, state):
    """Parse and execute, for callers holding the program as text."""
    return execute(parse(source), state)
