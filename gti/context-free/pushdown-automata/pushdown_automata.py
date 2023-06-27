"""Pushdown automata: a finite automaton with a stack.

The stack is the whole difference from the first block, and it is exactly what
lets a machine count. ``a^n b^n`` is impossible for a finite automaton and easy
here: push on every a, pop on every b, and check the stack is empty.

A transition reads a state, an input symbol or nothing, and the top of the
stack, and it produces a new state and a string that replaces that top symbol.
Nondeterminism is essential, not a convenience: deterministic pushdown automata
accept strictly fewer languages, and palindromes are the standard example of
the gap.

Two acceptance modes exist and are equally expressive:

- by **final state**: the run ends in an accepting state
- by **empty stack**: the run ends with nothing on the stack

The conversions between them are short and are here as well.
"""

from __future__ import annotations

from dataclasses import dataclass, field

EPSILON = ""


@dataclass
class PDA:
    """A nondeterministic pushdown automaton.

    ``transitions`` maps ``(state, input symbol, stack top)`` to a set of
    ``(next state, pushed string)``. The pushed string replaces the popped
    symbol, leftmost character ending up on top, so ``("q", "AB")`` leaves A
    above B.
    """

    states: set
    input_alphabet: tuple
    stack_alphabet: tuple
    transitions: dict
    start: str
    start_stack: str
    accepting: set = field(default_factory=set)
    mode: str = "final"
    name: str = "P"

    def moves(self, state, symbol, stack):
        """Every configuration reachable in one step."""
        if not stack:
            return []

        top = stack[0]
        found = []

        for target, pushed in self.transitions.get((state, symbol, top), ()):
            found.append((target, pushed + stack[1:]))

        return found

    def accepts(self, word, limit=4000):
        """Whether some run accepts the word.

        Breadth-first over configurations, with a limit because a pushdown
        automaton can loop on epsilon moves for ever while the stack grows.
        The limit turns non-termination into a rejection, which is accurate for
        a simulator and is why membership is decided by
        [CYK](../cyk/) rather than by running the machine.
        """
        start = (self.start, word, self.start_stack)
        seen = {start}
        queue = [start]
        steps = 0

        while queue and steps < limit:
            steps += 1
            state, rest, stack = queue.pop(0)

            if self._accepting(state, rest, stack):
                return True

            for symbol, remaining in self._readable(rest):
                for target, new_stack in self.moves(state, symbol, stack):
                    following = (target, remaining, new_stack)
                    if following not in seen and len(new_stack) <= len(word) + 5:
                        seen.add(following)
                        queue.append(following)

        return False

    def _readable(self, rest):
        """The epsilon move and, if input remains, the next symbol."""
        options = [(EPSILON, rest)]
        if rest:
            options.append((rest[0], rest[1:]))
        return options

    def _accepting(self, state, rest, stack):
        """Whether the configuration accepts under the automaton's mode."""
        if rest:
            return False
        if self.mode == "empty":
            return not stack
        return state in self.accepting

    def run_tree(self, word, limit=200):
        """Every configuration reached, for drawing the search by hand."""
        start = (self.start, word, self.start_stack)
        seen = {start}
        order = [start]
        queue = [start]

        while queue and len(order) < limit:
            state, rest, stack = queue.pop(0)
            for symbol, remaining in self._readable(rest):
                for target, new_stack in self.moves(state, symbol, stack):
                    following = (target, remaining, new_stack)
                    if following not in seen and len(new_stack) <= len(word) + 5:
                        seen.add(following)
                        order.append(following)
                        queue.append(following)

        return order

    def language(self, max_length, alphabet=None):
        """Every accepted word up to a length."""
        alphabet = sorted(alphabet or self.input_alphabet)
        found = []
        queue = [""]

        while queue:
            word = queue.pop(0)
            if self.accepts(word):
                found.append(word)
            if len(word) < max_length:
                queue.extend(word + symbol for symbol in alphabet)

        return found

    def __str__(self):
        """The transition table, one row per rule."""
        rows = [f"{self.name}: start {self.start}, stack start {self.start_stack}, "
                f"acceptance by {self.mode}"
                + (f", accepting {sorted(self.accepting)}" if self.mode == "final" else "")]

        for (state, symbol, top), targets in sorted(self.transitions.items(),
                                                    key=lambda item: str(item[0])):
            read = symbol if symbol else "eps"
            for target, pushed in sorted(targets):
                rows.append(f"  ({state}, {read}, {top}) -> ({target}, {pushed or 'eps'})")

        return "\n".join(rows)


def to_empty_stack(pda, name=None):
    """Convert acceptance by final state into acceptance by empty stack.

    A new bottom marker is pushed under everything so the machine can tell its
    own empty stack from the user's, and from every accepting state an epsilon
    move drains whatever is left. Without the marker the automaton could empty
    the stack in the middle of a run and accept a prefix.
    """
    if pda.mode == "empty":
        return pda

    bottom = "#"
    while bottom in pda.stack_alphabet:
        bottom += "#"

    transitions = {key: set(value) for key, value in pda.transitions.items()}
    new_start = "<start>"
    drain = "<drain>"

    transitions[(new_start, EPSILON, bottom)] = {(pda.start, pda.start_stack + bottom)}

    for state in pda.accepting:
        for symbol in tuple(pda.stack_alphabet) + (bottom,):
            transitions.setdefault((state, EPSILON, symbol), set()).add((drain, ""))

    for symbol in tuple(pda.stack_alphabet) + (bottom,):
        transitions.setdefault((drain, EPSILON, symbol), set()).add((drain, ""))

    return PDA(set(pda.states) | {new_start, drain}, pda.input_alphabet,
               tuple(pda.stack_alphabet) + (bottom,), transitions, new_start, bottom,
               set(), "empty", name or f"empty({pda.name})")


def to_final_state(pda, name=None):
    """Convert acceptance by empty stack into acceptance by final state.

    The mirror image: a marker below everything, and an accepting state
    reached exactly when that marker becomes the top, which happens only when
    the original stack is gone.
    """
    if pda.mode == "final":
        return pda

    bottom = "#"
    while bottom in pda.stack_alphabet:
        bottom += "#"

    transitions = {key: set(value) for key, value in pda.transitions.items()}
    new_start = "<start>"
    accept = "<accept>"

    transitions[(new_start, EPSILON, bottom)] = {(pda.start, pda.start_stack + bottom)}
    transitions.setdefault((pda.start, EPSILON, bottom), set())

    for state in pda.states:
        transitions.setdefault((state, EPSILON, bottom), set()).add((accept, ""))

    return PDA(set(pda.states) | {new_start, accept}, pda.input_alphabet,
               tuple(pda.stack_alphabet) + (bottom,), transitions, new_start, bottom,
               {accept}, "final", name or f"final({pda.name})")


def balanced_parentheses():
    """The standard example: correctly nested brackets, by empty stack."""
    transitions = {
        ("q", "(", "Z"): {("q", "AZ")},
        ("q", "(", "A"): {("q", "AA")},
        ("q", ")", "A"): {("q", "")},
        ("q", EPSILON, "Z"): {("q", "")},
    }
    return PDA({"q"}, ("(", ")"), ("Z", "A"), transitions, "q", "Z",
               set(), "empty", "balanced")


def equal_counts():
    """``a^n b^n`` accepted by final state, the classic non-regular language."""
    transitions = {
        ("push", "a", "Z"): {("push", "AZ")},
        ("push", "a", "A"): {("push", "AA")},
        ("push", "b", "A"): {("pop", "")},
        ("pop", "b", "A"): {("pop", "")},
        ("pop", EPSILON, "Z"): {("done", "Z")},
    }
    return PDA({"push", "pop", "done"}, ("a", "b"), ("Z", "A"), transitions,
               "push", "Z", {"done"}, "final", "a^n b^n")


def palindromes(alphabet=("a", "b")):
    """Even-length palindromes, which need real nondeterminism.

    The machine has to guess where the middle is, and no deterministic pushdown
    automaton can accept this language. It is the standard witness that
    deterministic and nondeterministic pushdown automata differ, unlike finite
    automata where the subset construction removes the difference.
    """
    transitions = {}

    for symbol in alphabet:
        transitions.setdefault(("push", symbol, "Z"), set()).add(("push", symbol.upper() + "Z"))
        for stacked in alphabet:
            transitions.setdefault(("push", symbol, stacked.upper()), set()).add(
                ("push", symbol.upper() + stacked.upper()))
        transitions.setdefault(("push", EPSILON, "Z"), set()).add(("match", "Z"))
        for stacked in alphabet:
            transitions.setdefault(("push", EPSILON, stacked.upper()), set()).add(
                ("match", stacked.upper()))
        transitions.setdefault(("match", symbol, symbol.upper()), set()).add(("match", ""))

    transitions.setdefault(("match", EPSILON, "Z"), set()).add(("done", "Z"))

    return PDA({"push", "match", "done"}, tuple(alphabet),
               ("Z",) + tuple(symbol.upper() for symbol in alphabet),
               transitions, "push", "Z", {"done"}, "final", "palindromes")
