"""The pumping lemma, as the two-player game it actually is.

For a regular language L there is a length n such that every word w in L with
|w| >= n can be split as w = xyz with

    |xy| <= n,   |y| >= 1,   and   x y^i z in L for every i >= 0

The lemma is a **necessary** condition. It proves languages non-regular by
contradiction, and it never proves one regular: there are non-regular languages
that pump perfectly well.

The game makes the quantifiers concrete, which is where the exercises go wrong:

1. the adversary picks n
2. **you** pick a word w in L with |w| >= n
3. the adversary splits it into x, y, z respecting the two constraints
4. **you** pick i and show that x y^i z leaves L

You win a round by having an answer for every split. Winning for every n is the
proof.
"""

from __future__ import annotations


def pump(x, y, z, times):
    """The word ``x y^times z``."""
    return x + y * times + z


def decompositions(word, length):
    """Every split allowed by the lemma: ``|xy| <= n`` and ``|y| >= 1``.

    These are the adversary's moves. Enumerating them is what turns a proof
    sketch into a case analysis that can be checked.
    """
    found = []
    for split in range(min(length, len(word)) + 1):
        for end in range(split + 1, min(length, len(word)) + 1):
            found.append((word[:split], word[split:end], word[end:]))
    return found


def defeat_split(membership, x, y, z, max_power=6):
    """Find an exponent that pushes ``x y^i z`` out of the language.

    Zero counts and is often the easiest answer, since removing the repeated
    part usually breaks whatever balance the language demands.
    """
    for times in range(max_power + 1):
        if not membership(pump(x, y, z, times)):
            return times
    return None


def win_round(membership, word, length, max_power=6):
    """Whether every allowed split of a word can be defeated.

    Returns the winning exponent per split, or the split that survived. One
    surviving split loses the round: the lemma requires a contradiction for
    **every** decomposition the adversary may choose.
    """
    answers = {}

    for x, y, z in decompositions(word, length):
        times = defeat_split(membership, x, y, z, max_power)
        if times is None:
            return False, (x, y, z), answers
        answers[(x, y, z)] = times

    return True, None, answers


def refute_regular(membership, candidates, max_length=8, max_power=6):
    """Play the game for every pumping length up to a bound.

    ``candidates`` maps a pumping length n to the word to play against it, or
    is a function that produces one. A language that loses no round up to the
    bound is very probably not regular, and the transcript is the proof
    sketch: for this n, this word, and here is the exponent for every split.
    """
    transcript = []

    for length in range(1, max_length + 1):
        word = candidates(length) if callable(candidates) else candidates.get(length)
        if word is None:
            continue

        if not membership(word):
            raise ValueError(f"the word {word!r} chosen for n = {length} is not in the language")

        won, survivor, answers = win_round(membership, word, length, max_power)
        transcript.append({
            "n": length,
            "word": word,
            "won": won,
            "surviving split": survivor,
            "splits": len(answers),
        })

        if not won:
            return False, transcript

    return True, transcript


def survives_pumping(membership, length, words, max_power=6):
    """Check that a language does pump at a given length, as a sanity test.

    Used the other way round: on a regular language every word should have a
    split that survives every exponent. It is what stops the game code from
    "proving" that a regular language is not regular.
    """
    for word in words:
        if len(word) < length or not membership(word):
            continue

        survived = False
        for x, y, z in decompositions(word, length):
            if all(membership(pump(x, y, z, times)) for times in range(max_power + 1)):
                survived = True
                break

        if not survived:
            return False, word

    return True, None


def equal_counts(first="a", second="b"):
    """The membership test for ``a^n b^n``, the standard non-regular example."""
    def membership(word):
        """Whether the word has as many of the first symbol as of the second."""
        count = word.count(first)
        return word == first * count + second * count
    return membership


def palindromes(alphabet="ab"):
    """The membership test for palindromes, non-regular over two or more symbols."""
    def membership(word):
        """Whether the word is a palindrome over the alphabet."""
        return all(character in alphabet for character in word) and word == word[::-1]
    return membership


def squares():
    """The membership test for ``a^(n^2)``, non-regular with sparse witnesses."""
    def membership(word):
        """Whether the word is a run of a's of square length."""
        if set(word) - {"a"}:
            return False
        length = len(word)
        root = int(length ** 0.5)
        return root * root == length
    return membership
