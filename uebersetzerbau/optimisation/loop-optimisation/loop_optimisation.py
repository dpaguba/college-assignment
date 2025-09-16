"""Loop optimisations: the three that pay for themselves.

Code inside a loop runs many times, so moving work out of it, or making each
iteration cheaper, is worth more than the same change anywhere else. Three
classic transformations, in increasing order of how much they need to know:

- **invariant code motion** moves a computation whose operands do not change
  inside the loop to just before it
- **induction variable recognition** finds variables stepping by a constant
- **strength reduction** replaces an expensive operation on an induction
  variable by a cheaper one

All three need to know where the loop is, which is what a natural loop is for.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "liveness-analysis"))
import liveness_analysis as la


def dominators(graph):
    """Which nodes every path from the entry must pass through, per node.

    Computed as the greatest fixed point of
    `dom(n) = {n} union intersection over predecessors of dom(p)`, with the
    entry dominating only itself and everything else starting as all nodes.
    """
    everything = set(graph.nodes)
    result = {node: set(everything) for node in graph.nodes}
    result[graph.entry] = {graph.entry}

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
            for source, _ in incoming:
                intersection = (set(result[source]) if intersection is None
                                else intersection & result[source])

            candidate = {node} | (intersection or set())
            if candidate != result[node]:
                result[node] = candidate
                changed = True

    return result


def back_edges(graph):
    """Edges going to a node that dominates their source.

    Reachability is the tempting shortcut and it is wrong: in a graph whose
    loop is reachable from the start, the target of **every** earlier edge can
    reach that edge's source through the loop, so the straight-line prefix
    would be reported as three extra loops. Dominance is what distinguishes
    "goes back to the top of a loop" from "is followed by a loop".
    """
    dominates = dominators(graph)
    return [(source, target) for source, target, _ in graph.edges
            if target in dominates[source]]


def natural_loops(graph):
    """The set of nodes belonging to each back edge's loop.

    The natural loop of a back edge from `n` to `h` is `h` together with every
    node that can reach `n` without going through `h`. That is what makes the
    loop a single-entry region, which every transformation below relies on: a
    computation moved before `h` runs exactly once per loop execution.
    """
    loops = []

    for source, header in back_edges(graph):
        body = {header, source}
        stack = [source]

        while stack:
            current = stack.pop()
            for predecessor, _ in graph.predecessors(current):
                if predecessor != header and predecessor not in body:
                    body.add(predecessor)
                    stack.append(predecessor)

        loops.append(body)

    return loops


def assigned_in(graph, body):
    """Variables assigned anywhere inside a loop body."""
    names = set()
    for source, target, statement in graph.edges:
        if source in body and target in body:
            defined, _ = la.parse_statement(statement)
            if defined:
                names.add(defined)
    return names


def invariant_statements(graph, body):
    """Assignments inside the loop whose operands never change inside it.

    The condition is conservative and cheap: every operand is assigned nowhere
    in the loop. A stronger version iterates, since a statement becomes
    invariant once the statements it depends on are hoisted, and that is what
    a real optimiser does.
    """
    changing = assigned_in(graph, body)
    found = []

    for source, target, statement in graph.edges:
        if source not in body or target not in body:
            continue
        defined, used = la.parse_statement(statement)
        if defined is None:
            continue
        if defined in used:
            continue
        if used & changing:
            continue
        found.append(((source, target), statement))

    return found


def hoist(graph, body):
    """Move invariant statements to just before the loop header.

    The statement is replaced by a skip inside the loop and inserted on the
    edge entering the header from outside. That edge is unique for a natural
    loop, which is exactly the property that makes the transformation safe.
    """
    invariant = invariant_statements(graph, body)
    if not invariant:
        return graph

    header = min(body)
    entering = [(source, target) for source, target, _ in graph.edges
                if target == header and source not in body]
    if not entering:
        return graph

    entry_edge = entering[0]
    edges = []
    moved = [statement for _, statement in invariant]

    for source, target, statement in graph.edges:
        if (source, target) == entry_edge:
            edges.append((source, target, moved[0]))
            continue
        if ((source, target), statement) in invariant:
            edges.append((source, target, "skip"))
            continue
        edges.append((source, target, statement))

    return la.Graph(edges, graph.entry, graph.exit)


def position_of(graph, statement):
    """The edge a statement sits on, for checking where a hoist put it."""
    for source, target, current in graph.edges:
        if current == statement:
            return (source, target)
    return None


def induction_variables(graph, body):
    """Variables updated by adding a constant on every loop iteration.

    The pattern `i = i + c` is what array indexing and loop counters look like
    after the front end, and recognising it is what allows the address
    arithmetic inside the loop to be turned into an addition per iteration
    rather than a multiplication.
    """
    found = set()

    for source, target, statement in graph.edges:
        if source not in body or target not in body:
            continue
        defined, used = la.parse_statement(statement)
        if defined is None or defined not in used:
            continue
        right = statement.split("=", 1)[1].strip()
        if any(f"{defined}{operator}" in right.replace(" ", "")
               for operator in ("+", "-")):
            found.add(defined)

    return found


def reduce_strength(statement):
    """Replace a multiplication by a small constant with repeated addition.

    Worth doing when a multiply costs more than an add, which was true of every
    processor the technique was invented for and is true again on small
    embedded cores. The cut-off is a judgement: four additions are cheaper than
    a multiplication on some machines and not on others, so anything above four
    is left alone here.
    """
    text = statement.replace(" ", "")
    if "=" not in text or "*" not in text:
        return statement

    target, right = text.split("=", 1)
    left, factor = right.split("*", 1)

    if not factor.isdigit():
        return statement

    count = int(factor)
    if count < 2 or count > 4:
        return statement

    return f"{target} = " + "+".join([left] * count)
