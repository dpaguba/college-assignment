"""Type inference in the style of Hindley and Milner.

The algorithm walks the term, invents a fresh variable wherever the term does
not say what the type is, and calls unification whenever the rules force two
types to agree. What comes back is the principal type: every other type the
term has is an instance of it.

That is the property that makes inference useful rather than merely possible.
The identity gets ``t0 -> t0`` and not ``int -> int``, so one definition
serves every use.
"""

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "unification"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "lambda-calculus", "syntax-and-substitution"))
import syntax_and_substitution as syntax
import unification


def principal_type(text):
    """The principal type of a term, printed, or nothing when it has none."""
    term = syntax.parse(text)
    counter = itertools.count()
    try:
        kind, substitution = _infer(term, {}, {}, counter)
    except ValueError:
        return None
    resolved = unification.apply(substitution, kind)
    return to_text(resolved)


def _fresh(counter):
    """A fresh type variable."""
    return ("var", "t%d" % next(counter))


def _infer(term, environment, substitution, counter):
    """The type of a term and the substitution the inference accumulated."""
    if term[0] == "var":
        if term[1] not in environment:
            raise ValueError("unbound variable: %s" % term[1])
        return environment[term[1]], substitution
    if term[0] == "lam":
        argument = _fresh(counter)
        inner = dict(environment)
        inner[term[1]] = argument
        body, substitution = _infer(term[2], inner, substitution, counter)
        return ("arrow", argument, body), substitution
    function, substitution = _infer(term[1], environment, substitution, counter)
    argument, substitution = _infer(term[2], environment, substitution, counter)
    result = _fresh(counter)
    merged = unification.unify(unification.apply(substitution, function),
                               ("arrow", argument, result), substitution)
    if merged is None:
        raise ValueError("type mismatch")
    return result, merged


def to_text(kind):
    """The written form of a type."""
    if isinstance(kind, tuple) and kind[0] == "var":
        return kind[1]
    if isinstance(kind, str):
        return kind
    return "(%s -> %s)" % (to_text(kind[1]), to_text(kind[2]))


def is_principal(text, candidate):
    """Whether the given type is the principal type of the term.

    A term has many types and one principal type. Checking that a concrete
    type such as ``int -> int`` is not principal for the identity is the
    check that the inference is not accidentally committing to something.
    """
    return principal_type(text) == candidate
