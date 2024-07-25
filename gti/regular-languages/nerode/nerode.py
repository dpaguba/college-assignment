"""The Nerode relation: the states a language forces you to have.

Two words are **Nerode-equivalent** for a language L when no continuation tells
them apart:

    x ~L y   iff   for all z:  xz in L  <=>  yz in L

The relation is an equivalence, its classes partition the words over the
alphabet, and the Myhill-Nerode theorem says:

    L is regular  <=>  ~L has finitely many classes

and then the number of classes is exactly the number of states of the minimal
DFA. That is the deepest statement of the first block: the minimal automaton
is not something a clever algorithm found, it is forced by the language itself.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "finite-automata"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "minimisation"))

from finite_automata import DFA
from minimisation import minimise


def classes_from_dfa(dfa, max_length=6):
    """The Nerode classes of L(A), with the words of each up to a length.

    Two words are equivalent exactly when they lead the **minimal** automaton
    into the same state, so the classes are read off by running every short
    word and grouping by the state reached. Using the minimal automaton rather
    than the given one matters: a non-minimal automaton splits classes that the
    language does not.
    """
    minimal = minimise(dfa)
    groups = {}

    queue = [""]
    while queue:
        word = queue.pop(0)
        state = _state_after(minimal, word)
        if state is not None:
            groups.setdefault(state, []).append(word)
        if len(word) < max_length:
            queue.extend(word + symbol for symbol in minimal.alphabet)

    return {state: words for state, words in sorted(groups.items(), key=str)}


def _state_after(dfa, word):
    """The state the automaton reaches after reading the word."""
    current = dfa.start
    for symbol in word:
        current = dfa.step(current, symbol)
        if current is None:
            return None
    return current


def index(dfa):
    """The number of Nerode classes, which is the size of the minimal DFA."""
    return len(minimise(dfa).states)


def equivalent(dfa, first, second, max_length=8):
    """Whether two words are Nerode-equivalent for the language of a DFA.

    Decided exactly, by running both words and comparing the states of the
    minimal automaton, rather than by testing continuations up to a length.
    The continuation test is what the definition says; the state test is what
    makes it decidable.
    """
    minimal = minimise(dfa)
    return _state_after(minimal, first) == _state_after(minimal, second)


def separating_continuation(dfa, first, second, max_length=8):
    """A word z with exactly one of ``first + z`` and ``second + z`` in the language.

    This is the witness the definition asks for. If the two words are
    equivalent there is none, and the search says so by returning None after
    exhausting the bound.
    """
    for length in range(max_length + 1):
        for word in _words(dfa.alphabet, length):
            if dfa.accepts(first + word) != dfa.accepts(second + word):
                return word
    return None


def _words(alphabet, length):
    """Every word of the given length over the alphabet."""
    if length == 0:
        yield ""
        return
    for prefix in _words(alphabet, length - 1):
        for symbol in alphabet:
            yield prefix + symbol


def classes_from_language(membership, alphabet, max_word=4, max_test=5):
    """Approximate the Nerode classes of a language given only as a predicate.

    Words up to ``max_word`` are grouped by their behaviour on continuations up
    to ``max_test``. Two words land in the same group when no tested
    continuation separates them.

    This is a **test**, not a proof: a longer continuation might still separate
    two words that look equal here. It is exactly the practical method for the
    exercise that asks to find the classes of a language by hand, and it has
    exactly the same limitation.
    """
    words = []
    queue = [""]
    while queue:
        word = queue.pop(0)
        words.append(word)
        if len(word) < max_word:
            queue.extend(word + symbol for symbol in alphabet)

    tests = []
    queue = [""]
    while queue:
        word = queue.pop(0)
        tests.append(word)
        if len(word) < max_test:
            queue.extend(word + symbol for symbol in alphabet)

    groups = {}
    for word in words:
        signature = tuple(membership(word + test) for test in tests)
        groups.setdefault(signature, []).append(word)

    return sorted(groups.values(), key=lambda group: (len(group[0]), group[0]))


def lower_bound_witness(membership, alphabet, candidates):
    """Show that a language needs at least as many states as candidates given.

    Every pair of the candidate words is checked for a separating
    continuation. If all pairs are separated, they lie in distinct Nerode
    classes, and the minimal automaton needs at least that many states. With
    an infinite family of pairwise separated words, the same argument proves
    the language is **not** regular, which is the Myhill-Nerode alternative to
    the pumping lemma and is usually shorter.
    """
    separated = {}
    for index_first, first in enumerate(candidates):
        for second in candidates[index_first + 1:]:
            witness = None
            queue = [""]
            while queue and witness is None:
                test = queue.pop(0)
                if membership(first + test) != membership(second + test):
                    witness = test
                elif len(test) < 6:
                    queue.extend(test + symbol for symbol in alphabet)
            separated[(first, second)] = witness

    return separated, all(witness is not None for witness in separated.values())
