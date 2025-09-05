"""A lexer generator: one automaton for the whole token specification.

Running one automaton per rule is correct and wasteful, because every rule
re-reads the same characters. A generator instead merges all the rules into a
single NFA with one fresh start state and epsilon edges into each rule's
fragment, determinises that once, and labels each accepting state with the
highest-priority rule whose accepting state it contains.

The result is what lex and flex produce: a table, and a driver loop that reads
characters, remembers the last accepting state it passed, and backs up to it
when it gets stuck.
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


class ScanError(Exception):
    """No rule matched a non-empty prefix at this position."""

    def __init__(self, position, character):
        """Record the position and the character no rule could start with."""
        super().__init__(f"no token matches at position {position}: {character!r}")
        self.position = position
        self.character = character


class Lexer:
    """A generated scanner: one DFA plus a rule label per accepting state."""

    def __init__(self, rules):
        """Merge the rules into one automaton and label its accepting states."""
        self.rules = list(rules)
        self.dfa, self.labels = _generate(self.rules)

    def scan(self, text):
        """Split the input into tokens by maximum munch."""
        tokens = []
        position = 0

        while position < len(text):
            name, length = self._longest(text, position)
            if name is None:
                raise ScanError(position, text[position])
            tokens.append(Token(name, text[position:position + length], position))
            position += length

        return tokens

    def _longest(self, text, position):
        """Run the automaton forward, remembering the last accepting state.

        This is the backup rule. The automaton keeps reading past an accepting
        state because a longer match may follow, and when it finally gets
        stuck, the scanner returns to the last position where it was accepting.
        Without the backup, `abab` against the rules `ab` and `abcd` would fail
        at the third character instead of yielding two tokens.
        """
        state = self.dfa.start
        best_name, best_length = None, 0

        if state in self.labels:
            best_name, best_length = self.labels[state], 0

        for offset in range(position, len(text)):
            state = self.dfa.step(state, text[offset])
            if state is None:
                break
            if state in self.labels:
                best_name = self.labels[state]
                best_length = offset - position + 1

        if best_length == 0:
            return None, 0
        return best_name, best_length

    def statistics(self):
        """Size of the generated table, which is what a generator reports."""
        return {
            "rules": len(self.rules),
            "states": len(self.dfa.states),
            "accepting": len(self.labels),
            "transitions": len(self.dfa.transitions),
        }


def _generate(rules):
    """Build the combined automaton and the accepting-state labels.

    The subset construction is repeated here rather than reused, because the
    labels have to be read off the NFA state sets: a DFA state is accepting for
    whichever rules its subset contains an accepting state of, and priority
    picks among them.
    """
    transitions = {}
    counter = {"next": 1}
    accepting_of = {}

    for name, pattern in rules:
        tree = rx.parse(rx.expand(pattern))
        start, accept = rx.build_fragment(tree, counter, transitions)
        transitions.setdefault((0, None), set()).add(start)
        accepting_of[accept] = name

    nfa = rx.NFA(0, set(accepting_of), transitions, set(range(counter["next"])))
    priority = {name: index for index, (name, _) in enumerate(rules)}

    alphabet = rx.alphabet_of(nfa)
    start_set = frozenset(nfa.epsilon_closure({0}))
    numbers = {start_set: 0}
    dfa_transitions = {}
    worklist = [start_set]

    while worklist:
        current = worklist.pop()
        for symbol in alphabet:
            target = frozenset(nfa.epsilon_closure(nfa.move(current, symbol)))
            if not target:
                continue
            if target not in numbers:
                numbers[target] = len(numbers)
                worklist.append(target)
            dfa_transitions[(numbers[current], symbol)] = numbers[target]

    labels = {}
    for subset, number in numbers.items():
        winners = [accepting_of[state] for state in subset if state in accepting_of]
        if winners:
            labels[number] = min(winners, key=lambda name: priority[name])

    dfa = rx.DFA(0, set(labels), dfa_transitions, set(numbers.values()))
    return dfa, labels


def table(lexer):
    """The transition table as rows, the form a generator would emit.

    Printing it is the point of the exercise: a generated scanner is a table
    and a twenty-line driver, and seeing the table makes clear that the
    regular expressions have disappeared entirely by run time.
    """
    alphabet = sorted({symbol for _, symbol in lexer.dfa.transitions})
    rows = []

    for state in sorted(lexer.dfa.states):
        row = {"state": state, "accepts": lexer.labels.get(state)}
        for symbol in alphabet:
            row[symbol] = lexer.dfa.step(state, symbol)
        rows.append(row)

    return alphabet, rows
