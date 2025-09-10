"""Available expressions: which computations do not need repeating.

An expression is **available** at a point when it has been computed on every
path to that point and none of its operands has changed since. Two identical
computations with an available expression between them are a common
subexpression, and the second one can be replaced by the first one's result.

The analysis is the mirror image of liveness in both axes: it runs **forwards**
and takes **intersections** at joins, because "on every path" is a must
property. That makes it the must-forward corner of the same monotone framework
that liveness sits in the may-backward corner of.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "liveness-analysis"))
import liveness_analysis as la


def expression_of(statement):
    """The right side of an assignment, if it is a compound expression.

    A copy `x = y` and a constant `x = 5` are not worth tracking: there is
    nothing to save by not recomputing them. Only expressions with an operator
    are candidates.
    """
    defined, _ = la.parse_statement(statement)
    if defined is None:
        return None

    right = statement.split("=", 1)[1].strip()
    if any(operator in right for operator in "+-*/"):
        return right
    return None


def all_expressions(graph):
    """Every compound expression the program computes."""
    found = set()
    for _, _, statement in graph.edges:
        expression = expression_of(statement)
        if expression:
            found.add(expression)
    return found


def transfer(statement, incoming, universe):
    """Add what the statement computes, remove what its assignment kills.

    Killing comes second, and it matters for a statement like `a = a+b`: the
    expression `a+b` is computed and then immediately invalidated, so it is not
    available afterwards. Adding after killing would wrongly claim it is.
    """
    defined, _ = la.parse_statement(statement)
    result = set(incoming)

    expression = expression_of(statement)
    if expression:
        result.add(expression)

    if defined:
        result = {candidate for candidate in result
                  if defined not in la._names(candidate)}

    return result


def available(graph):
    """Available expressions at every node, as a greatest fixed point.

    The initialisation is what distinguishes a must analysis: every node except
    the entry starts with **everything** available, and the iteration removes
    what cannot be justified. Starting from the empty set would compute the
    least fixed point, which for an intersection framework is the trivial one
    that says nothing is ever available.
    """
    universe = all_expressions(graph)
    result = {node: set(universe) for node in graph.nodes}
    result[graph.entry] = set()

    changed = True
    while changed:
        changed = False
        for node in sorted(graph.nodes):
            if node == graph.entry:
                continue

            incoming = graph.predecessors(node)
            if not incoming:
                continue

            intersection = None
            for source, statement in incoming:
                contribution = transfer(statement, result[source], universe)
                intersection = (contribution if intersection is None
                                else intersection & contribution)

            if intersection != result[node]:
                result[node] = intersection
                changed = True

    return result


def redundant(graph):
    """Assignments recomputing an expression that is already available.

    These are the ones common subexpression elimination replaces by a copy
    from wherever the value was first computed. The saving is real and the
    cost is a longer live range for the temporary, which is why an optimiser
    runs this together with register allocation rather than before it.
    """
    table = available(graph)
    found = []

    for source, target, statement in graph.edges:
        expression = expression_of(statement)
        if expression and expression in table[source]:
            found.append(((source, target), statement))

    return found


def very_busy(graph):
    """Expressions computed on every path forward, the must-backward analysis.

    The fourth corner of the framework, and the one behind code hoisting: an
    expression computed on every outgoing path can be computed once here
    instead, which shrinks the program even when it does not speed it up.
    """
    universe = all_expressions(graph)
    result = {node: set(universe) for node in graph.nodes}
    result[graph.exit] = set()

    changed = True
    while changed:
        changed = False
        for node in sorted(graph.nodes, reverse=True):
            if node == graph.exit:
                continue

            outgoing = graph.successors(node)
            if not outgoing:
                continue

            intersection = None
            for target, statement in outgoing:
                contribution = transfer(statement, result[target], universe)
                intersection = (contribution if intersection is None
                                else intersection & contribution)

            if intersection != result[node]:
                result[node] = intersection
                changed = True

    return result
