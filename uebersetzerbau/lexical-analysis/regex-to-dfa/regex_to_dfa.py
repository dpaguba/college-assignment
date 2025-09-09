"""From a regular expression to a deterministic automaton.

The first phase of a compiler is a decision procedure: given the next
characters of the input, which token is this. The specification is written as
regular expressions and the implementation is a table-driven automaton, and the
path between them is mechanical, which is why lexers are generated rather than
written.

Three steps: rewrite the extended operators away, build an epsilon-NFA by
Thompson's patterns, determinise by the subset construction. The theory behind
the last two lives in `gti/regular-languages/`; what is added here is the
lecture's state numbering convention and the machinery the scanner needs.
"""

from __future__ import annotations


class NFA:
    """A nondeterministic automaton with epsilon transitions.

    Transitions map a state and a symbol to a set of states, with `None` as the
    symbol standing for an epsilon move.
    """

    def __init__(self, start, accepting, transitions, states):
        """Store the start state, the accepting states and the transitions."""
        self.start = start
        self.accepting = set(accepting)
        self.transitions = transitions
        self.states = set(states)

    def move(self, states, symbol):
        """States reachable from a set by reading one symbol."""
        result = set()
        for state in states:
            result |= self.transitions.get((state, symbol), set())
        return result

    def epsilon_closure(self, states):
        """All states reachable without reading anything.

        The fixed point of following epsilon edges. Both the subset
        construction and direct NFA simulation are built on it, which is why it
        is a method rather than a helper inside one of them.
        """
        stack = list(states)
        seen = set(states)

        while stack:
            state = stack.pop()
            for target in self.transitions.get((state, None), set()):
                if target not in seen:
                    seen.add(target)
                    stack.append(target)

        return seen

    def accepts(self, word):
        """Simulate the automaton directly, without determinising it."""
        current = self.epsilon_closure({self.start})
        for symbol in word:
            current = self.epsilon_closure(self.move(current, symbol))
            if not current:
                return False
        return bool(current & self.accepting)


class DFA:
    """A deterministic automaton, with a partial transition function.

    A missing transition means the word is rejected. Adding an explicit trap
    state would make the function total and the automaton bigger for no gain,
    since the scanner needs to know when it has run out of moves anyway.
    """

    def __init__(self, start, accepting, transitions, states):
        """Store the start state, the accepting states and the transitions."""
        self.start = start
        self.accepting = set(accepting)
        self.transitions = transitions
        self.states = set(states)

    def step(self, state, symbol):
        """The successor state, or `None` if there is none."""
        return self.transitions.get((state, symbol))

    def accepts(self, word):
        """Whether the automaton accepts a word."""
        state = self.start
        for symbol in word:
            state = self.step(state, symbol)
            if state is None:
                return False
        return state in self.accepting

    def longest_match(self, text, position=0):
        """Length of the longest accepted prefix starting at a position.

        `None` when no prefix is accepted, including the empty one. This is the
        operation the scanner is built on, and the reason the automaton has to
        keep running after an accepting state rather than stopping there: a
        longer match may still be ahead.
        """
        state = self.start
        best = None
        if state in self.accepting:
            best = 0

        for offset in range(position, len(text)):
            state = self.step(state, text[offset])
            if state is None:
                break
            if state in self.accepting:
                best = offset - position + 1

        return best


def expand(pattern):
    """Rewrite the extended operators into the three basic ones.

    `a+` becomes `a.a*` and `a?` becomes `(a|)`, exactly as the lecture
    requires before Thompson's construction is applied. Both are definitions
    rather than approximations, so nothing is lost, and the resulting automaton
    is the one the lecture's numbering convention refers to.
    """
    result = []
    index = 0

    while index < len(pattern):
        character = pattern[index]

        if character in "+?" and result:
            operand = _last_operand(result)
            if character == "+":
                result.extend(["."] + operand + ["*"])
            else:
                result = result[:len(result) - len(operand)]
                result.extend(["("] + operand + ["|", ")"])
        else:
            result.append(character)

        index += 1

    return "".join(result)


def _last_operand(tokens):
    """The tokens forming the operand a postfix operator applies to."""
    if tokens[-1] == ")":
        depth = 0
        for index in range(len(tokens) - 1, -1, -1):
            if tokens[index] == ")":
                depth += 1
            elif tokens[index] == "(":
                depth -= 1
                if depth == 0:
                    return tokens[index:]
    if tokens[-1] == "*":
        return _last_operand(tokens[:-1]) + ["*"]
    return [tokens[-1]]


def parse(pattern):
    """Parse a regular expression into a syntax tree.

    Recursive descent over the usual three levels: alternation binds loosest,
    then concatenation, then the postfix star. Concatenation may be written
    with an explicit dot, as the lecture does, or by juxtaposition.
    """
    state = {"text": pattern, "position": 0}
    tree = _alternation(state)
    if state["position"] != len(pattern):
        raise ValueError(f"unexpected character at {state['position']}")
    return tree


def _alternation(state):
    """Parse a sequence of concatenations separated by the alternation bar."""
    branches = [_concatenation(state)]
    while _peek(state) == "|":
        _advance(state)
        branches.append(_concatenation(state))
    return branches[0] if len(branches) == 1 else ("alt", branches)


def _concatenation(state):
    """Parse a sequence of starred atoms, with or without explicit dots."""
    parts = []
    while True:
        character = _peek(state)
        if character is None or character in "|)":
            break
        if character == ".":
            _advance(state)
            continue
        parts.append(_star(state))

    if not parts:
        return ("empty",)
    return parts[0] if len(parts) == 1 else ("cat", parts)


def _star(state):
    """Parse an atom followed by any number of stars."""
    node = _atom(state)
    while _peek(state) == "*":
        _advance(state)
        node = ("star", node)
    return node


def _atom(state):
    """Parse a parenthesised expression or a single symbol."""
    character = _peek(state)
    if character == "(":
        _advance(state)
        node = _alternation(state)
        if _peek(state) != ")":
            raise ValueError("missing closing parenthesis")
        _advance(state)
        return node
    if character is None:
        return ("empty",)
    _advance(state)
    return ("symbol", character)


def _peek(state):
    """The next character, or `None` at the end."""
    if state["position"] >= len(state["text"]):
        return None
    return state["text"][state["position"]]


def _advance(state):
    """Consume one character."""
    state["position"] += 1


def thompson(pattern):
    """Build an epsilon-NFA from a regular expression by Thompson's patterns.

    Every fragment keeps one start state and one accepting state, with nothing
    entering the start and nothing leaving the accepting one, so fragments
    compose without interfering. The start state of the whole automaton is
    numbered 0 and the rest ascend in the direction of the arrows, which is the
    numbering the lecture's figures use.
    """
    tree = parse(pattern)
    counter = {"next": 0}
    transitions = {}
    start, accept = build_fragment(tree, counter, transitions)
    states = set(range(counter["next"]))
    return NFA(start, {accept}, transitions, states)


def build_fragment(node, counter, transitions):
    """Construct the fragment for one syntax tree node, returning its ends.

    Exposed because a lexer generator merges several expressions into one
    automaton and therefore needs to build fragments into a shared transition
    table with a shared state counter, rather than one automaton per pattern.
    """
    kind = node[0]

    if kind == "symbol":
        start, accept = _fresh(counter), _fresh(counter)
        _add(transitions, start, node[1], accept)
        return start, accept

    if kind == "empty":
        start, accept = _fresh(counter), _fresh(counter)
        _add(transitions, start, None, accept)
        return start, accept

    if kind == "cat":
        first_start, first_accept = build_fragment(node[1][0], counter, transitions)
        current = first_accept
        for part in node[1][1:]:
            part_start, part_accept = build_fragment(part, counter, transitions)
            _add(transitions, current, None, part_start)
            current = part_accept
        return first_start, current

    if kind == "alt":
        start = _fresh(counter)
        ends = []
        for branch in node[1]:
            branch_start, branch_accept = build_fragment(branch, counter, transitions)
            _add(transitions, start, None, branch_start)
            ends.append(branch_accept)
        accept = _fresh(counter)
        for end in ends:
            _add(transitions, end, None, accept)
        return start, accept

    start = _fresh(counter)
    inner_start, inner_accept = build_fragment(node[1], counter, transitions)
    accept = _fresh(counter)
    _add(transitions, start, None, inner_start)
    _add(transitions, start, None, accept)
    _add(transitions, inner_accept, None, inner_start)
    _add(transitions, inner_accept, None, accept)
    return start, accept


def _fresh(counter):
    """Allocate the next state number."""
    number = counter["next"]
    counter["next"] += 1
    return number


def _add(transitions, source, symbol, target):
    """Record one transition."""
    transitions.setdefault((source, symbol), set()).add(target)


def alphabet_of(nfa):
    """The symbols the automaton actually reads, excluding epsilon."""
    return sorted({symbol for _, symbol in nfa.transitions if symbol is not None})


def determinise(nfa):
    """The subset construction: a DFA state is a set of NFA states.

    Exponential in the worst case and mild in practice, because most subsets
    are unreachable. The reachable subsets are exactly what the algorithm
    enumerates, which is why it is written as a worklist rather than as a loop
    over the power set.
    """
    alphabet = alphabet_of(nfa)
    start = frozenset(nfa.epsilon_closure({nfa.start}))

    states = {start: 0}
    transitions = {}
    worklist = [start]

    while worklist:
        current = worklist.pop()
        for symbol in alphabet:
            target = frozenset(nfa.epsilon_closure(nfa.move(current, symbol)))
            if not target:
                continue
            if target not in states:
                states[target] = len(states)
                worklist.append(target)
            transitions[(states[current], symbol)] = states[target]

    accepting = {number for subset, number in states.items() if subset & nfa.accepting}
    return DFA(0, accepting, transitions, set(states.values()))


def compile_regex(pattern):
    """The whole path from an expression to a deterministic automaton."""
    return determinise(thompson(expand(pattern)))


def minimise(dfa):
    """Merge states that no word can distinguish, by table filling.

    Two states are equivalent when no word leads one to acceptance and the
    other to rejection. Marking pairs that differ and propagating backwards
    until nothing changes leaves the equivalence classes, and the quotient
    automaton is the unique smallest one for the language.
    """
    states = sorted(dfa.states)
    alphabet = sorted({symbol for _, symbol in dfa.transitions})

    trap = max(states) + 1 if states else 0
    complete = dict(dfa.transitions)
    for state in states + [trap]:
        for symbol in alphabet:
            complete.setdefault((state, symbol), trap)
    working = states + [trap]

    distinct = set()
    for first in working:
        for second in working:
            if first < second and ((first in dfa.accepting) != (second in dfa.accepting)):
                distinct.add((first, second))

    changed = True
    while changed:
        changed = False
        for first in working:
            for second in working:
                if first >= second or (first, second) in distinct:
                    continue
                for symbol in alphabet:
                    a, b = complete[(first, symbol)], complete[(second, symbol)]
                    if a != b and (min(a, b), max(a, b)) in distinct:
                        distinct.add((first, second))
                        changed = True
                        break

    classes = {}
    for state in working:
        for representative in classes:
            pair = (min(state, representative), max(state, representative))
            if state != representative and pair not in distinct:
                classes[state] = classes[representative]
                break
        else:
            classes[state] = len(set(classes.values()))

    reachable = {classes[dfa.start]}
    frontier = [dfa.start]
    seen = {dfa.start}
    new_transitions = {}

    while frontier:
        state = frontier.pop()
        for symbol in alphabet:
            target = complete[(state, symbol)]
            if target == trap and trap not in dfa.states:
                continue
            new_transitions[(classes[state], symbol)] = classes[target]
            reachable.add(classes[target])
            if target not in seen:
                seen.add(target)
                frontier.append(target)

    accepting = {classes[state] for state in dfa.accepting}
    return DFA(classes[dfa.start], accepting, new_transitions, reachable)


def follows_rule(word):
    """Whether every `a` is followed by two more `a`s or by one or two `b`s.

    The rule from sheet 1, checked literally against the wording rather than
    through an automaton, so that the regular expression proposed in the
    solution can be compared against the specification instead of against
    itself.

    Reading it literally is what makes the solution's remark provable: the
    first alternative can never be satisfied by a finite word, because the
    last `a` of any run has fewer than two `a`s after it. So in practice every
    `a` must be followed by a run of exactly one or two `b`s, and `abbb`, which
    the expression `(b|abb?)*` wrongly generates, is not in the language.
    """
    for index, character in enumerate(word):
        if character != "a":
            continue

        rest = word[index + 1:]
        if rest.startswith("aa"):
            continue

        run = 0
        while run < len(rest) and rest[run] == "b":
            run += 1
        if run not in (1, 2):
            return False

    return True
