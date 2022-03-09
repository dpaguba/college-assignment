"""Propositions, truth tables, and the two rules that look alike.

The lecture opens with implication, because it is the connective whose truth
table students argue with: a false premise makes the implication true,
whatever the conclusion says. Everything else in the chapter follows from
reading the tables rather than from intuition, and that is what the functions
here make checkable.
"""

import inspect
import itertools


def arity(formula):
    """How many propositional variables the formula takes."""
    return len(inspect.signature(formula).parameters)


def truth_table(formula):
    """Every assignment paired with the value the formula takes."""
    rows = []
    for assignment in itertools.product([False, True], repeat=arity(formula)):
        rows.append((assignment, bool(formula(*assignment))))
    return rows


def is_tautology(formula):
    """Whether the formula holds under every assignment."""
    return all(value for _, value in truth_table(formula))


def is_satisfiable(formula):
    """Whether some assignment makes it true."""
    return any(value for _, value in truth_table(formula))


def equivalent(first, second):
    """Whether two formulas of the same arity agree everywhere."""
    return truth_table(first) == truth_table(second)


def implies(premise, conclusion):
    """Material implication, false only for a true premise and a false conclusion."""
    return (not premise) or conclusion


def equivalence(left, right):
    """Both implications at once."""
    return implies(left, right) and implies(right, left)


def for_all(universe, predicate):
    """Whether the predicate holds for every element, vacuously true when empty."""
    return all(predicate(element) for element in universe)


def exists(universe, predicate):
    """Whether it holds for some element, false over an empty universe."""
    return any(predicate(element) for element in universe)


def negation_of_for_all(universe, predicate):
    """The negation of a universal statement, as an existential one.

    Stated as a computation so the equivalence can be checked rather than
    recited: the two sides are evaluated over the same universe and compared.
    """
    return exists(universe, lambda element: not predicate(element))
