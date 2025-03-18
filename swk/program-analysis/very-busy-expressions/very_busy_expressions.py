"""Very busy expressions: which expressions will certainly be computed next.

Backward and *must*. An expression is very busy at a point when every path
from there computes it before changing any of its variables. Code hoisting is
the application: a very busy expression can be moved up to the point where it
becomes busy, which saves the computation on all but one path.

It is the mirror image of available expressions, and the pair is the standard
way the four classical analyses are laid out: forward or backward, may or must.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "while-language"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "control-flow-graph"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "monotone-framework"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "available-expressions"))

from available_expressions import all_expressions, subexpressions
from control_flow_graph import ControlFlowGraph
from monotone_framework import Analysis, solve
from while_language import parse


def kill(graph):
    """Return the kill function: an assignment invalidates what it changes."""
    universe = all_expressions(graph)

    def kill_of(block):
        """The expressions this block invalidates by writing a variable."""
        if block.kind != "assign":
            return set()
        return {expression for expression in universe
                if block.variable in expression.variables()}

    return kill_of


def gen(block):
    """Every expression the block itself computes.

    Unlike available expressions, the assigned variable is not filtered out:
    the expression **is** evaluated here, before the assignment takes effect,
    which is all busyness claims.
    """
    if block.expression is None:
        return set()
    return subexpressions(block.expression)


def analyse(graph):
    """Run very busy expressions on a program or a control flow graph.

    Backward and joined with intersection. Nothing is busy at the end of the
    program, and every other label starts from the full set.
    """
    if not isinstance(graph, ControlFlowGraph):
        graph = ControlFlowGraph(parse(graph) if isinstance(graph, str) else graph)

    analysis = Analysis(
        name="very busy expressions",
        direction="backward",
        combine="intersection",
        kill=kill(graph),
        gen=gen,
        initial=set(),
        bottom=all_expressions(graph),
    )
    return solve(graph, analysis)


def hoistable(graph):
    """Expressions very busy at a label, so computable there once instead of later."""
    if not isinstance(graph, ControlFlowGraph):
        graph = ControlFlowGraph(parse(graph) if isinstance(graph, str) else graph)

    result = analyse(graph)
    return [(label, str(expression))
            for label in sorted(graph.nodes)
            for expression in sorted(result.entry[label], key=str)]
