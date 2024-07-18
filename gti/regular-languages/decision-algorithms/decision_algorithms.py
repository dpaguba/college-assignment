"""What can be decided about regular languages, and how fast.

The strength of the regular class is that every natural question about it is
decidable, which stops being true one level up: for context-free languages,
equivalence is already undecidable.

| Question | Method | Cost |
|---|---|---|
| word in language | run the automaton | O(length) |
| language empty | reachability | O(states + edges) |
| language finite | look for a useful cycle | O(states + edges) |
| languages equal | symmetric difference is empty | product, then reachability |
| one contained in the other | difference is empty | product, then reachability |
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "finite-automata"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "closure-properties"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "minimisation"))

import closure_properties as closure
from finite_automata import DFA
from minimisation import isomorphic, minimise


def accepts(dfa, word):
    """The word problem: does the automaton accept this word.

    Linear in the length of the word and independent of the size of the
    automaton, which is what makes regular expressions usable in a text editor.
    """
    return dfa.accepts(word)


def is_empty(dfa):
    """Whether the language is empty, and a witness word when it is not.

    Reachability: the language is non-empty exactly when some accepting state
    is reachable from the start. The shortest path to one is the shortest word
    in the language.
    """
    witness = dfa.shortest_word()
    return witness is None, witness


def is_finite(dfa):
    """Whether the language is finite, and a pumpable word when it is not.

    A language is infinite exactly when the trimmed automaton has a cycle: any
    cycle can be run any number of times, and everything in a trimmed
    automaton is both reachable and useful. Finding the cycle also produces
    the word that witnesses the infinity.
    """
    trimmed = dfa.trim()
    colour = {}
    stack = []

    def walk(state):
        """Depth-first search that reports a cycle through the colouring."""
        colour[state] = "grey"
        stack.append(state)

        for symbol in trimmed.alphabet:
            target = trimmed.step(state, symbol)
            if target is None:
                continue
            if colour.get(target) == "grey":
                return stack[stack.index(target):]
            if target not in colour:
                found = walk(target)
                if found:
                    return found

        colour[state] = "black"
        stack.pop()
        return None

    cycle = walk(trimmed.start) if trimmed.states else None
    if cycle is None:
        return True, None

    return False, cycle


def equivalent(first, second):
    """Whether two automata accept the same language, with a witness if not.

    Two ways, both here. The symmetric difference must be empty, which is the
    construction the course gives; and the minimal automata must be isomorphic,
    which is the same statement read through Myhill-Nerode.

    The witness is the shortest word in the symmetric difference, which is the
    useful part of a negative answer.
    """
    alphabet = tuple(sorted(set(first.alphabet) | set(second.alphabet)))
    first = first.with_alphabet(alphabet)
    second = second.with_alphabet(alphabet)

    difference = closure.product(first, second, "symmetric")
    empty, witness = is_empty(difference)

    by_minimisation = isomorphic(minimise(first), minimise(second))
    if empty != by_minimisation:
        raise AssertionError("the two decision methods disagree, which cannot happen")

    return empty, witness


def contains(outer, inner):
    """Whether every word of the inner language is in the outer one.

    Inclusion reduces to emptiness of ``inner minus outer``, which is one
    product automaton away. Nothing here needs to enumerate words.
    """
    alphabet = tuple(sorted(set(inner.alphabet) | set(outer.alphabet)))
    empty, witness = is_empty(closure.product(inner.with_alphabet(alphabet),
                                              outer.with_alphabet(alphabet), "difference"))
    return empty, witness


def is_universal(dfa):
    """Whether the automaton accepts every word over its alphabet."""
    empty, witness = is_empty(closure.complement(dfa))
    return empty, witness


def size_report(dfa):
    """Everything the decision procedures can say about one automaton."""
    empty, shortest = is_empty(dfa)
    finite, cycle = is_finite(dfa)
    minimal = minimise(dfa)

    return {
        "states": len(dfa.states),
        "minimal states": len(minimal.states),
        "empty": empty,
        "shortest word": shortest,
        "finite": finite,
        "cycle": cycle,
        "universal": is_universal(dfa)[0],
    }
