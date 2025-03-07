"""Available expressions: which expressions are already computed on every path.

Forward and *must*. An expression is available at a point when every path to
it has computed the expression and has not since changed any of its variables.
Common subexpression elimination is the application: an available expression
does not have to be evaluated again.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "while-language"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "control-flow-graph"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "monotone-framework"))

from control_flow_graph import ControlFlowGraph
from monotone_framework import Analysis, solve
from while_language import BinOp, Not, parse


ARITHMETIC = {"+", "-", "*", "/", "%"}


def subexpressions(expression):
    """Every non-trivial arithmetic subexpression of an expression.

    Variables and literals are excluded: they cost nothing to evaluate, so
    there is nothing to save by remembering them. Comparisons and boolean
    operators are excluded as well, and their operands are still collected:
    the classical analyses are defined over AExp, the arithmetic expressions,
    because those are the ones worth reusing. A test still contributes the
    arithmetic it computes.
    """
    if isinstance(expression, BinOp):
        inner = subexpressions(expression.left) | subexpressions(expression.right)
        return ({expression} | inner) if expression.op in ARITHMETIC else inner
    if isinstance(expression, Not):
        return subexpressions(expression.operand)
    return set()


def all_expressions(graph):
    """Every non-trivial expression occurring anywhere in the program.

    This is the universe of the lattice, and for a *must* analysis it is also
    the starting value at every label except the entry.
    """
    found = set()
    for block in graph.blocks.values():
        if block.expression is not None:
            found |= subexpressions(block.expression)
    return found


def kill(graph):
    """Return the kill function: an assignment invalidates what it changes.

    Assigning to x kills every expression containing x, everywhere in the
    program, because the value that was computed for it is now stale.
    """
    universe = all_expressions(graph)

    def kill_of(block):
        """The expressions this block invalidates by writing a variable."""
        if block.kind != "assign":
            return set()
        return {expression for expression in universe
                if block.variable in expression.variables()}

    return kill_of


def gen(block):
    """What a block computes, minus anything the same block invalidates.

    ``x := x + 1`` computes ``x + 1`` and then changes x, so the expression is
    not available afterwards. Subtracting the killed part here is what keeps
    that case right.
    """
    if block.expression is None:
        return set()

    generated = subexpressions(block.expression)
    if block.kind == "assign":
        generated = {expression for expression in generated
                     if block.variable not in expression.variables()}
    return generated


def analyse(graph):
    """Run available expressions on a program or a control flow graph.

    Forward and joined with intersection: an expression is available only if
    **every** path computed it. Nothing is available at the entry, and every
    other label starts from the full set, so the iteration shrinks to the
    greatest fixed point.

    Starting a *must* analysis at the empty set instead would be sound and
    useless: the result would stay empty, since intersection can only remove.
    """
    if not isinstance(graph, ControlFlowGraph):
        graph = ControlFlowGraph(parse(graph) if isinstance(graph, str) else graph)

    analysis = Analysis(
        name="available expressions",
        direction="forward",
        combine="intersection",
        kill=kill(graph),
        gen=gen,
        initial=set(),
        bottom=all_expressions(graph),
    )
    return solve(graph, analysis)


def redundant_computations(graph):
    """Expressions computed at a label although they were already available."""
    if not isinstance(graph, ControlFlowGraph):
        graph = ControlFlowGraph(parse(graph) if isinstance(graph, str) else graph)

    result = analyse(graph)
    found = []

    for label in sorted(graph.nodes):
        block = graph.blocks[label]
        if block.expression is None:
            continue
        for expression in sorted(subexpressions(block.expression), key=str):
            if expression in result.entry[label]:
                found.append((label, str(expression)))

    return found
