"""Beta reduction, and the strategies that disagree about termination.

A redex is an abstraction applied to an argument, and contracting it
substitutes. Which redex is contracted first is the strategy, and it matters:
call by value evaluates the argument first and diverges on a term whose
argument has no normal form, while the normal order strategy contracts the
leftmost outermost redex and finds a normal form whenever one exists.

That is the theorem behind lazy evaluation. Haskell's semantics is the normal
order one, which is why a definition may mention a value that is never
computed.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "syntax-and-substitution"))
import syntax_and_substitution as syntax


def is_redex(term):
    """Whether the term is an application of an abstraction."""
    return term[0] == "app" and term[1][0] == "lam"


def contract(term):
    """Performs the substitution a redex stands for."""
    if not is_redex(term):
        raise ValueError("not a redex")
    return syntax.substitute(term[1][2], term[1][1], term[2])


def normal_order_step(term):
    """Contracts the leftmost outermost redex, or returns nothing."""
    if is_redex(term):
        return contract(term)
    if term[0] == "lam":
        inner = normal_order_step(term[2])
        return syntax.abstraction(term[1], inner) if inner else None
    if term[0] == "app":
        left = normal_order_step(term[1])
        if left is not None:
            return syntax.application(left, term[2])
        right = normal_order_step(term[2])
        if right is not None:
            return syntax.application(term[1], right)
    return None


def call_by_value_step(term):
    """Contracts only when the argument is already a value."""
    if term[0] == "app":
        left = call_by_value_step(term[1])
        if left is not None:
            return syntax.application(left, term[2])
        right = call_by_value_step(term[2])
        if right is not None:
            return syntax.application(term[1], right)
        if is_redex(term):
            return contract(term)
    return None


def call_by_name_step(term):
    """Contracts the leftmost redex without going under an abstraction."""
    if is_redex(term):
        return contract(term)
    if term[0] == "app":
        left = call_by_name_step(term[1])
        if left is not None:
            return syntax.application(left, term[2])
    return None


def normal_form(term, limit=10000):
    """The normal form under the normal order strategy, or nothing."""
    current = term
    for _ in range(limit):
        following = normal_order_step(current)
        if following is None:
            return current
        current = following
    return None


def call_by_name(term, limit=10000):
    """The weak head normal form, which is what a lazy language computes."""
    current = term
    for _ in range(limit):
        following = call_by_name_step(current)
        if following is None:
            return current
        current = following
    return None


def call_by_value(term, limit=10000):
    """The value under the strict strategy, or nothing when it diverges."""
    current = term
    for _ in range(limit):
        following = call_by_value_step(current)
        if following is None:
            return current
        current = following
    return None


def steps(term, limit=1000):
    """Every intermediate term of the normal order reduction."""
    result = [term]
    current = term
    for _ in range(limit):
        following = normal_order_step(current)
        if following is None:
            return result
        result.append(following)
        current = following
    return result


def confluent(term, limit=200):
    """Whether every reduction path from the term ends at the same normal form.

    The Church-Rosser theorem says it always does. Checking it on a term
    means reducing it in several ways and comparing, which is a test of the
    implementation rather than of the theorem.
    """
    target = normal_form(term, limit)
    if target is None:
        return True
    for strategy in (call_by_value_step, normal_order_step):
        current = term
        for _ in range(limit):
            following = strategy(current)
            if following is None:
                break
            current = following
        reached = normal_form(current, limit)
        if reached is None or not syntax.alpha_equal(reached, target):
            return False
    return True
