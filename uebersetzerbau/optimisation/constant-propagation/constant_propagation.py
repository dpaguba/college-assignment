"""Constant propagation over a lattice.

If a variable holds the same known value on every path to a point, its uses
there can be replaced by that value, and expressions built from constants can
be folded at compile time.

The values form a three-level lattice: `UNDEFINED` at the top for "no path
reaches here yet", the constants in the middle, and `UNKNOWN` at the bottom for
"different paths disagree". The meet operation is what joins do, and its shape
is the entire analysis:

    meet(c, c) = c          agreeing paths keep the constant
    meet(c, d) = UNKNOWN    disagreeing paths lose it
    meet(c, UNDEFINED) = c  an unreached path contributes nothing

The lattice has finite height, which is why the iteration terminates: a
variable can only move down twice.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "liveness-analysis"))
import liveness_analysis as la

UNDEFINED = "undefined"
"""Top of the lattice: no path has reached this point yet."""

UNKNOWN = "unknown"
"""Bottom of the lattice: paths disagree, so nothing can be assumed."""


def meet(first, second):
    """Combine two lattice values at a join."""
    if first == UNDEFINED:
        return second
    if second == UNDEFINED:
        return first
    if first == UNKNOWN or second == UNKNOWN:
        return UNKNOWN
    return first if first == second else UNKNOWN


def evaluate(expression, values):
    """Evaluate an expression under a lattice environment, or return UNKNOWN.

    Any unknown operand makes the result unknown. That is a deliberate
    over-approximation: `x - x` is zero whatever `x` is, and this analysis will
    not say so, because tracking that needs a relational domain rather than one
    value per variable.
    """
    text = expression.strip()

    if text.lstrip("-").isdigit():
        return int(text)
    if text in values:
        return values[text]

    for operator in ("+", "-", "*", "/"):
        if operator in text:
            left, right = text.split(operator, 1)
            first = evaluate(left, values)
            second = evaluate(right, values)
            if first in (UNKNOWN, UNDEFINED) or second in (UNKNOWN, UNDEFINED):
                return UNKNOWN
            if operator == "+":
                return first + second
            if operator == "-":
                return first - second
            if operator == "*":
                return first * second
            return UNKNOWN if second == 0 else first // second

    return UNKNOWN


def transfer(statement, incoming):
    """Update the environment across one statement."""
    defined, _ = la.parse_statement(statement)
    result = dict(incoming)

    if defined:
        right = statement.split("=", 1)[1]
        result[defined] = evaluate(right, incoming)

    return result


def propagate(graph):
    """Constant values at every node, as a forwards fixed point over the lattice."""
    variables = graph.variables()
    values = {node: {name: UNDEFINED for name in variables} for node in graph.nodes}

    changed = True
    while changed:
        changed = False
        for node in sorted(graph.nodes):
            incoming = graph.predecessors(node)
            if not incoming:
                continue

            combined = {name: UNDEFINED for name in variables}
            for source, statement in incoming:
                contribution = transfer(statement, values[source])
                for name in variables:
                    combined[name] = meet(combined[name], contribution.get(name, UNDEFINED))

            if combined != values[node]:
                values[node] = combined
                changed = True

    return values


def fold(graph):
    """Rewrite statements whose right side is a known constant.

    The payoff of the analysis, and the reason it is worth running before code
    generation: a folded statement needs no arithmetic instruction at all, and
    the constant it produces may enable further folding downstream.
    """
    values = propagate(graph)
    edges = []

    for source, target, statement in graph.edges:
        defined, _ = la.parse_statement(statement)
        if defined:
            right = statement.split("=", 1)[1]
            result = evaluate(right, values[source])
            if result not in (UNKNOWN, UNDEFINED):
                edges.append((source, target, f"{defined} = {result}"))
                continue
        edges.append((source, target, statement))

    return la.Graph(edges, graph.entry, graph.exit)
