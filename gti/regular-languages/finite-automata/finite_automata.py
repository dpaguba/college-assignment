"""Finite automata: DFA and NFA, the two models the whole first block moves between.

A DFA reads a word and has exactly one choice at each step. An NFA may have
several, or none, and may take epsilon steps that read nothing. Both accept
exactly the regular languages, which is the first real theorem of the course
and the reason the conversions in the neighbouring folders matter.

States are any hashable value, usually strings or frozensets, because the
subset construction produces sets of states and they should stay readable.
"""

from __future__ import annotations

from dataclasses import dataclass, field

EPSILON = ""


@dataclass
class DFA:
    """A deterministic automaton, possibly partial.

    ``transitions`` maps ``(state, symbol)`` to a state. A missing entry means
    the automaton rejects from there, which is the partial case; ``complete``
    fills the gaps with a trap state when a total function is needed.
    """

    states: set
    alphabet: tuple
    transitions: dict
    start: object
    accepting: set
    name: str = "A"

    def step(self, state, symbol):
        """The successor state, or None when the transition is missing."""
        return self.transitions.get((state, symbol))

    def run(self, word):
        """The states passed through, stopping early if the run gets stuck."""
        visited = [self.start]
        current = self.start

        for symbol in word:
            current = self.step(current, symbol)
            if current is None:
                return visited
            visited.append(current)

        return visited

    def accepts(self, word):
        """Whether the automaton accepts the word."""
        current = self.start
        for symbol in word:
            current = self.step(current, symbol)
            if current is None:
                return False
        return current in self.accepting

    def complete(self, trap="trap"):
        """Add a trap state so every transition is defined.

        Needed before complementing: a partial automaton rejects by getting
        stuck, and swapping accepting states would then not swap those words.
        Forgetting this is the classic error in the complement construction.
        """
        if all((state, symbol) in self.transitions
               for state in self.states for symbol in self.alphabet):
            return self

        transitions = dict(self.transitions)
        for state in self.states | {trap}:
            for symbol in self.alphabet:
                transitions.setdefault((state, symbol), trap)

        return DFA(self.states | {trap}, self.alphabet, transitions,
                   self.start, set(self.accepting), f"complete({self.name})")

    def with_alphabet(self, alphabet, trap="trap"):
        """The same language, read over a larger alphabet.

        Every operation that combines two automata needs them to agree on the
        alphabet. Extending is not cosmetic: a symbol the automaton has never
        seen must lead into a trap, and without this step it leads nowhere at
        all, so the automaton gets stuck instead of rejecting. Union and
        complement then quietly lose every word containing that symbol.
        """
        alphabet = tuple(sorted(set(alphabet) | set(self.alphabet)))
        extended = DFA(set(self.states), alphabet, dict(self.transitions),
                       self.start, set(self.accepting), self.name)
        return extended.complete(trap)

    def reachable(self):
        """Every state reachable from the start."""
        seen = {self.start}
        queue = [self.start]

        while queue:
            state = queue.pop()
            for symbol in self.alphabet:
                target = self.step(state, symbol)
                if target is not None and target not in seen:
                    seen.add(target)
                    queue.append(target)

        return seen

    def productive(self):
        """Every state from which an accepting state can still be reached."""
        backwards = {state: set() for state in self.states}
        for (state, _), target in self.transitions.items():
            backwards.setdefault(target, set()).add(state)

        seen = set(self.accepting)
        queue = list(self.accepting)

        while queue:
            state = queue.pop()
            for source in backwards.get(state, ()):
                if source not in seen:
                    seen.add(source)
                    queue.append(source)

        return seen

    def trim(self):
        """Drop states that are unreachable or from which nothing is accepted."""
        keep = self.reachable() & self.productive()
        if self.start not in keep:
            keep = {self.start}

        transitions = {(state, symbol): target
                       for (state, symbol), target in self.transitions.items()
                       if state in keep and target in keep}

        return DFA(keep, self.alphabet, transitions, self.start,
                   self.accepting & keep, f"trim({self.name})")

    def language(self, max_length):
        """Every accepted word up to a length, in shortlex order."""
        found = []
        queue = [""]

        while queue:
            word = queue.pop(0)
            if self.accepts(word):
                found.append(word)
            if len(word) < max_length:
                queue.extend(word + symbol for symbol in self.alphabet)

        return found

    def shortest_word(self):
        """A shortest accepted word, or None when the language is empty."""
        seen = {self.start}
        queue = [(self.start, "")]

        while queue:
            state, word = queue.pop(0)
            if state in self.accepting:
                return word
            for symbol in self.alphabet:
                target = self.step(state, symbol)
                if target is not None and target not in seen:
                    seen.add(target)
                    queue.append((target, word + symbol))

        return None

    def rename(self, prefix="q"):
        """Give the states short names, keeping the structure.

        The subset construction produces frozensets of frozensets, which are
        correct and unreadable. Renaming after a construction is what keeps
        the printed automaton comparable with one drawn by hand.
        """
        order = [self.start] + sorted((state for state in self.states if state != self.start),
                                      key=str)
        names = {state: f"{prefix}{index}" for index, state in enumerate(order)}

        transitions = {(names[state], symbol): names[target]
                       for (state, symbol), target in self.transitions.items()}

        return DFA({names[state] for state in self.states}, self.alphabet, transitions,
                   names[self.start], {names[state] for state in self.accepting}, self.name)

    def to_nfa(self):
        """The same automaton read as a non-deterministic one."""
        transitions = {key: {target} for key, target in self.transitions.items()}
        return NFA(set(self.states), self.alphabet, transitions, {self.start},
                   set(self.accepting), self.name)

    def __str__(self):
        """The transition table, one row per state."""
        rows = [f"{self.name}: start {self.start}, accepting {sorted(self.accepting, key=str)}"]
        for state in sorted(self.states, key=str):
            cells = []
            for symbol in self.alphabet:
                target = self.step(state, symbol)
                cells.append(f"{symbol}->{target if target is not None else '-'}")
            marker = "*" if state in self.accepting else " "
            rows.append(f"  {marker}{state}: " + ", ".join(cells))
        return "\n".join(rows)


@dataclass
class NFA:
    """A non-deterministic automaton with epsilon transitions.

    ``transitions`` maps ``(state, symbol)`` to a **set** of states, and the
    empty string is used as the symbol for an epsilon step.
    """

    states: set
    alphabet: tuple
    transitions: dict
    start: set
    accepting: set
    name: str = "N"

    def step(self, state, symbol):
        """Every state reachable from one state by one symbol, without closure."""
        return set(self.transitions.get((state, symbol), set()))

    def epsilon_closure(self, states):
        """Every state reachable by epsilon steps alone.

        The operation that makes epsilon transitions harmless: a set of states
        is always kept closed under them, so the rest of the machinery can
        pretend they do not exist.
        """
        closure = set(states)
        queue = list(states)

        while queue:
            state = queue.pop()
            for target in self.transitions.get((state, EPSILON), set()):
                if target not in closure:
                    closure.add(target)
                    queue.append(target)

        return closure

    def move(self, states, symbol):
        """The closed set of states reached from a set by one symbol."""
        targets = set()
        for state in self.epsilon_closure(states):
            targets |= self.step(state, symbol)
        return self.epsilon_closure(targets)

    def accepts(self, word):
        """Whether some run on the word ends in an accepting state."""
        current = self.epsilon_closure(self.start)
        for symbol in word:
            current = self.move(current, symbol)
            if not current:
                return False
        return bool(current & self.accepting)

    def language(self, max_length):
        """Every accepted word up to a length."""
        found = []
        queue = [""]

        while queue:
            word = queue.pop(0)
            if self.accepts(word):
                found.append(word)
            if len(word) < max_length:
                queue.extend(word + symbol for symbol in self.alphabet)

        return found

    def rename(self, prefix="n"):
        """Give the states short names, keeping the structure."""
        order = sorted(self.states, key=str)
        names = {state: f"{prefix}{index}" for index, state in enumerate(order)}

        transitions = {}
        for (state, symbol), targets in self.transitions.items():
            transitions[(names[state], symbol)] = {names[target] for target in targets}

        return NFA({names[state] for state in self.states}, self.alphabet, transitions,
                   {names[state] for state in self.start},
                   {names[state] for state in self.accepting}, self.name)

    def __str__(self):
        """The transition table, with sets of targets per cell."""
        rows = [f"{self.name}: start {sorted(self.start, key=str)}, "
                f"accepting {sorted(self.accepting, key=str)}"]
        for state in sorted(self.states, key=str):
            cells = []
            for symbol in tuple(self.alphabet) + (EPSILON,):
                targets = self.transitions.get((state, symbol))
                if targets:
                    label = symbol if symbol else "eps"
                    cells.append(f"{label}->{sorted(targets, key=str)}")
            marker = "*" if state in self.accepting else " "
            rows.append(f"  {marker}{state}: " + (", ".join(cells) if cells else "-"))
        return "\n".join(rows)


def dfa_from_table(table, start, accepting, alphabet=None, name="A"):
    """Build a DFA from a nested dictionary, which is how the sheets write them.

    ``table`` maps a state to a dictionary from symbol to target, exactly the
    shape of the tables in the exercises.
    """
    states = set(table)
    symbols = alphabet or tuple(sorted({symbol for row in table.values() for symbol in row}))

    transitions = {}
    for state, row in table.items():
        for symbol, target in row.items():
            transitions[(state, symbol)] = target
            states.add(target)

    return DFA(states, tuple(symbols), transitions, start, set(accepting), name)


def nfa_from_table(table, start, accepting, alphabet=None, name="N"):
    """Build an NFA from a nested dictionary of sets."""
    states = set(table)
    symbols = alphabet or tuple(sorted({symbol for row in table.values() for symbol in row
                                        if symbol != EPSILON}))

    transitions = {}
    for state, row in table.items():
        for symbol, targets in row.items():
            transitions[(state, symbol)] = set(targets)
            states |= set(targets)

    return NFA(states, tuple(symbols), transitions, set(start), set(accepting), name)
