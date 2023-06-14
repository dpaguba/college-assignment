"""The pumping lemma for context-free languages.

For a context-free language there is a length n such that every word z in it
with |z| >= n can be written as

    z = u v w x y      with   |vwx| <= n,   |vx| >= 1,   u v^i w x^i y in L

for every i >= 0. Two pieces are pumped **together**, and that is the whole
difference from the regular version: a context-free language can keep two
counts in step, and that is exactly what it cannot do for three.

The proof is the parse tree. In a grammar in Chomsky normal form, a long
enough word forces a path from the root deeper than the number of variables, so
some variable repeats on it, and the subtree between the two occurrences can be
inserted again or cut out.

The standard use is showing that ``a^n b^n c^n`` is not context-free: whatever
vwx is, it fits inside two of the three blocks, so pumping changes two counts
and leaves the third behind.
"""

from __future__ import annotations


def pump(u, v, w, x, y, times):
    """The word ``u v^i w x^i y``."""
    return u + v * times + w + x * times + y


def decompositions(word, length):
    """Every split allowed by the lemma: ``|vwx| <= n`` and ``|vx| >= 1``.

    These are the adversary's moves, and there are many more than in the
    regular case: four cut points instead of two, so the case analysis in an
    exercise is correspondingly longer.
    """
    found = []
    size = len(word)

    for start in range(size + 1):
        for span in range(1, min(length, size - start) + 1):
            middle = word[start:start + span]
            for first in range(len(middle) + 1):
                for second in range(first, len(middle) + 1):
                    v = middle[:first]
                    w = middle[first:second]
                    x = middle[second:]
                    if not v and not x:
                        continue
                    found.append((word[:start], v, w, x, word[start + span:]))

    return found


def defeat_split(membership, u, v, w, x, y, max_power=4):
    """An exponent that pushes the pumped word out of the language."""
    for times in range(max_power + 1):
        if not membership(pump(u, v, w, x, y, times)):
            return times
    return None


def win_round(membership, word, length, max_power=4):
    """Whether every allowed decomposition of a word can be defeated."""
    for u, v, w, x, y in decompositions(word, length):
        if defeat_split(membership, u, v, w, x, y, max_power) is None:
            return False, (u, v, w, x, y)
    return True, None


def refute_context_free(membership, candidates, max_length=6, max_power=4):
    """Play the game for every pumping length up to a bound.

    A language that loses no round is very probably not context-free, and the
    transcript is the case analysis an exercise asks for.
    """
    transcript = []

    for length in range(1, max_length + 1):
        word = candidates(length) if callable(candidates) else candidates.get(length)
        if word is None:
            continue

        if not membership(word):
            raise ValueError(f"the word {word!r} chosen for n = {length} is not in the language")

        won, survivor = win_round(membership, word, length, max_power)
        transcript.append({"n": length, "word": word, "won": won,
                           "surviving split": survivor,
                           "splits": len(decompositions(word, length))})

        if not won:
            return False, transcript

    return True, transcript


def survives_pumping(membership, length, words, max_power=4):
    """Check that a context-free language does pump, as a control.

    Run on a language that **is** context-free, every long enough word must
    have some decomposition that survives every exponent. Without this control
    a bug in the search would "prove" that every language fails.
    """
    for word in words:
        if len(word) < length or not membership(word):
            continue

        survived = False
        for u, v, w, x, y in decompositions(word, length):
            if all(membership(pump(u, v, w, x, y, times)) for times in range(max_power + 1)):
                survived = True
                break

        if not survived:
            return False, word

    return True, None


def three_equal_blocks():
    """``a^n b^n c^n``, the standard language that is not context-free."""
    def membership(word):
        """Whether the word is three equal blocks of a, b and c."""
        count = len(word) // 3
        return word == "a" * count + "b" * count + "c" * count and len(word) % 3 == 0
    return membership


def copy_language(alphabet="ab"):
    """``{ ww }``, which is not context-free either.

    A pushdown automaton reverses what it stores, so it can check ``w w^R``
    and not ``w w``. The stack is a stack, not a queue.
    """
    def membership(word):
        """Whether the word is some text followed by a copy of itself."""
        if len(word) % 2 or set(word) - set(alphabet):
            return False
        half = len(word) // 2
        return word[:half] == word[half:]
    return membership


def equal_counts():
    """``a^n b^n``, which **is** context-free, used as the control."""
    def membership(word):
        """Whether the word is as many a's as b's, in that order."""
        count = word.count("a")
        return word == "a" * count + "b" * count
    return membership
