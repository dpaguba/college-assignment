"""The simply typed lambda calculus, and what typing costs.

Three rules: a variable has the type the environment gives it, an
abstraction has an arrow type built from the type of its binder and the type
of its body, and an application requires the argument type to match the
domain of the function.

The price is expressiveness. Self application cannot be typed, because the
same term would have to be both a function and its own argument, so the
divergent term of the course file has no type at all. That is the theorem
behind strong normalisation: every typable term has a normal form, and the
terms that do not are exactly the ones the type system rejects.
"""

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "lambda-calculus", "syntax-and-substitution"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "unification"))
import syntax_and_substitution as syntax
import unification


class TypeError_(Exception):
    """Raised when a term cannot be typed."""


def arrow(source, target):
    """The type of functions from one type to another."""
    return ("arrow", source, target)


def variable(name):
    """A type variable, kept distinct from a constant of the same name."""
    return ("var", name)


class TypeError_(Exception):
    """Raised when a term cannot be typed."""


def to_text(kind):
    """The written form of a type."""
    if isinstance(kind, str):
        return kind
    if kind[0] == "var":
        return kind[1]
    return "(%s -> %s)" % (to_text(kind[1]), to_text(kind[2]))


def infer(term, environment):
    """The type of a term in an environment, or a raised error.

    Fresh variables stand for whatever the term does not fix, and
    unification resolves them, so this is inference rather than checking even
    though the calculus is the simply typed one.
    """
    counter = itertools.count()
    substitution = {}
    kind = _infer(term, dict(environment), substitution, counter)
    return unification.apply(substitution, kind)


def _fresh(counter):
    """A fresh type variable, named with a letter."""
    return variable(chr(ord("a") + next(counter) % 26))


def _infer(term, environment, substitution, counter):
    """The inference itself, accumulating a substitution."""
    if term[0] == "var":
        if term[1] not in environment:
            raise TypeError_("unbound variable: %s" % term[1])
        return environment[term[1]]
    if term[0] == "lam":
        argument = _fresh(counter)
        inner = dict(environment)
        inner[term[1]] = argument
        result = _infer(term[2], inner, substitution, counter)
        return arrow(unification.apply(substitution, argument), result)
    function = _infer(term[1], environment, substitution, counter)
    argument = _infer(term[2], environment, substitution, counter)
    result = _fresh(counter)
    merged = unification.unify(unification.apply(substitution, function),
                               arrow(unification.apply(substitution, argument),
                                     result),
                               substitution)
    if merged is None:
        raise TypeError_("cannot match %s with an arrow into %s"
                         % (to_text(function), to_text(result)))
    substitution.clear()
    substitution.update(merged)
    return unification.apply(substitution, result)


def is_typable(term, environment=None):
    """Whether the term has a type at all."""
    try:
        infer(term, environment or {})
        return True
    except TypeError_:
        return False
