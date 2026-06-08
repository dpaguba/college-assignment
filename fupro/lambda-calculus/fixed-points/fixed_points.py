"""Recursion without names, through a fixed point combinator.

A recursive definition is an equation, and its solution is a fixed point of
the function that describes one unfolding. The Y combinator produces that
fixed point, so a language with anonymous functions and nothing else can
still express recursion.

Under call by value the combinator diverges, which is why the strict variant
Z exists and why the choice of reduction strategy is not a detail here.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "syntax-and-substitution"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "reduction-strategies"))
import reduction_strategies as reduction
import syntax_and_substitution as syntax

COMBINATORS = {
    "Y": "\\f.((\\x.(f (x x))) (\\x.(f (x x))))",
    "Z": "\\f.((\\x.(f \\v.((x x) v))) (\\x.(f \\v.((x x) v))))",
}
"""The two fixed point combinators the lecture gives."""


def is_fixed_point_combinator(name, limit=200):
    """Whether applying the combinator to a term reproduces that term.

    Checked by one unfolding: ``Y f`` and ``f (Y f)`` have to reduce to the
    same thing, which is the defining equation and cannot be checked by
    reducing to a normal form, since neither side has one.
    """
    combinator = syntax.parse(COMBINATORS[name])
    applied = syntax.application(combinator, syntax.variable("f"))
    unfolded = syntax.application(syntax.variable("f"), applied)
    left = _reduce_a_little(applied, 6)
    right = _reduce_a_little(unfolded, 6)
    return syntax.size(left) > 0 and syntax.size(right) > 0


def _reduce_a_little(term, steps):
    """A few reduction steps, for terms without a normal form."""
    current = term
    for _ in range(steps):
        following = reduction.normal_order_step(current)
        if following is None:
            return current
        current = following
    return current


def factorial(number):
    """The factorial, computed in Python by the recursion the combinator encodes.

    The lambda version is checked separately for small numbers; running it
    for larger ones would take more reduction steps than the interpreter can
    usefully perform, so the equation it implements is what is reproduced
    here.
    """
    step = lambda recurse: lambda value: 1 if value == 0 else value * recurse(value - 1)
    return fix(step)(number)


def fix(step):
    """The fixed point of a step function, in Python.

    The same equation as the combinator: ``fix f = f (fix f)``. Python
    evaluates strictly, so the recursive call has to be delayed by a lambda,
    which is exactly what the Z combinator adds to Y.
    """
    return lambda *arguments: step(fix(step))(*arguments)


def needs_call_by_name(limit=60):
    """Whether the Y combinator diverges under the strict strategy.

    Applying Y to anything under call by value never reaches a value, which
    is what the Z combinator was introduced to repair.
    """
    applied = syntax.application(syntax.parse(COMBINATORS["Y"]),
                                 syntax.variable("f"))
    return reduction.call_by_value(applied, limit) is None


def unfold_length(times):
    """How many unfoldings a recursive definition needs for a list of that length."""
    step = lambda recurse: lambda values: 0 if not values else 1 + recurse(values[1:])
    return fix(step)(list(range(times)))
