"""The three monad laws, checked over samples.

Return is a left and a right identity for bind, and bind is associative in
the sense that regrouping a chain does not change it. Nothing in the type
system enforces them, so an instance can typecheck and be wrong, which is
what the broken instance here demonstrates.

The laws are also what makes do-notation a notation rather than a construct:
it expands to a chain of binds, and the associativity law is what lets the
lines be regrouped without changing the meaning.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "haskell-core", "algebraic-data-types"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "monad"))
import algebraic_data_types as adt
import monad

STEPS = [lambda value: [value, value + 1], lambda value: [value * 2]]
"""Sample steps for the list instance."""


def _samples(name):
    """Sample values of the instance."""
    if name == "Maybe":
        return [adt.NOTHING, adt.just(1), adt.just(4)]
    return [[], [1], [1, 2, 3]]


def _steps(name):
    """Sample steps of the instance."""
    if name == "Maybe":
        return [lambda value: adt.just(value + 1),
                lambda value: adt.NOTHING if value > 2 else adt.just(value * 2)]
    return STEPS


def left_identity(name):
    """Whether return followed by bind is the step itself."""
    instance = "List" if name == "Broken" else name
    for step in _steps(instance):
        for value in (1, 3, 5):
            if monad.bind(name, monad.unit(instance, value), step) != step(value):
                return False
    return True


def right_identity(name):
    """Whether binding return changes nothing."""
    for sample in _samples(name):
        if monad.bind(name, sample, lambda value: monad.unit(name, value)) \
                != sample:
            return False
    return True


def associativity(name):
    """Whether regrouping a chain of binds changes nothing."""
    steps = _steps(name)
    for sample in _samples(name):
        left = monad.bind(name, monad.bind(name, sample, steps[0]), steps[1])
        right = monad.bind(name, sample,
                           lambda value: monad.bind(name, steps[0](value),
                                                    steps[1]))
        if left != right:
            return False
    return True


def do_matches_bind():
    """Whether do-notation and an explicit bind chain agree.

    The exam asks for the translation in one direction. Running both and
    comparing is the check that the translation preserves meaning, which is
    the claim the notation rests on.
    """
    step = lambda value: adt.just(value * 2)
    with_bind = monad.bind("Maybe", adt.just(3),
                           lambda first: monad.bind("Maybe", step(first),
                                                    lambda second:
                                                    adt.just(first + second)))
    first = 3
    second = adt.from_just(step(first))
    with_do = adt.just(first + second)
    return with_bind == with_do
