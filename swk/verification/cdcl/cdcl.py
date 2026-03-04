"""CDCL: what modern SAT solvers do instead of plain backtracking.

DPLL backtracks one decision at a time and forgets everything it learned on
the way. Conflict-driven clause learning keeps three things that turn the same
search into the engine behind industrial verification:

- an **implication graph** recording why each assignment was forced
- a **learned clause** derived from every conflict, forbidding the cause rather
  than the symptom
- a **backjump** to the level where that clause becomes useful, which is often
  far above the last decision

The learned clause is the whole idea. A conflict deep in the tree usually has
a small explanation, and adding it as a clause stops the search from repeating
the same mistake anywhere else in the tree.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "propositional-logic"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dpll"))

from propositional_logic import Literal, cnf_atoms, evaluate_clauses


@dataclass
class Statistics:
    """What the search did, which is how solvers are compared in practice."""

    decisions: int = 0
    propagations: int = 0
    conflicts: int = 0
    learned: int = 0

    def __str__(self):
        """The four counters that describe one run."""
        return (f"decisions {self.decisions}, propagations {self.propagations}, "
                f"conflicts {self.conflicts}, learned clauses {self.learned}")


@dataclass
class _Assignment:
    """One assigned atom: its value, the level it was set at, and its reason."""

    value: bool
    level: int
    reason: frozenset = None


def solve(clauses, statistics=None):
    """Return a satisfying assignment, or None, using clause learning.

    The loop is: propagate everything forced, and if that produces a conflict,
    analyse it into a learned clause and jump back to where that clause is
    unit; otherwise decide a new atom.
    """
    clauses = [frozenset(one) for one in clauses]
    statistics = statistics if statistics is not None else Statistics()
    names = sorted(cnf_atoms(clauses))

    assignment = {}
    trail = []
    level = 0

    while True:
        conflict = _propagate(clauses, assignment, trail, level, statistics)

        if conflict is not None:
            statistics.conflicts += 1

            if level == 0:
                return None

            learned, backjump = _analyse(conflict, assignment, trail, level)
            clauses.append(learned)
            statistics.learned += 1

            while trail and assignment[trail[-1]].level > backjump:
                del assignment[trail.pop()]
            level = backjump
            continue

        unassigned = [name for name in names if name not in assignment]
        if not unassigned:
            return {name: entry.value for name, entry in assignment.items()}

        level += 1
        statistics.decisions += 1
        chosen = unassigned[0]
        assignment[chosen] = _Assignment(True, level)
        trail.append(chosen)


def _propagate(clauses, assignment, trail, level, statistics):
    """Assign every literal that is forced, returning a falsified clause or None."""
    changed = True

    while changed:
        changed = False

        for one in clauses:
            unassigned = []
            satisfied = False

            for literal in one:
                if literal.name not in assignment:
                    unassigned.append(literal)
                elif assignment[literal.name].value == literal.positive:
                    satisfied = True
                    break

            if satisfied:
                continue
            if not unassigned:
                return one
            if len(unassigned) == 1:
                literal = unassigned[0]
                assignment[literal.name] = _Assignment(literal.positive, level, one)
                trail.append(literal.name)
                statistics.propagations += 1
                changed = True

    return None


def _analyse(conflict, assignment, trail, level):
    """Derive a learned clause from a conflict, and the level to jump back to.

    Resolution against the reasons on the trail, stopping at the first unique
    implication point: the single literal from the current decision level that
    every path from the decision to the conflict passes through. The clause
    that results is asserting, meaning it becomes unit immediately after the
    backjump, so the search continues rather than repeating the decision.
    """
    learned = set(conflict)

    while True:
        at_level = [literal for literal in learned
                    if assignment[literal.name].level == level]
        if len(at_level) <= 1:
            break

        for name in reversed(trail):
            if any(literal.name == name for literal in at_level):
                reason = assignment[name].reason
                if reason is None:
                    break
                learned = (learned | set(reason)) - {Literal(name, True), Literal(name, False)}
                break
        else:
            break

    levels = sorted({assignment[literal.name].level for literal in learned}, reverse=True)
    backjump = levels[1] if len(levels) > 1 else 0
    return frozenset(learned), backjump


def satisfiable(clauses):
    """True when some assignment satisfies every clause."""
    return solve(clauses) is not None


def check_model(clauses, assignment):
    """Verify an assignment against the clauses, as an independent check."""
    if assignment is None:
        return False
    complete = {name: assignment.get(name, False) for name in cnf_atoms(clauses)}
    return evaluate_clauses(clauses, complete)


def pigeonhole(holes):
    """The pigeonhole clauses for holes+1 pigeons, a standard hard instance.

    Every resolution proof of unsatisfiability for this family is exponential
    in the number of holes, which is a theorem of Haken from 1985. It is the
    plain counterweight to the claim that clause learning makes SAT easy: on
    this family it does not, and the size of the search shows it.
    """
    pigeons = holes + 1
    clauses = []

    for pigeon in range(pigeons):
        clauses.append(frozenset(Literal(f"p{pigeon}h{hole}") for hole in range(holes)))

    for hole in range(holes):
        for first in range(pigeons):
            for second in range(first + 1, pigeons):
                clauses.append(frozenset({Literal(f"p{first}h{hole}", False),
                                          Literal(f"p{second}h{hole}", False)}))

    return clauses
