"""DPLL: the satisfiability algorithm from the lecture, with its trace.

Davis, Putnam, Logemann and Loveland, 1962. Backtracking search over
assignments, sharpened by two observations that let whole subtrees be skipped:

- **unit clause**: a clause with one unassigned literal left has only one way
  to be satisfied, so that assignment is forced rather than guessed
- **pure literal**: an atom that occurs with one sign only can take that sign
  without ever hurting, so it needs no case split either

The worst case is still O(2^n), and the lecture's own example shows why it is
worth having anyway: three variables, eight possible assignments, and the
search tests one.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "propositional-logic"))

from propositional_logic import (Literal, cnf_atoms, clause, evaluate_clauses,
                                 to_tseitin)


@dataclass
class Trace:
    """The decisions the search made, in order."""

    steps: list = field(default_factory=list)

    def record(self, reason, name, value, depth):
        """Note one assignment, why it was made, and how deep the search was."""
        self.steps.append((depth, reason, name, value))

    def __str__(self):
        """The decisions and propagations, indented by depth."""
        return "\n".join(
            f"{'  ' * depth}{name} := {int(value)}   [{reason}]"
            for depth, reason, name, value in self.steps)


def simplify(clauses, assignment):
    """Drop satisfied clauses and falsified literals under a partial assignment.

    The two lines of the lecture's pseudocode that do the real work: a clause
    containing a true literal is gone, and a false literal is removed from the
    clauses that remain. An empty clause left behind means the branch is dead.
    """
    simplified = set()

    for one in clauses:
        remaining = set()
        satisfied = False

        for literal in one:
            if literal.name not in assignment:
                remaining.add(literal)
            elif literal.evaluate(assignment):
                satisfied = True
                break

        if not satisfied:
            simplified.add(frozenset(remaining))

    return simplified


def find_unit(clauses):
    """A literal that is alone in some clause, or None."""
    for one in clauses:
        if len(one) == 1:
            return next(iter(one))
    return None


def find_pure(clauses):
    """A literal whose atom occurs with one sign only, or None."""
    signs = {}
    for one in clauses:
        for literal in one:
            signs.setdefault(literal.name, set()).add(literal.positive)

    for name, seen in sorted(signs.items()):
        if len(seen) == 1:
            return Literal(name, next(iter(seen)))
    return None


def solve(clauses, trace=None):
    """Return a satisfying assignment, or None when the clauses are unsatisfiable.

    Follows the lecture's pseudocode exactly: simplify, check for the empty
    clause, check for the empty clause set, then unit, then pure, then split.

    The returned assignment may leave atoms unmentioned. Those are the ones the
    search never needed to decide, and any value works for them.
    """
    return _search(set(clauses), {}, trace, 0)


def _search(clauses, assignment, trace, depth):
    """The recursive search: propagate, choose, and try both values."""
    clauses = simplify(clauses, assignment)

    if frozenset() in clauses:
        return None
    if not clauses:
        return dict(assignment)

    unit = find_unit(clauses)
    if unit is not None:
        if trace is not None:
            trace.record("unit", unit.name, unit.positive, depth)
        return _search(clauses, {**assignment, unit.name: unit.positive}, trace, depth)

    pure = find_pure(clauses)
    if pure is not None:
        if trace is not None:
            trace.record("pure", pure.name, pure.positive, depth)
        return _search(clauses, {**assignment, pure.name: pure.positive}, trace, depth)

    name = sorted(cnf_atoms(clauses))[0]

    for value in (False, True):
        if trace is not None:
            trace.record("split", name, value, depth)
        found = _search(clauses, {**assignment, name: value}, trace, depth + 1)
        if found is not None:
            return found

    return None


def satisfiable(clauses):
    """True when some assignment satisfies every clause."""
    return solve(clauses) is not None


def check_model(clauses, assignment):
    """Verify that an assignment really satisfies the clauses.

    Cheap, and worth doing: a solver that says SAT is only useful if the model
    it hands back can be checked independently, which is the standard defence
    against a subtly wrong search.
    """
    if assignment is None:
        return False
    complete = {name: assignment.get(name, False) for name in cnf_atoms(clauses)}
    return evaluate_clauses(clauses, complete)


def entails(premise, conclusion):
    """Check ``premise |= conclusion`` with this solver.

    Wraps the negation trick from the logic folder: look for a model of
    ``premise and not conclusion``. When one exists it is returned as a
    counterexample.
    """
    from propositional_logic import And, Not
    model = solve(to_tseitin(And((premise, Not(conclusion)))))
    return model is None, model
