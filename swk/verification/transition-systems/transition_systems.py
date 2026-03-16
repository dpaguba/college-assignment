"""Transition systems: the model everything in this folder is verified against.

The lecture arrives here by simplification. A component has state, inputs and
outputs; a component composed with a driver that feeds it inputs and a monitor
that watches its outputs has neither, and what is left is a triple

    T = <s, I, G>

with ``s`` a set of typed variables, ``I`` a formula over ``s`` describing the
initial states, and ``G`` a formula over ``s`` and the primed copy ``s'``
describing the transition relation.

The state space is generally infinite, which is the reason the verification is
bounded, symbolic, or inductive rather than an exhaustive walk.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "program-analysis" / "while-language"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "linear-arithmetic"))

import linear_arithmetic as arithmetic
from while_language import BinOp, Bool, Not, Num, Var

PRIME = "'"


def primed(name):
    """The name of a variable in the successor state."""
    return name + PRIME


def prime(expression):
    """Replace every variable in an expression by its primed copy."""
    return rename(expression, lambda name: primed(name))


def rename(expression, mapping):
    """Rewrite every variable name in an expression through a function."""
    if isinstance(expression, Var):
        return Var(mapping(expression.name))
    if isinstance(expression, (Num, Bool)):
        return expression
    if isinstance(expression, Not):
        return Not(rename(expression.operand, mapping))
    if isinstance(expression, BinOp):
        return BinOp(expression.op,
                     rename(expression.left, mapping),
                     rename(expression.right, mapping))
    raise TypeError(f"cannot rename inside {expression!r}")


def conjoin(*parts):
    """Fold any number of formulas into one conjunction."""
    parts = [part for part in parts if part is not None]
    if not parts:
        return Bool(True)
    result = parts[0]
    for part in parts[1:]:
        result = BinOp("&&", result, part)
    return result


def disjoin(*parts):
    """Fold any number of formulas into one disjunction."""
    parts = [part for part in parts if part is not None]
    if not parts:
        return Bool(False)
    result = parts[0]
    for part in parts[1:]:
        result = BinOp("||", result, part)
    return result


@dataclass
class TransitionSystem:
    """A triple of state variables, an initial condition, and a transition relation.

    ``transition`` mentions both ``x`` and ``x'`` for each state variable, the
    unprimed name meaning the value now and the primed one the value in the
    successor state.
    """

    variables: tuple
    initial: object
    transition: object
    name: str = "T"

    def domains(self, low=-64, high=64):
        """Finite domains for the state and its primed copy.

        Bounds are not part of the model. They are what makes the solver
        terminate, and every answer computed with them is an answer about the
        states inside them.
        """
        bounds = arithmetic.Domain(low, high)
        return {name: bounds for variable in self.variables
                for name in (variable, primed(variable))}

    def initial_states(self, domains=None):
        """Every state satisfying the initial condition, inside the domains."""
        domains = domains or self.domains()
        restricted = {name: domains[name] for name in self.variables}
        return arithmetic.search(self.initial, restricted, all_models=True)

    def successors(self, state, domains=None):
        """Every successor of a state, inside the domains.

        Solves the transition relation with the current state fixed. A
        deterministic system returns one successor, a non-deterministic one
        returns several, and a stuck state returns none.
        """
        domains = domains or self.domains()
        fixed = conjoin(self.transition,
                        *[BinOp("=", Var(name), Num(state[name])) for name in self.variables])
        restricted = {name: domains[name] for name in self.variables + tuple(
            primed(variable) for variable in self.variables)}

        found = arithmetic.search(fixed, restricted, all_models=True)
        return [{variable: model[primed(variable)] for variable in self.variables}
                for model in found]

    def run(self, state, steps, domains=None):
        """Follow one path of the given length, taking the first successor each time.

        Enough for a deterministic system, which is what the driver and monitor
        construction produces, and a demonstration rather than a proof for any
        other.
        """
        path = [dict(state)]
        for _ in range(steps):
            following = self.successors(path[-1], domains)
            if not following:
                break
            path.append(following[0])
        return path

    def holds(self, state, property_):
        """Whether a property holds in a concrete state."""
        return bool(property_.evaluate(state))


@dataclass
class Component:
    """A named piece of a system: its own state, inputs, outputs, and update.

    Composition is conjunction. Two components running side by side are one
    system whose transition relation is the conjunction of theirs, with shared
    names connecting an output of one to an input of the other. That is the
    whole formalism, and it is why a driver and a monitor need no special
    treatment: they are components too.
    """

    name: str
    variables: tuple
    initial: object
    transition: object


def compose(*components, name="composed"):
    """Combine components into one transition system.

    Names are shared, not renamed: a variable written by one component and read
    by another is the same variable, which is how the wiring is expressed.
    """
    variables = []
    for component in components:
        for variable in component.variables:
            if variable not in variables:
                variables.append(variable)

    return TransitionSystem(
        variables=tuple(variables),
        initial=conjoin(*[component.initial for component in components]),
        transition=conjoin(*[component.transition for component in components]),
        name=name,
    )
