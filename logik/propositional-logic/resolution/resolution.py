"""Propositional resolution, with the proof it found.

One rule: two clauses containing complementary literals resolve to their union
minus that pair. Deriving the empty clause proves unsatisfiability, and the
sequence of resolution steps is the proof.

Resolution is **refutation complete**: it derives the empty clause from every
unsatisfiable clause set, and from no satisfiable one. It is not complete for
deriving arbitrary consequences, which is why every use of it starts by
negating what is to be proved.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "equivalence-transformations"))
import equivalence_transformations as eq


def negate(literal):
    """The complement of a literal."""
    return literal[1:] if literal.startswith("!") else "!" + literal


def satisfies(clause, assignment):
    """Whether an assignment makes a clause true."""
    for literal in clause:
        name = literal.lstrip("!")
        value = assignment.get(name, False)
        if literal.startswith("!") != value:
            return True
    return False


def clauses_from(texts):
    """Parse clauses written as disjunctions of literals."""
    result = []
    for text in texts:
        formula = eq.parse(text)
        result.extend(eq.clauses_of(eq.to_cnf(formula)))
    return result


def resolve(first, second, pivot):
    """The resolvent of two clauses on a pivot literal."""
    return (first - {pivot}) | (second - {negate(pivot)})


def refute(clauses, limit=2000):
    """Derive the empty clause, returning the proof, or `None`.

    Saturation: resolve every pair that can be resolved, add what is new,
    repeat. That is complete and wasteful, and every practical prover restricts
    it, which is what makes DPLL and CDCL in
    [swk/verification](../../../swk/verification/) different machines rather
    than optimisations of this one.

    A tautological resolvent, one containing a literal and its complement, is
    discarded: it is satisfied by every assignment, so it can never contribute
    to a refutation, and keeping it makes the saturation much larger.
    """
    known = [set(clause) for clause in clauses]
    proof = [{"rule": "given", "clause": set(clause), "parents": [], "pivot": None}
             for clause in known]

    for step in proof:
        if not step["clause"]:
            return proof

    seen = {frozenset(clause) for clause in known}
    added = True

    while added and len(known) < limit:
        added = False
        for i in range(len(known)):
            for j in range(i + 1, len(known)):
                for pivot in list(known[i]):
                    if negate(pivot) not in known[j]:
                        continue

                    resolvent = resolve(known[i], known[j], pivot)
                    if any(negate(literal) in resolvent for literal in resolvent):
                        continue
                    if frozenset(resolvent) in seen:
                        continue

                    known.append(resolvent)
                    seen.add(frozenset(resolvent))
                    proof.append({"rule": "resolution", "clause": resolvent,
                                  "parents": [known[i], known[j]], "pivot": pivot})
                    added = True

                    if not resolvent:
                        return proof

    return None


def entails(premises, conclusion):
    """Whether the premises entail a conclusion, by refuting its negation.

    The standard move, and the reason refutation completeness is enough: a set
    of premises entails a formula exactly when the premises together with the
    negated formula are unsatisfiable.
    """
    negated = eq.clauses_of(eq.to_cnf(eq.parse(f"!({conclusion})")))
    return refute(clauses_from(premises) + negated) is not None


def proof_length(proof):
    """How many resolution steps a proof used, excluding the given clauses."""
    return sum(1 for step in proof if step["rule"] == "resolution")


def render(proof):
    """The proof as numbered lines, in the form the sheets write."""
    lines = []
    numbers = {}

    for index, step in enumerate(proof, 1):
        text = "{" + ", ".join(sorted(step["clause"])) + "}" if step["clause"] else "[]"
        numbers[frozenset(step["clause"])] = index

        if step["rule"] == "given":
            lines.append(f"{index}. {text}  (given)")
        else:
            first = numbers.get(frozenset(step["parents"][0]), "?")
            second = numbers.get(frozenset(step["parents"][1]), "?")
            lines.append(f"{index}. {text}  (from {first}, {second} on {step['pivot']})")

    return lines
