"""Boolean functions as truth vectors, and the two normal forms.

A function of `n` variables is a vector of `2^n` bits, and every such vector is
a function: there are `2^(2^n)` of them, which is why a five-variable function
already has more than four billion siblings.

The two canonical forms read the vector from opposite ends. The **disjunctive**
form lists the rows that are one, as conjunctions. The **conjunctive** form
lists the rows that are zero, as disjunctions of the negated literals. Both are
unique up to ordering, and both are usually far larger than necessary, which is
what [minimisation](../minimisation/) is for.
"""

from __future__ import annotations

import itertools


def truth_table(function, variables):
    """The truth vector of a Python function of the given arity."""
    return [int(bool(function(*[(index >> (variables - 1 - position)) & 1
                                for position in range(variables)])))
            for index in range(2 ** variables)]


def assignment_of(index, variables):
    """The assignment a row index denotes, most significant variable first."""
    bits = format(index, f"0{len(variables)}b")
    return {name: bit == "1" for name, bit in zip(variables, bits)}


def minterms(vector):
    """The row indices where the function is one."""
    return [index for index, value in enumerate(vector) if value]


def maxterms(vector):
    """The row indices where the function is zero."""
    return [index for index, value in enumerate(vector) if not value]


def minterm_text(index, variables):
    """One minterm as a conjunction of literals."""
    assignment = assignment_of(index, variables)
    return " ".join(name if assignment[name] else f"!{name}" for name in variables)


def maxterm_text(index, variables):
    """One maxterm as a disjunction of literals.

    The literals are negated relative to the minterm: a row that must be
    excluded contributes a clause that is false exactly on that row.
    """
    assignment = assignment_of(index, variables)
    return " | ".join(f"!{name}" if assignment[name] else name for name in variables)


def dnf(vector, variables):
    """The full disjunctive normal form, one term per one-row."""
    return [minterm_text(index, variables) for index in minterms(vector)]


def cnf(vector, variables):
    """The full conjunctive normal form, one clause per zero-row."""
    return [maxterm_text(index, variables) for index in maxterms(vector)]


def evaluate_dnf(terms, assignment):
    """Evaluate a disjunctive form under an assignment."""
    for term in terms:
        if all(_literal(literal, assignment) for literal in term.split()):
            return True
    return False


def evaluate_cnf(clauses, assignment):
    """Evaluate a conjunctive form under an assignment."""
    for clause in clauses:
        literals = [part.strip() for part in clause.split("|")]
        if not any(_literal(literal, assignment) for literal in literals):
            return False
    return True


def _literal(literal, assignment):
    """The value of one literal."""
    if literal.startswith("!"):
        return not assignment[literal[1:]]
    return assignment[literal]


def complement(vector):
    """The truth vector of the negated function."""
    return [1 - value for value in vector]


def compose(first, second, operator):
    """Combine two truth vectors pointwise."""
    if operator == "and":
        return [a & b for a, b in zip(first, second)]
    if operator == "or":
        return [a | b for a, b in zip(first, second)]
    if operator == "xor":
        return [a ^ b for a, b in zip(first, second)]
    raise ValueError(f"unknown operator {operator}")


def is_symmetric(vector, variables):
    """Whether the function depends only on how many inputs are one.

    A symmetric function has the same value on every row with the same number
    of ones, which makes it cheap to build from a counter and is why parity and
    majority get special hardware.
    """
    groups = {}
    for index, value in enumerate(vector):
        ones = bin(index).count("1")
        if ones in groups and groups[ones] != value:
            return False
        groups[ones] = value
    return True


def depends_on(vector, position, variables):
    """Whether the function's value ever changes with one variable.

    A variable the function ignores costs a wire and nothing else, and finding
    them is the first thing any minimiser does.
    """
    step = 2 ** (variables - 1 - position)
    for index in range(len(vector)):
        if index & step:
            continue
        if vector[index] != vector[index + step]:
            return True
    return False
