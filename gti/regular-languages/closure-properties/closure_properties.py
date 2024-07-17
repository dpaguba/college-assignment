"""Closure properties: the operations regular languages survive.

The class of regular languages is closed under union, intersection,
complement, difference, concatenation, star, reversal and homomorphism. Each
proof is a construction, and each construction is here.

Two of them carry most of the weight in exercises. The **product automaton**
runs two automata side by side and gives intersection, union and difference in
one construction, and the **complement** is a one-line change that is wrong
unless the automaton is complete first.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "finite-automata"))

from finite_automata import DFA, EPSILON, NFA


def product(first, second, accept="intersection", name=None):
    """Run two DFAs side by side, one state pair at a time.

    The states are pairs, the transitions move both components, and the
    accepting set decides which operation this is:

    - ``intersection``: both components accept
    - ``union``: at least one accepts
    - ``difference``: the first accepts and the second does not
    - ``symmetric``: exactly one accepts

    Both automata are completed first, or a missing transition in one of them
    would stop the pair automaton and quietly change the language.
    """
    alphabet = tuple(sorted(set(first.alphabet) | set(second.alphabet)))
    first = first.with_alphabet(alphabet, "trap1")
    second = second.with_alphabet(alphabet, "trap2")

    start = (first.start, second.start)
    states = {start}
    transitions = {}
    queue = [start]

    while queue:
        left, right = queue.pop(0)
        for symbol in alphabet:
            target = (first.step(left, symbol), second.step(right, symbol))
            if None in target:
                continue
            transitions[((left, right), symbol)] = target
            if target not in states:
                states.add(target)
                queue.append(target)

    tests = {
        "intersection": lambda left, right: left in first.accepting and right in second.accepting,
        "union": lambda left, right: left in first.accepting or right in second.accepting,
        "difference": lambda left, right: left in first.accepting and right not in second.accepting,
        "symmetric": lambda left, right: (left in first.accepting) != (right in second.accepting),
    }
    test = tests[accept]
    accepting = {(left, right) for left, right in states if test(left, right)}

    return DFA(states, alphabet, transitions, start, accepting,
               name or f"{accept}({first.name}, {second.name})")


def complement(dfa, alphabet=None, name=None):
    """Swap accepting and non-accepting states, after completing the automaton.

    The completion is not optional. A partial automaton rejects a word by
    getting stuck, and swapping the accepting set does not turn those words
    into accepted ones, so the result would be missing exactly the words that
    have no run at all.

    The complement is always taken **relative to an alphabet**, and the answer
    changes with it: the complement of ``a*`` over {a} is empty and over {a, b}
    is everything containing a b. Passing the alphabet explicitly is how that
    choice is made visible.
    """
    complete = dfa.with_alphabet(alphabet or dfa.alphabet)
    return DFA(set(complete.states), complete.alphabet, dict(complete.transitions),
               complete.start, complete.states - complete.accepting,
               name or f"complement({dfa.name})")


def union(first, second):
    """The union of two languages, as a product automaton."""
    return product(first, second, "union")


def intersection(first, second):
    """The intersection of two languages, as a product automaton."""
    return product(first, second, "intersection")


def difference(first, second):
    """Words accepted by the first automaton and rejected by the second."""
    return product(first, second, "difference")


def concatenation(first, second, name=None):
    """Everything from the first language followed by everything from the second.

    Built on NFAs, because the join is naturally non-deterministic: at an
    accepting state of the first automaton the machine may either continue in
    it or jump into the second, and it cannot know which is right.
    """
    left = first.to_nfa() if isinstance(first, DFA) else first
    right = second.to_nfa() if isinstance(second, DFA) else second

    transitions = {}
    for (state, symbol), targets in left.transitions.items():
        transitions[(f"l{state}", symbol)] = {f"l{target}" for target in targets}
    for (state, symbol), targets in right.transitions.items():
        transitions[(f"r{state}", symbol)] = {f"r{target}" for target in targets}

    for state in left.accepting:
        transitions.setdefault((f"l{state}", EPSILON), set()).update(
            f"r{target}" for target in right.start)

    states = {f"l{state}" for state in left.states} | {f"r{state}" for state in right.states}
    alphabet = tuple(sorted(set(left.alphabet) | set(right.alphabet)))

    return NFA(states, alphabet, transitions, {f"l{state}" for state in left.start},
               {f"r{state}" for state in right.accepting},
               name or f"concat({left.name}, {right.name})")


def kleene_star(automaton, name=None):
    """Any number of repetitions, including none.

    A fresh start state is added and made accepting, rather than making the
    old start accepting. Reusing the old start would add every word that
    happens to loop back to it, which is the standard wrong construction.
    """
    inner = automaton.to_nfa() if isinstance(automaton, DFA) else automaton

    transitions = {}
    for (state, symbol), targets in inner.transitions.items():
        transitions[(f"s{state}", symbol)] = {f"s{target}" for target in targets}

    new_start = "<star>"
    transitions[(new_start, EPSILON)] = {f"s{state}" for state in inner.start}
    for state in inner.accepting:
        transitions.setdefault((f"s{state}", EPSILON), set()).update(
            f"s{target}" for target in inner.start)

    states = {f"s{state}" for state in inner.states} | {new_start}
    accepting = {f"s{state}" for state in inner.accepting} | {new_start}

    return NFA(states, inner.alphabet, transitions, {new_start}, accepting,
               name or f"star({inner.name})")


def reversal(automaton, name=None):
    """The language read backwards.

    Every edge is turned around, the accepting states become the start states
    and the start becomes accepting. Determinism is lost even when the input
    was a DFA, which is the point: the reversed automaton has to guess where
    the word ended.
    """
    inner = automaton.to_nfa() if isinstance(automaton, DFA) else automaton

    transitions = {}
    for (state, symbol), targets in inner.transitions.items():
        for target in targets:
            transitions.setdefault((target, symbol), set()).add(state)

    return NFA(set(inner.states), inner.alphabet, transitions,
               set(inner.accepting), set(inner.start),
               name or f"reverse({inner.name})")


def homomorphism(automaton, mapping, name=None):
    """Replace every symbol by a word, which regular languages survive.

    Each edge labelled ``a`` becomes a chain of edges spelling ``mapping[a]``,
    with fresh states in between. A symbol mapped to the empty word becomes an
    epsilon edge, which is why the result is an NFA even from a DFA.
    """
    inner = automaton.to_nfa() if isinstance(automaton, DFA) else automaton

    transitions = {}
    states = set(inner.states)
    counter = 0

    for (state, symbol), targets in inner.transitions.items():
        image = mapping.get(symbol, symbol) if symbol != EPSILON else EPSILON

        for target in targets:
            if image == EPSILON or len(image) <= 1:
                transitions.setdefault((state, image), set()).add(target)
                continue

            current = state
            for position, character in enumerate(image):
                following = target if position == len(image) - 1 else f"h{counter}"
                if position < len(image) - 1:
                    counter += 1
                    states.add(following)
                transitions.setdefault((current, character), set()).add(following)
                current = following

    alphabet = tuple(sorted({character for word in mapping.values() for character in word}))
    return NFA(states, alphabet or inner.alphabet, transitions, set(inner.start),
               set(inner.accepting), name or f"hom({inner.name})")
