"""Monads: sequencing computations that carry a context.

The context is what the functor holds on to: possible absence for Maybe,
several results for a list, a threaded state for State. Bind runs the second
computation on the result of the first and lets the instance decide what to
do with the context, which is why the same do-notation reads as failure
propagation, as a nested loop, or as a state machine.

The exam asks for three things from this module: the translation of a bind
chain into do-notation, a map over a monad that fails as a whole, and a stack
machine written in the state monad.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "haskell-core", "algebraic-data-types"))
import algebraic_data_types as adt


def unit(name, value):
    """The value in the monad, called return in Haskell."""
    if name == "List":
        return [value]
    if name == "Maybe":
        return adt.just(value)
    raise ValueError("no monad instance for %s" % name)


def bind(name, value, step):
    """Runs the step on the contents, in the way the instance prescribes."""
    if name == "List":
        result = []
        for item in value:
            result.extend(step(item))
        return result
    if name == "Maybe":
        return adt.NOTHING if adt.is_nothing(value) else step(adt.from_just(value))
    if name == "Broken":
        return [] if isinstance(value, list) else adt.NOTHING
    raise ValueError("no monad instance for %s" % name)


def map_m(name, step, values):
    """The exam's mapM: a step over every element, failing as a whole.

    Written with bind, which is what the exam asks to translate into
    do-notation. The translation is mechanical: every bind whose result is
    named becomes a binding line, and the final return becomes the last
    expression.
    """
    if not values:
        return unit(name, [])
    head, tail = values[0], values[1:]
    return bind(name, step(head),
                lambda first: bind(name, map_m(name, step, tail),
                                   lambda rest: unit(name, [first] + rest)))


def try_map(step, values):
    """The exam's tryMap: map over a list, giving nothing if any step fails."""
    return map_m("Maybe", step, values)


def state(run):
    """A state computation, which is a function from state to value and state."""
    return ("State", run)


def run_state(computation, initial):
    """Runs a state computation on an initial state."""
    return computation[1](initial)


def state_unit(value):
    """The computation that returns a value and leaves the state alone."""
    return state(lambda current: (value, current))


def state_bind(computation, step):
    """Threads the state from one computation into the next."""
    def run(current):
        """Runs the first computation and then the one the step builds."""
        value, following = run_state(computation, current)
        return run_state(step(value), following)
    return state(run)


def push(item):
    """Puts a value on the stack."""
    return state(lambda stack: (None, [item] + stack))


def pop():
    """Takes the top value off, or nothing when the stack is empty."""
    def run(stack):
        """Removes the head if there is one."""
        if not stack:
            return (adt.NOTHING, [])
        return (adt.just(stack[0]), stack[1:])
    return state(run)


def clear():
    """The exam's clear: returns the whole stack and empties it."""
    return state(lambda stack: (stack, []))


def push_n(items):
    """The exam's pushN: pushes a list so its head ends up on top."""
    if not items:
        return state_unit(None)
    return state_bind(push_n(items[1:]), lambda _ignored: push(items[0]))


def pop_n(count):
    """The exam's popN: the top values, or as many as there are."""
    if count == 0:
        return state_unit([])
    def step(value):
        """Continues with the rest once one value has been taken."""
        if adt.is_nothing(value):
            return state_unit([])
        return state_bind(pop_n(count - 1),
                          lambda rest: state_unit([adt.from_just(value)] + rest))
    return state_bind(pop(), step)
