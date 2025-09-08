"""Scanning by maximum munch: longest match wins, priority breaks ties.

A token specification is a list of named regular expressions, and the scanner
repeatedly consumes the longest prefix of the remaining input that any of them
accepts. Two rules decide everything:

- **longest match**: among all specifications that match a prefix, the one with
  the longest prefix wins, regardless of the order they were written in
- **priority**: among matches of equal length, the specification listed first
  wins

Both are needed and neither is arbitrary. Longest match is why `iffa` is one
identifier and not the keyword `if` followed by `fa`. Priority is why `if` is
the keyword and not an identifier, since both match exactly two characters.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "regex-to-dfa"))
import regex_to_dfa as rx


class Token:
    """One scanned token: which rule matched, what text, and where."""

    def __init__(self, name, lexeme, position):
        """Record which rule matched, the matched text and its position."""
        self.name = name
        self.lexeme = lexeme
        self.position = position

    def __repr__(self):
        """Short form naming the rule and the matched text."""
        return f"Token({self.name}, {self.lexeme!r}, at {self.position})"

    def __eq__(self, other):
        """Two tokens are equal when rule, text and position agree."""
        return (isinstance(other, Token) and self.name == other.name
                and self.lexeme == other.lexeme and self.position == other.position)


class ScanError(Exception):
    """No specification matched a non-empty prefix at this position.

    The position is carried because that is the only useful part of a lexical
    error message: the character that could not start any token.
    """

    def __init__(self, position, character):
        """Record the position and the character no rule could start with."""
        super().__init__(f"no token matches at position {position}: {character!r}")
        self.position = position
        self.character = character


def build(rules):
    """Compile each specification into its own deterministic automaton.

    One automaton per rule rather than one combined automaton. That keeps the
    priority rule trivial to state, at the cost of running every automaton at
    every position. The combined form, which a real generator uses, is in
    [lexer-generator](../lexer-generator/).
    """
    return [(name, rx.compile_regex(pattern)) for name, pattern in rules]


def scan(rules, text):
    """Split the whole input into tokens, or raise where nothing matches."""
    automata = build(rules)
    tokens = []
    position = 0

    while position < len(text):
        name, length = _longest(automata, text, position)
        if name is None:
            raise ScanError(position, text[position])
        tokens.append(Token(name, text[position:position + length], position))
        position += length

    return tokens


def _longest(automata, text, position):
    """The winning rule and match length at one position, or `(None, 0)`.

    A match of length zero is not a match. A rule whose language contains the
    empty word would otherwise win every position and the scanner would never
    advance, which is the classic way a hand-written lexer hangs.
    """
    best_name, best_length = None, 0

    for name, dfa in automata:
        length = dfa.longest_match(text, position)
        if length is not None and length > best_length:
            best_name, best_length = name, length

    return best_name, best_length


def matches(pattern, word):
    """Whether one specification accepts a word exactly."""
    return rx.compile_regex(pattern).accepts(word)


def trace(rules, text):
    """The whole decision at every position, for explaining a tokenisation.

    Reports, per token, how far each rule could match, which one won and
    whether it won on length or on priority. This is what makes an unexpected
    tokenisation explainable rather than merely surprising.
    """
    automata = build(rules)
    steps = []
    position = 0

    while position < len(text):
        lengths = {}
        for name, dfa in automata:
            length = dfa.longest_match(text, position)
            if length:
                lengths[name] = length

        if not lengths:
            raise ScanError(position, text[position])

        best = max(lengths.values())
        candidates = [name for name, _ in automata if lengths.get(name) == best]
        winner = candidates[0]

        steps.append({
            "position": position,
            "lengths": lengths,
            "winner": winner,
            "lexeme": text[position:position + best],
            "by_priority": len(candidates) > 1,
            "beaten_by_priority": candidates[1:],
        })
        position += best

    return steps
