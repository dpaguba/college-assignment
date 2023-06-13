"""What context-free languages survive, and what breaks them.

Closed under union, concatenation and star, and **not** closed under
intersection or complement. That asymmetry is the main structural difference
from the regular level, where everything was closed.

The witness is short: ``a^i b^i c^j`` and ``a^i b^j c^j`` are both
context-free, and their intersection is ``a^n b^n c^n``, which the
[pumping lemma](../cfl-pumping-lemma/) shows is not. Complement follows,
because closure under complement and union would give closure under
intersection by De Morgan.

Intersection with a **regular** language is a different matter and does hold,
which is what makes it the usual tool for proving a language non-context-free:
intersect with something regular until what is left is a known bad case.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "context-free-grammars"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "grammar-cleanup"))

from context_free_grammars import Grammar
from grammar_cleanup import remove_useless


def _rename(grammar, prefix):
    """Give every variable a prefix so two grammars can be merged safely."""
    mapping = {variable: f"{prefix}{variable}" for variable in grammar.variables}
    rules = {}

    for variable, sides in grammar.rules.items():
        rules[mapping[variable]] = [
            tuple(mapping.get(symbol, symbol) for symbol in right) for right in sides]

    return Grammar(set(mapping.values()), set(grammar.terminals), rules,
                   mapping[grammar.start], grammar.name)


def union(first, second, name=None):
    """A grammar for the union: a new start choosing between the two."""
    left = _rename(first, "L")
    right = _rename(second, "R")

    rules = {**left.rules, **right.rules}
    start = "U"
    rules[start] = [(left.start,), (right.start,)]

    return Grammar(set(rules), first.terminals | second.terminals, rules, start,
                   name or f"union({first.name}, {second.name})")


def concatenation(first, second, name=None):
    """A grammar for the concatenation: a new start putting them in sequence."""
    left = _rename(first, "L")
    right = _rename(second, "R")

    rules = {**left.rules, **right.rules}
    start = "C"
    rules[start] = [(left.start, right.start)]

    return Grammar(set(rules), first.terminals | second.terminals, rules, start,
                   name or f"concat({first.name}, {second.name})")


def star(grammar, name=None):
    """A grammar for any number of repetitions.

    The new start is right-recursive rather than doubly recursive: ``S -> A S``
    and ``S -> eps``. The doubly recursive version ``S -> S S`` is also
    correct and makes every word ambiguous for no reason.
    """
    inner = _rename(grammar, "S")
    rules = dict(inner.rules)
    start = "K"
    rules[start] = [(inner.start, start), ()]

    return Grammar(set(rules), set(grammar.terminals), rules, start,
                   name or f"star({grammar.name})")


def intersect_with_regular(grammar, dfa, name=None):
    """The intersection of a context-free and a regular language, as a grammar.

    The triple construction again: a variable ``[p A q]`` derives the words
    that A derives **and** that take the automaton from p to q. Rules mirror
    the grammar's, threading states through the right-hand side.

    This is why closure under intersection with a regular language holds while
    general intersection fails: the finite automaton contributes finitely many
    states to thread, and a second pushdown automaton would contribute a second
    stack, which no single machine of this class has.
    """
    import sys as _sys
    from pathlib import Path as _Path
    _sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "regular-languages" / "finite-automata"))
    _sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "chomsky-normal-form"))
    from chomsky_normal_form import to_chomsky_normal_form

    normal = to_chomsky_normal_form(grammar)
    dfa = dfa.complete()
    states = sorted(dfa.states, key=str)

    def variable(left, symbol, right):
        """The name of the triple variable for a state pair and a symbol."""
        return f"[{left},{symbol},{right}]"

    rules = {}
    start = "S0"
    rules[start] = [(variable(dfa.start, normal.start, state),) for state in states
                    if state in dfa.accepting]

    for head, sides in normal.rules.items():
        for right in sides:
            if len(right) == 1 and right[0] in normal.terminals:
                terminal = right[0]
                for source in states:
                    target = dfa.step(source, terminal)
                    if target is not None:
                        rules.setdefault(variable(source, head, target), []).append((terminal,))

            elif len(right) == 2:
                for source in states:
                    for middle in states:
                        for target in states:
                            rules.setdefault(variable(source, head, target), []).append(
                                (variable(source, right[0], middle),
                                 variable(middle, right[1], target)))

    if () in normal.rules.get(normal.start, []):
        for state in states:
            if state in dfa.accepting and state == dfa.start:
                rules[start].append(())

    variables = set(rules)
    for sides in rules.values():
        for right in sides:
            for symbol in right:
                if symbol.startswith("["):
                    variables.add(symbol)
    for symbol in variables:
        rules.setdefault(symbol, [])

    grammar_out = Grammar(variables, set(normal.terminals),
                          {head: sides for head, sides in rules.items() if sides},
                          start, name or f"cap({grammar.name}, {dfa.name})")

    return remove_useless(grammar_out, grammar_out.name)


def intersection_counterexample():
    """The two grammars whose intersection is not context-free.

    ``a^i b^i c^j`` and ``a^i b^j c^j``. Each is context-free, one count at a
    time is all a stack can do. Their intersection needs both counts at once,
    which is ``a^n b^n c^n``.
    """
    from context_free_grammars import parse_grammar

    first = parse_grammar("""
S -> A C
A -> a A b | eps
C -> c C | eps
""", name="a^i b^i c^j")

    second = parse_grammar("""
S -> A B
A -> a A | eps
B -> b B c | eps
""", name="a^i b^j c^j")

    return first, second
