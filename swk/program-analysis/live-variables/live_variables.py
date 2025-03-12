"""Live variables: which variables may still be read before being overwritten.

Backward and *may*. A variable is live at a point when some path from there
reads it before assigning to it. Dead assignments are the application: writing
to a variable that is not live afterwards is work no execution can observe,
which is what a compiler removes and what a linter reports.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "while-language"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "control-flow-graph"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "monotone-framework"))

from control_flow_graph import ControlFlowGraph
from monotone_framework import Analysis, solve
from while_language import parse


def kill(block):
    """An assignment kills the variable it writes."""
    return {block.variable} if block.kind == "assign" else set()


def gen(block):
    """A block generates every variable it reads.

    For an assignment that is the right-hand side only. The assigned variable
    itself is not read, which is exactly why the analysis can spot a write that
    nobody needs.
    """
    if block.kind == "assign":
        return set(block.expression.variables())
    if block.kind == "test":
        return set(block.expression.variables())
    return set()


def analyse(graph):
    """Run live variables on a program or a control flow graph.

    Backward, because liveness depends on what happens after a point, not
    before it. Joined with union, because a variable is live if **some**
    continuation reads it. Nothing is live at the end of the program.
    """
    if not isinstance(graph, ControlFlowGraph):
        graph = ControlFlowGraph(parse(graph) if isinstance(graph, str) else graph)

    analysis = Analysis(
        name="live variables",
        direction="backward",
        combine="union",
        kill=kill,
        gen=gen,
        initial=set(),
        bottom=set(),
    )
    return solve(graph, analysis)


def dead_assignments(graph):
    """Assignments whose variable is not live afterwards.

    The write can be removed without changing what the program computes, unless
    the right-hand side can fail or diverge, which in While it cannot.

    The result is a may-analysis read backwards, so it is safe in the direction
    that matters: an assignment reported here is genuinely unused, because the
    analysis over-approximates liveness and still found none.
    """
    if not isinstance(graph, ControlFlowGraph):
        graph = ControlFlowGraph(parse(graph) if isinstance(graph, str) else graph)

    result = analyse(graph)
    found = []

    for label in sorted(graph.nodes):
        block = graph.blocks[label]
        if block.kind == "assign" and block.variable not in result.exit[label]:
            found.append((label, block.variable))

    return found
