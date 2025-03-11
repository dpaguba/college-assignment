"""Cyclomatic complexity, measured on the control flow graph.

The lecture defines it as the number of independent paths through a program,
computed from the graph as

    CC = e - n + 2p

with e edges, n nodes and p connected components.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "control-flow-graph"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "while-language"))

from control_flow_graph import ControlFlowGraph, build
from while_language import parse


def cyclomatic_complexity(graph):
    """CC = e - n + 2p for the given control flow graph.

    The lecture's example, the factorial program, has six nodes and six edges
    in one component, so CC = 6 - 6 + 2 = 2: the loop is entered or it is not.

    The measure counts decisions, not statements. Straight-line code of any
    length has CC = 1, and every test adds one. That is why it is used as a
    testing budget: CC is a lower bound on the number of test cases needed for
    branch coverage.

    It also has a well known blind spot. A switch with twenty cases scores
    twenty and is easy to read; two nested loops with a flag score four and are
    not. The number measures branching, and branching is only one source of
    difficulty.
    """
    edges = len(graph.edges)
    nodes = len(graph.nodes)
    parts = len(graph.components())
    return edges - nodes + 2 * parts


def decision_count(graph):
    """The number of test blocks, which is CC - 1 for a structured program.

    Counting decisions is the other way the measure is usually stated, and on
    a While program the two agree. They part company on graphs that do not come
    from structured code, which is why the edge formula is the definition.
    """
    return sum(1 for block in graph.blocks.values() if block.kind == "test")


def independent_paths(graph, limit=1000):
    """Enumerate paths from the entry to an exit, each loop taken at most once.

    A basis of independent paths has exactly CC members, and this returns paths
    that cover every edge, which is the practical use: one test case per path.
    It is not the formal cycle basis, and for a program with many nested loops
    the count grows past CC.
    """
    found = []

    def walk(label, path, used_edges):
        """Enumerates paths through the graph, stopping at exits."""
        if label in graph.exits and not graph.successors(label) - set():
            pass
        targets = graph.successors(label)
        if not targets:
            found.append(list(path))
            return
        extended = False
        for target in sorted(targets):
            if (label, target) in used_edges:
                continue
            extended = True
            walk(target, path + [target], used_edges | {(label, target)})
            if len(found) >= limit:
                return
        if not extended:
            found.append(list(path))

    walk(graph.entry, [graph.entry], frozenset())
    return found


def report(source):
    """A one-line summary for a program given as source text."""
    graph = build(source)
    return (f"nodes {len(graph.nodes)}, edges {len(graph.edges)}, "
            f"components {len(graph.components())}, CC {cyclomatic_complexity(graph)}")
