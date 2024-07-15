"""What regular languages are actually used for: searching and tokenising.

The theory pays off in two places the course names. A pattern becomes an
automaton, and then finding it in a text costs one pass with no backtracking;
several patterns become one automaton, and then a lexer is a single scan that
decides which token it is looking at while it reads.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "finite-automata"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "regular-expressions"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "subset-construction"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "thompson-construction"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "minimisation"))

from finite_automata import DFA, EPSILON, NFA
from minimisation import minimise
from regular_expressions import parse
from subset_construction import determinise
from thompson_construction import build


def search_automaton(pattern, alphabet):
    """A DFA that accepts exactly the texts containing the pattern somewhere.

    Built from the expression ``S* p S*`` over the given alphabet, then
    determinised and minimised. The result scans a text in one pass with no
    backtracking, which is the property that separates automaton matching from
    the backtracking regex engines that can be made exponentially slow.
    """
    any_symbol = "|".join(alphabet)
    expression = parse(f"({any_symbol})*({pattern})({any_symbol})*")
    return minimise(determinise(build(expression)), name=f"search({pattern})")


def occurrences(pattern, text, alphabet=None):
    """Every position where the pattern matches, by running one automaton.

    The automaton for the pattern alone is run from every position, which is
    the straightforward version and costs O(n * m). The single-pass variant
    keeps the state of the search automaton instead, and finds the **ends** of
    matches without restarting; it is what ``matches_prefix`` supports below.
    """
    alphabet = alphabet or sorted(set(text) | set(pattern) - set("()|*+?"))
    automaton = minimise(determinise(build(parse(pattern))))

    found = []
    for start in range(len(text) + 1):
        for end in range(start, len(text) + 1):
            if automaton.accepts(text[start:end]) and end > start:
                found.append((start, text[start:end]))
                break

    return found


@dataclass
class Token:
    """One token: its kind, its text, and where it started."""

    kind: str
    text: str
    position: int

    def __str__(self):
        """The kind, the text and the position, as the tests print them."""
        return f"{self.kind}({self.text!r})@{self.position}"


class Lexer:
    """A longest-match tokeniser built from one automaton per token kind.

    Two rules decide what a scanner does, and both are in ``next_token``:

    - **longest match**: the scanner keeps reading while any automaton could
      still accept, and reports the longest prefix that some automaton did
      accept, which is why ``iff`` is one identifier and not ``if`` followed by
      ``f``
    - **priority**: when several kinds match the same longest prefix, the one
      declared first wins, which is how keywords beat identifiers

    Both rules are conventions, not consequences of the theory. The theory only
    says that each kind is a regular language.
    """

    def __init__(self, rules, alphabet=None):
        """Compiles every rule into a minimal automaton once, at construction."""
        self.rules = [(kind, minimise(determinise(build(parse(pattern)))))
                      for kind, pattern in rules]
        self.alphabet = alphabet

    def next_token(self, text, position):
        """The longest token starting at a position, or None."""
        best = None

        for end in range(position + 1, len(text) + 1):
            candidate = text[position:end]
            for kind, automaton in self.rules:
                if automaton.accepts(candidate):
                    best = Token(kind, candidate, position)
                    break

        return best

    def tokenise(self, text, skip=" \t\n"):
        """Split a whole text into tokens, or raise at the first character that fits none."""
        tokens = []
        position = 0

        while position < len(text):
            if text[position] in skip:
                position += 1
                continue

            token = self.next_token(text, position)
            if token is None:
                raise ValueError(f"no token matches at position {position}: {text[position]!r}")

            tokens.append(token)
            position += len(token.text)

        return tokens


def word_count_automaton(words, alphabet):
    """One automaton recognising any of several words.

    The union of the individual patterns, determinised once. Scanning for
    twenty patterns then costs exactly what scanning for one costs, which is
    the reason this construction exists at all and the idea behind
    Aho-Corasick.
    """
    pattern = "|".join(words)
    return minimise(determinise(build(parse(pattern))), name=f"words({len(words)})")
