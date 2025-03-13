"""The monotone framework: one worklist algorithm, four analyses.

Reaching definitions, live variables, available expressions and very busy
expressions differ in four choices and nothing else:

- the direction, forward along ``flow`` or backward along ``flow_r``
- the lattice, sets ordered by inclusion
- the combination at a join, union for *may* analyses and intersection for
  *must* ones
- the transfer function per block, always ``(incoming \\ kill) | gen``

Writing the algorithm once and instantiating it four times is the point of the
framework: the correctness argument is made once, and each analysis is reduced
to its kill and gen sets.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "while-language"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "control-flow-graph"))

from control_flow_graph import ControlFlowGraph
from while_language import parse


@dataclass
class Analysis:
    """One instantiation of the framework.

    ``kill`` and ``gen`` take a block and return a set. ``initial`` is the value
    at the entry (or exit, for a backward analysis), and ``bottom`` is the
    starting value everywhere else.
    """

    name: str
    direction: str
    combine: str
    kill: object
    gen: object
    initial: object
    bottom: object


@dataclass
class Result:
    """Entry and exit sets per label, plus how many rounds it took."""

    entry: dict
    exit: dict
    iterations: int

    def table(self, order=None):
        """The result as text, one row per label."""
        rows = []
        for label in (order or sorted(self.entry)):
            rows.append(f"  {label}: entry {_show(self.entry[label])}  exit {_show(self.exit[label])}")
        return "\n".join(rows)


def _show(items):
    """A set in a stable order, so two runs print the same."""
    return "{" + ", ".join(str(item) for item in sorted(items, key=str)) + "}"


def solve(graph, analysis):
    """Run the analysis to its least fixed point with a worklist.

    Every label starts at ``bottom`` and is recomputed whenever one of its
    neighbours changes. The sets only grow for a *may* analysis and only shrink
    for a *must* one, and both are bounded, so the loop terminates: that is the
    ascending chain condition, and it is why the framework needs a lattice of
    finite height rather than any old set of values.

    A chaotic iteration over all labels would give the same answer. The
    worklist only avoids recomputing labels whose inputs did not change.
    """
    if not isinstance(graph, ControlFlowGraph):
        graph = ControlFlowGraph(parse(graph) if isinstance(graph, str) else graph)

    all_labels = set(graph.nodes)
    block_of = graph.blocks

    forward = analysis.direction == "forward"
    edges = set(graph.edges) if forward else {(b, a) for a, b in graph.edges}
    starts = {graph.entry} if forward else set(graph.exits)

    incoming = {label: set() for label in all_labels}
    for source, target in edges:
        incoming[target].add(source)

    entry = {label: set(analysis.initial) if label in starts else set(analysis.bottom)
             for label in all_labels}
    exit_sets = {label: set() for label in all_labels}

    for label in all_labels:
        exit_sets[label] = _transfer(entry[label], block_of[label], analysis)

    worklist = list(all_labels)
    iterations = 0

    while worklist:
        iterations += 1
        label = worklist.pop(0)

        if label in starts:
            new_entry = set(analysis.initial)
        elif not incoming[label]:
            new_entry = set(analysis.bottom)
        else:
            sources = [exit_sets[source] for source in incoming[label]]
            new_entry = set.union(*sources) if analysis.combine == "union" \
                else set.intersection(*sources)

        new_exit = _transfer(new_entry, block_of[label], analysis)

        if new_entry != entry[label] or new_exit != exit_sets[label]:
            entry[label] = new_entry
            exit_sets[label] = new_exit
            for source, target in edges:
                if source == label and target not in worklist:
                    worklist.append(target)

    if forward:
        return Result(entry, exit_sets, iterations)
    return Result(exit_sets, entry, iterations)


def _transfer(incoming, block, analysis):
    """The transfer function of a block: remove what it kills, add what it generates."""
    return (set(incoming) - set(analysis.kill(block))) | set(analysis.gen(block))
