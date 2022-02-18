"""Horn formulas: the fragment where satisfiability is easy.

A Horn clause has at most one positive literal, so it reads as an implication
with a conjunction of conditions and a single conclusion. Satisfiability for
Horn formulas is decidable in linear time by a marking algorithm, while the
general problem is NP-complete.

The algorithm is one paragraph. Mark every variable forced true by a clause
with no negative literals, repeat for clauses whose negative literals are all
marked, and stop when a clause with no positive literal has all its conditions
marked, which means unsatisfiable.

That the marked set is not merely **a** model but the **smallest** one is what
makes the fragment useful beyond the decision: it is the semantics of a Prolog
program, and it is why a logic program has a well-defined answer at all.
"""

from __future__ import annotations


def is_horn(clauses):
    """Whether every clause has at most one positive literal."""
    return all(sum(1 for literal in clause if not literal.startswith("!")) <= 1
               for clause in clauses)


def _positive(clause):
    """The positive literal of a Horn clause, or `None`."""
    for literal in clause:
        if not literal.startswith("!"):
            return literal
    return None


def _conditions(clause):
    """The variables appearing negatively, which are the clause's conditions."""
    return {literal[1:] for literal in clause if literal.startswith("!")}


def trace(clauses):
    """Every round of the marking algorithm, with what it marked and why.

    The rounds are worth reporting because the bound is what makes the
    algorithm interesting: each round marks at least one new variable, so
    there are at most as many rounds as variables, and each round is one scan
    of the clauses.
    """
    if not is_horn(clauses):
        raise ValueError("the marking algorithm only applies to Horn formulas")

    marked = set()
    steps = [{"marked": set(), "reason": "start"}]

    while True:
        for clause in clauses:
            head = _positive(clause)
            if head is None or head in marked:
                continue
            if _conditions(clause) <= marked:
                marked.add(head)
                steps.append({"marked": set(marked), "reason": sorted(clause)})
                break
        else:
            return steps


def satisfiable(clauses):
    """Whether a Horn formula is satisfiable.

    Unsatisfiable exactly when some clause with no positive literal has all its
    conditions marked. Everything else is satisfied by the marked set, which is
    why one pass after the marking finishes decides it.
    """
    marked = minimal_model(clauses)

    for clause in clauses:
        if _positive(clause) is None and _conditions(clause) <= marked:
            return False

    return True


def minimal_model(clauses):
    """The set of variables the marking algorithm marks.

    Contained in every model, which is what "minimal" means here: a variable is
    marked only when some clause forces it, so any model must contain it too.
    A general propositional formula has no such canonical model, and that is
    precisely what the Horn restriction buys.
    """
    return trace(clauses)[-1]["marked"]


def as_implications(clauses):
    """The clauses written as implications, which is how they are read.

    `{!A, !B, C}` is `A and B -> C`, `{C}` is `-> C` a fact, and `{!A, !B}` is
    `A and B -> false` a goal. Seeing the three shapes side by side is what
    makes the connection to Prolog obvious: facts, rules and a query.
    """
    result = []

    for clause in clauses:
        head = _positive(clause)
        conditions = sorted(_conditions(clause))
        body = " and ".join(conditions) if conditions else "true"
        result.append(f"{body} -> {head if head else 'false'}")

    return result
