"""Bounded model checking: unroll the system k steps and ask a solver.

Model checking explores the states of a system to decide whether a property
holds. The state space here is infinite, so a complete exploration is out.
Bounded model checking gives up completeness on purpose and asks a smaller
question that a solver can answer:

    is there an execution of at most k steps that breaks the property?

The lecture writes k-safety as an entailment,

    I[s0] and G(0,1) and ... and G(k-1,k)  |=  P0 and ... and Pk

and then tests it the only way an entailment is ever tested: by searching for
a model of the negation. A model found is a counterexample, step by step, and
that is what makes the technique useful even though it proves nothing about
longer runs.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "program-analysis" / "while-language"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "linear-arithmetic"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "transition-systems"))

import linear_arithmetic as arithmetic
from transition_systems import PRIME, conjoin, disjoin, rename
from while_language import BinOp, Not, Var


def at(expression, step):
    """Rename an unprimed formula into the copy of the state at a given step."""
    return rename(expression, lambda name: f"{name}@{step}")


def transition_at(transition, step):
    """Rename a transition formula into the step from one state copy to the next.

    Unprimed names become the copy at ``step`` and primed names the copy at
    ``step + 1``. This is the lecture's ``G(i,j) = G[si/s][sj/s']`` written out.
    """
    def mapping(name):
        """The name of a variable at this step, primed names meaning the next one."""
        if name.endswith(PRIME):
            return f"{name[:-len(PRIME)]}@{step + 1}"
        return f"{name}@{step}"

    return rename(transition, mapping)


@dataclass
class Counterexample:
    """A concrete execution that violates the property, with the step it fails at."""

    trace: list
    step: int

    def __str__(self):
        """The trace, marking the step where the property fails."""
        rows = []
        for index, state in enumerate(self.trace):
            marker = "  <- violated here" if index == self.step else ""
            values = ", ".join(f"{name}={value}" for name, value in sorted(state.items()))
            rows.append(f"  step {index}: {values}{marker}")
        return "\n".join(rows)


def unrolling(system, steps):
    """The formula for k steps of the system: the initial state and every transition."""
    parts = [at(system.initial, 0)]
    for step in range(steps):
        parts.append(transition_at(system.transition, step))
    return conjoin(*parts)


def k_safety_test(system, property_, steps):
    """The formula whose models are counterexamples of length at most k.

    The unrolling conjoined with the negation of the property at some step.
    The lecture writes the disjunction of negations explicitly, and it is what
    makes one solver call cover every step rather than k separate calls.
    """
    violations = disjoin(*[Not(at(property_, step)) for step in range(steps + 1)])
    return conjoin(unrolling(system, steps), violations)


def domains_for(system, steps, low=-64, high=64):
    """Finite domains for every state copy the unrolling mentions."""
    bounds = arithmetic.Domain(low, high)
    return {f"{variable}@{step}": bounds
            for variable in system.variables
            for step in range(steps + 1)}


def is_k_safe(system, property_, steps, domains=None):
    """Check k-safety and return the counterexample when it fails."""
    domains = domains or domains_for(system, steps)
    model = arithmetic.search(k_safety_test(system, property_, steps), domains)

    if model is None:
        return True, None

    trace = [{variable: model[f"{variable}@{step}"] for variable in system.variables}
             for step in range(steps + 1)]
    failing = next(step for step, state in enumerate(trace)
                   if not property_.evaluate(state))
    return False, Counterexample(trace, failing)


def check(system, property_, limit=10, domains=None, low=-64, high=64):
    """Increase k until a counterexample turns up or the limit is reached.

    This is the algorithm as the lecture states it: start at k = 0, test, and
    on failure report the model as a counterexample; otherwise increase k and
    repeat.

    Reaching the limit proves nothing about the system, only about executions
    of that length. The set of states reachable in i steps grows with i, and
    there is no formula available that says when it has stopped growing, which
    is exactly the gap that inductive invariants fill.
    """
    for steps in range(limit + 1):
        safe, counterexample = is_k_safe(
            system, property_, steps,
            domains or domains_for(system, steps, low, high))
        if not safe:
            return counterexample
    return None
