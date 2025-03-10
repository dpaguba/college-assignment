"""The control flow graph of a While program, built from the flow relation.

The lecture defines the CFG of a program S as the graph (V, E) with
V = labels(S) and E = flow(S). That is all this module does, plus the
bookkeeping every analysis wants: predecessors, successors, reachability, and
an export that can be drawn.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "while-language"))

from while_language import blocks, final, flow, init, labels, parse


class ControlFlowGraph:
    """Nodes are labels, edges are the control flow relation."""

    def __init__(self, program):
        """Builds the graph from the blocks and the flow of the program."""
        self.program = program
        self.blocks = blocks(program)
        self.nodes = set(labels(program))
        self.edges = set(flow(program))
        self.entry = init(program)
        self.exits = set(final(program))

        self._index()

    @classmethod
    def from_parts(cls, block_list, edges, entry, exits):
        """Build a graph directly, for a CFG given as a picture rather than as code.

        The exercise sheets sometimes draw a control flow graph without the
        program behind it. The analyses run on the graph, so they do not care
        which of the two the graph came from.
        """
        graph = cls.__new__(cls)
        graph.program = None
        graph.blocks = {block.label: block for block in block_list}
        graph.nodes = set(graph.blocks)
        graph.edges = set(edges)
        graph.entry = entry
        graph.exits = set(exits)
        graph._index()
        return graph

    def _index(self):

        """Indexes the edges in both directions, so either can be read directly."""
        self._successors = {label: set() for label in self.nodes}
        self._predecessors = {label: set() for label in self.nodes}
        for source, target in self.edges:
            self._successors[source].add(target)
            self._predecessors[target].add(source)

    def successors(self, label):
        """Labels that can run immediately after this one."""
        return set(self._successors[label])

    def predecessors(self, label):
        """Labels that can run immediately before this one."""
        return set(self._predecessors[label])

    def block(self, label):
        """The elementary block carrying this label."""
        return self.blocks[label]

    def reachable(self):
        """Every label reachable from the entry, by breadth-first search.

        A label outside this set is dead code: no execution can arrive there,
        which is one of the properties the lecture names as a target for static
        analysis.
        """
        seen = {self.entry}
        queue = [self.entry]
        while queue:
            current = queue.pop()
            for target in self._successors[current]:
                if target not in seen:
                    seen.add(target)
                    queue.append(target)
        return seen

    def unreachable(self):
        """Labels that no execution can reach."""
        return self.nodes - self.reachable()

    def components(self):
        """Connected components of the underlying undirected graph.

        This is the p of the cyclomatic complexity formula. A While program
        parsed as one statement always has p = 1; the count matters when
        several procedures are measured as one graph, which the lecture
        mentions for a Java class.
        """
        neighbours = {label: set() for label in self.nodes}
        for source, target in self.edges:
            neighbours[source].add(target)
            neighbours[target].add(source)

        unvisited = set(self.nodes)
        found = []
        while unvisited:
            start = unvisited.pop()
            component = {start}
            queue = [start]
            while queue:
                current = queue.pop()
                for other in neighbours[current]:
                    if other not in component:
                        component.add(other)
                        unvisited.discard(other)
                        queue.append(other)
            found.append(component)
        return found

    def to_dot(self):
        """The graph in Graphviz format, with each node labelled by its block."""
        lines = ["digraph cfg {", "  rankdir=TB;", '  node [shape=box];']
        for label in sorted(self.nodes):
            text = str(self.blocks[label]).replace('"', r"\"")
            shape = "diamond" if self.blocks[label].kind == "test" else "box"
            lines.append(f'  {label} [label="{text}", shape={shape}];')
        for source, target in sorted(self.edges):
            lines.append(f"  {source} -> {target};")
        lines.append("}")
        return "\n".join(lines)

    def __str__(self):
        """The graph as an edge list, one line per node."""
        rows = [f"entry: {self.entry}, exits: {sorted(self.exits)}"]
        for label in sorted(self.nodes):
            targets = sorted(self._successors[label])
            rows.append(f"  {self.blocks[label]} -> {targets if targets else 'exit'}")
        return "\n".join(rows)


def build(source):
    """Parse a program and return its control flow graph."""
    return ControlFlowGraph(parse(source) if isinstance(source, str) else source)
