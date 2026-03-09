"""Inductive invariants: the proof that covers all steps, not just the first k.

Bounded model checking can only ever say "no counterexample of length k". An
inductive invariant says "no counterexample of any length", and it costs two
entailment checks instead of one per depth:

    base:  I |= P
    step:  P and G |= P[s'/s]

If both hold, P is true in every reachable state by induction over the length
of the run. The catch is that most true properties are **not** inductive: the
step check starts from any state satisfying P, including unreachable ones, and
those can step outside P.

Strengthening is the answer, and it is where the work is: find a stronger Q
that implies P and is inductive.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "program-analysis" / "while-language"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "linear-arithmetic"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "transition-systems"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bounded-model-checking"))

import bounded_model_checking as bmc
import linear_arithmetic as arithmetic
from transition_systems import conjoin, prime, primed
from while_language import BinOp, Not, Var


@dataclass
class Report:
    """The outcome of the two checks, with the state that broke one of them."""

    base: bool
    step: bool
    base_counterexample: dict = None
    step_counterexample: dict = None

    @property
    def inductive(self):
        """True when both the base and the step hold."""
        return self.base and self.step

    def __str__(self):
        """Which of the two proof obligations failed, or that both hold."""
        if self.inductive:
            return "inductive: holds in every reachable state"
        if not self.base:
            return f"base fails: an initial state violates it, {self.base_counterexample}"
        return (f"step fails: not inductive, {self.step_counterexample} satisfies it "
                f"and its successor does not")


def base_check(system, invariant, domains=None):
    """Check ``I |= P``: every initial state satisfies the invariant."""
    domains = domains or system.domains()
    restricted = {name: domains[name] for name in system.variables}
    return arithmetic.entails(system.initial, invariant, restricted)


def step_check(system, invariant, domains=None):
    """Check ``P and G |= P'``: the invariant survives one transition.

    The state here is unconstrained apart from satisfying P. That is the whole
    difficulty: the check knows nothing about reachability, so it must hold
    even from states no execution ever produces.
    """
    domains = domains or system.domains()
    premise = conjoin(invariant, system.transition)
    return arithmetic.entails(premise, prime(invariant), domains)


def check(system, invariant, domains=None):
    """Run both checks and report."""
    base_ok, base_model = base_check(system, invariant, domains)
    step_ok, step_model = step_check(system, invariant, domains)
    return Report(base_ok, step_ok, base_model, step_model)


def is_inductive(system, invariant, domains=None):
    """True when the invariant passes both checks."""
    return check(system, invariant, domains).inductive


def strengthen(system, invariant, candidates, domains=None):
    """Search for extra conjuncts that make the invariant inductive.

    Tries the candidates in increasing combination size and returns the first
    conjunction that implies the original property and passes both checks.

    This is a toy version of what an industrial tool does automatically: IC3
    and PDR build such strengthenings themselves, one blocked counterexample at
    a time. The reason they are hard is visible here, in that the search space
    is the space of all formulas.
    """
    from itertools import combinations

    for size in range(1, len(candidates) + 1):
        for chosen in combinations(candidates, size):
            stronger = conjoin(invariant, *chosen)
            if check(system, stronger, domains).inductive:
                return stronger, chosen
    return None, None


def explain(system, invariant, domains=None, limit=8, low=-64, high=64):
    """Classify a property: inductive, true but not inductive, or false.

    The middle case is the interesting one, and it is what the lecture keeps
    returning to. A property can hold in every reachable state and still fail
    the step check, because the check starts from states that are not
    reachable. Bounded model checking is used here to tell the two apart:
    if no counterexample of bounded length exists but the step check fails, the
    property is at least plausible and needs strengthening.
    """
    report = check(system, invariant, domains)
    if report.inductive:
        return "inductive", report

    counterexample = bmc.check(system, invariant, limit=limit, low=low, high=high)
    if counterexample is not None:
        return "violated", counterexample
    return "true but not inductive", report
