"""From an automaton back to a regular expression, by eliminating states.

The second half of Kleene's theorem. Every state except the start and the
accepting one is removed, and the paths that went through it are written into
the labels of the edges that remain.

Removing state q with a self-loop labelled ``s`` turns every pair of an
incoming edge ``x`` and an outgoing edge ``y`` into a direct edge labelled

    x s* y

added to whatever label that pair already had. When only two states are left,
the answer can be read off directly.

The result is correct and usually ugly: the size depends on the elimination
order, and finding the order that gives the shortest expression is itself hard.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "finite-automata"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "regular-expressions"))

from finite_automata import DFA, EPSILON, NFA
from regular_expressions import (Empty, Epsilon, Regex, Symbol, concat, parse,
                                 star, union)


def to_regex(automaton, order=None):
    """Convert a DFA or NFA into an equivalent regular expression.

    A fresh start and a fresh accepting state are added first, joined by
    epsilon edges. That guarantees the two states that survive elimination are
    exactly those two, so the final read-off has one shape instead of four.

    ``order`` fixes which states go first. The default removes them in a
    stable sorted order, which keeps the output reproducible; a different
    order gives a different but equivalent expression, often much shorter.
    """
    edges, start, accept, states = _generalise(automaton)

    for state in (order or sorted(states, key=str)):
        if state in (start, accept):
            continue
        _eliminate(state, edges, states)

    return edges.get((start, accept), Empty())


def _generalise(automaton):
    """Turn the automaton into a generalised one with regex-labelled edges."""
    if isinstance(automaton, DFA):
        automaton = automaton.to_nfa()

    states = set(automaton.states) | {"<start>", "<accept>"}
    edges = {}

    def add(source, target, expression):
        """Joins a new label onto the edge with an alternation."""
        edges[(source, target)] = union(edges.get((source, target), Empty()), expression)

    for (state, symbol), targets in automaton.transitions.items():
        label = Epsilon() if symbol == EPSILON else Symbol(symbol)
        for target in targets:
            add(state, target, label)

    for state in automaton.start:
        add("<start>", state, Epsilon())
    for state in automaton.accepting:
        add(state, "<accept>", Epsilon())

    return edges, "<start>", "<accept>", states


def _eliminate(state, edges, states):
    """Remove one state, rerouting every path that went through it."""
    loop = star(edges.get((state, state), Empty()))

    incoming = [(source, label) for (source, target), label in list(edges.items())
                if target == state and source != state]
    outgoing = [(target, label) for (source, target), label in list(edges.items())
                if source == state and target != state]

    for source, before in incoming:
        for target, after in outgoing:
            detour = concat(concat(before, loop), after)
            edges[(source, target)] = union(edges.get((source, target), Empty()), detour)

    for key in list(edges):
        if state in key:
            del edges[key]

    states.discard(state)


def round_trip(text, max_length=6):
    """Check that an expression survives regex to automaton and back.

    Builds the automaton, determinises, minimises, converts back, and compares
    the two languages up to a length. The expression that comes back is almost
    never the one that went in; the language is.
    """
    import subset_construction
    import thompson_construction
    from minimisation import minimise
    from regular_expressions import language

    original = parse(text) if isinstance(text, str) else text
    automaton = minimise(subset_construction.determinise(
        thompson_construction.build(original)))
    recovered = to_regex(automaton)

    return recovered, language(original, max_length) == language(recovered, max_length)
