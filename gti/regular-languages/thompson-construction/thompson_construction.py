"""Thompson's construction: a regular expression becomes an epsilon-NFA.

One of the two directions of Kleene's theorem, and the easy one. The proof is
an induction over the five cases of the syntax, and each case is a picture
that glues smaller automata together with epsilon transitions.

Every fragment built here keeps two invariants, and they are what make the
gluing safe:

- exactly one start state and exactly one accepting state
- no transition enters the start state and none leaves the accepting one

That is why the pieces compose without interfering, and why the resulting
automaton has at most twice as many states as the expression has symbols and
operators: each case adds at most two.
"""

from __future__ import annotations

import sys
from itertools import count
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "finite-automata"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "regular-expressions"))

from finite_automata import EPSILON, NFA
from regular_expressions import (Concat, Empty, Epsilon, Regex, Star, Symbol,
                                 Union, parse)


class _Builder:
    """Allocates fresh state names and collects the transitions."""

    def __init__(self):
        """A builder with a fresh state counter and no transitions."""
        self.counter = count()
        self.transitions = {}
        self.states = set()

    def fresh(self):
        """A state name that has not been used before."""
        state = f"s{next(self.counter)}"
        self.states.add(state)
        return state

    def add(self, source, symbol, target):
        """Records one transition of the fragment being built."""
        self.transitions.setdefault((source, symbol), set()).add(target)


def build(expression):
    """Turn a regular expression into an equivalent epsilon-NFA.

    The five cases:

    - empty set: two states and no transition at all
    - epsilon: two states joined by an epsilon step
    - symbol: two states joined by that symbol
    - union: a new start branching into both fragments, both ends joined to a
      new accepting state
    - concatenation: the accepting state of the first fragment joined by
      epsilon to the start of the second
    - star: a new start and end, with epsilon steps in, out, around and back

    The epsilon steps are what keep the fragments from interfering. Merging
    states instead would be smaller and would break the invariants, which is
    the usual source of an off-by-one in a hand-drawn construction.
    """
    if isinstance(expression, str):
        expression = parse(expression)

    builder = _Builder()
    start, accept = _fragment(expression, builder)

    return NFA(
        states=set(builder.states),
        alphabet=tuple(sorted(expression.symbols())),
        transitions=builder.transitions,
        start={start},
        accepting={accept},
        name=f"Thompson({expression})",
    )


def _fragment(expression, builder):
    """The start and end state of the fragment built for the expression."""
    if isinstance(expression, Empty):
        return builder.fresh(), builder.fresh()

    if isinstance(expression, Epsilon):
        start, accept = builder.fresh(), builder.fresh()
        builder.add(start, EPSILON, accept)
        return start, accept

    if isinstance(expression, Symbol):
        start, accept = builder.fresh(), builder.fresh()
        builder.add(start, expression.value, accept)
        return start, accept

    if isinstance(expression, Union):
        left_start, left_accept = _fragment(expression.left, builder)
        right_start, right_accept = _fragment(expression.right, builder)
        start, accept = builder.fresh(), builder.fresh()

        builder.add(start, EPSILON, left_start)
        builder.add(start, EPSILON, right_start)
        builder.add(left_accept, EPSILON, accept)
        builder.add(right_accept, EPSILON, accept)
        return start, accept

    if isinstance(expression, Concat):
        left_start, left_accept = _fragment(expression.left, builder)
        right_start, right_accept = _fragment(expression.right, builder)
        builder.add(left_accept, EPSILON, right_start)
        return left_start, right_accept

    if isinstance(expression, Star):
        inner_start, inner_accept = _fragment(expression.inner, builder)
        start, accept = builder.fresh(), builder.fresh()

        builder.add(start, EPSILON, inner_start)
        builder.add(start, EPSILON, accept)
        builder.add(inner_accept, EPSILON, inner_start)
        builder.add(inner_accept, EPSILON, accept)
        return start, accept

    raise TypeError(f"not a regular expression: {expression!r}")


def size_bound(expression):
    """How many states the construction produces, and the bound that predicts it.

    Two states per symbol, per epsilon, per union and per star, and none for a
    concatenation. The result is linear in the size of the expression, which is
    the property that makes Thompson's construction the one compilers use.
    """
    if isinstance(expression, str):
        expression = parse(expression)

    def count_nodes(node):
        """How many states the construction produces for this node."""
        if isinstance(node, (Empty, Epsilon, Symbol)):
            return 2
        if isinstance(node, Union):
            return 2 + count_nodes(node.left) + count_nodes(node.right)
        if isinstance(node, Concat):
            return count_nodes(node.left) + count_nodes(node.right)
        return 2 + count_nodes(node.inner)

    return count_nodes(expression)
