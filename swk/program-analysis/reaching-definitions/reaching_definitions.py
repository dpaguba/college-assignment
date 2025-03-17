"""Reaching definitions: which assignments can reach which statements.

The classical dataflow analysis, and the one the lecture works through in
full. A pair ``(x, l)`` means "the assignment at label l can still be the last
one to have written x here"; the pair ``(x, ?)`` means "x may still be
uninitialised here".

That second kind is what makes the analysis useful: a variable read at a label
whose entry set contains ``(x, ?)`` may be read before it is ever written.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "while-language"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "control-flow-graph"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "monotone-framework"))

from control_flow_graph import ControlFlowGraph
from monotone_framework import Analysis, Result, solve
from while_language import parse

UNINITIALISED = "?"


def kill(graph):
    """Return the kill function: what an assignment invalidates.

    Assigning to x kills every pair for x, including ``(x, ?)``: after the
    assignment the variable is certainly initialised and certainly holds the
    value written here. Tests and skips kill nothing.

    The kill set needs the whole program, since it names every other label that
    assigns to the same variable, which is why this is a closure over the graph
    rather than a function of the block alone.
    """
    writers = {}
    for block in graph.blocks.values():
        if block.kind == "assign":
            writers.setdefault(block.variable, set()).add(block.label)

    def kill_of(block):
        """The definitions this block overwrites."""
        if block.kind != "assign":
            return set()
        return {(block.variable, UNINITIALISED)} | {
            (block.variable, label) for label in writers[block.variable]}

    return kill_of


def gen(block):
    """What a block generates: an assignment generates its own definition."""
    if block.kind == "assign":
        return {(block.variable, block.label)}
    return set()


def analyse(graph):
    """Run reaching definitions on a program or a control flow graph.

    Forward, and a *may* analysis: the sets are joined with union, because a
    definition reaches a label if it reaches it along **some** path. The
    analysis over-approximates, ignoring which branch a test would actually
    take, which is what keeps it decidable.
    """
    if not isinstance(graph, ControlFlowGraph):
        graph = ControlFlowGraph(parse(graph) if isinstance(graph, str) else graph)

    variables = set()
    for block in graph.blocks.values():
        variables |= set(block.variables())

    analysis = Analysis(
        name="reaching definitions",
        direction="forward",
        combine="union",
        kill=kill(graph),
        gen=gen,
        initial={(name, UNINITIALISED) for name in variables},
        bottom=set(),
    )
    return solve(graph, analysis)


def possibly_uninitialised(graph):
    """Labels that read a variable which may not have been written yet.

    This is the application the lecture names. A read of x at label l is
    suspicious when ``(x, ?)`` is in the entry set of l, and the analysis
    over-approximates, so a report may be spurious: the path that leaves x
    unwritten might never be taken. It never misses a real one.
    """
    if not isinstance(graph, ControlFlowGraph):
        graph = ControlFlowGraph(parse(graph) if isinstance(graph, str) else graph)

    result = analyse(graph)
    found = []

    for label in sorted(graph.nodes):
        block = graph.blocks[label]
        read = block.expression.variables() if block.expression is not None else frozenset()
        for name in sorted(read):
            if (name, UNINITIALISED) in result.entry[label]:
                found.append((label, name))

    return found
