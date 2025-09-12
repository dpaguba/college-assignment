"""Removing assignments whose results are never read.

An assignment is dead when its target is not live immediately after it. Finding
them is one liveness analysis; removing them is the easy part. What makes this
worth its own module is that removal **changes the analysis**: an assignment
only kept alive by a dead one becomes dead in turn, so the process iterates.

The sheet's graph shows it in two rounds. `x = a+b` is dead because `x` is
overwritten before any use. Removing it takes away the only remaining use of
`a`, which makes `a = 1` dead as well.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "liveness-analysis"))
import liveness_analysis as la


def eliminate(graph, live_at_exit=None, limit=100):
    """Remove dead assignments until none is left, reporting each round.

    Each round runs the analysis afresh rather than updating it. That is
    wasteful and it is what makes the process obviously correct: the result is
    a fixed point of "no assignment is dead", not of an incremental update
    whose invariants would have to be argued.
    """
    current = graph
    removed = []
    rounds = 0

    while rounds < limit:
        live = la.live_variables(current, live_at_exit=live_at_exit)
        dead = la.dead_assignments(current, live)
        if not dead:
            break

        rounds += 1
        for edge, statement in dead:
            removed.append((edge, statement))
            current = current.without(edge)

    return {"graph": current, "removed": removed, "rounds": rounds}


def removable_variables(graph, live_at_exit=None):
    """Variables that disappear entirely once dead assignments are removed.

    A variable no longer assigned or used anywhere costs a register and a slot
    in every table the compiler keeps. Reporting them is how the saving from
    this optimisation is stated in something other than instruction counts.
    """
    before = graph.variables()
    after = eliminate(graph, live_at_exit)["graph"].variables()
    return before - after


def statement_count(graph):
    """How many edges still carry a statement rather than a skip."""
    return sum(1 for _, _, statement in graph.edges if statement.strip() != "skip")
