"""LR item automata: LR(0), SLR(1), LR(1) and LALR(1).

A bottom-up parser reads the input and, whenever the top of its stack matches
the right side of a rule, may reduce it. The whole difficulty is deciding
**when**, and the answer is a finite automaton over items.

An item is a rule with a dot marking how much of its right side has been seen.
A state is a set of items, meaning "any of these rules might be in progress".
The four constructions differ only in how much lookahead information the items
carry:

| construction | item | states |
|---|---|---|
| LR(0) | rule and dot | fewest |
| SLR(1) | rule and dot, lookahead taken from Follow at reduce time | same as LR(0) |
| LR(1) | rule, dot and one lookahead symbol | most |
| LALR(1) | LR(1) states merged when their cores agree | same as LR(0) |

LALR is what yacc and bison build, because it has the state count of LR(0) and
almost the power of LR(1). The "almost" is precise: merging can create
reduce-reduce conflicts and can never create shift-reduce ones.
"""

from __future__ import annotations

import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, "..", "grammars"))
sys.path.insert(0, os.path.join(_here, "..", "first-follow"))
import first_follow as ff
import grammars as gr

END = ff.EPSILON
"""End of input, written as epsilon the way the lecture does."""


class Automaton:
    """An item automaton: numbered states and a goto function."""

    def __init__(self, states, transitions, start):
        """Store the numbered item sets and the goto function."""
        self.states = states
        self.transitions = transitions
        self.start = start

    def state_of(self, number):
        """The item set of one state."""
        return self.states[number]

    def goto(self, number, symbol):
        """The state reached from a state on a symbol, or `None`."""
        return self.transitions.get((number, symbol))


def augment(grammar):
    """Add a fresh start symbol with a single rule.

    Without it the parser cannot tell "the start symbol is complete" from "the
    start symbol might grow", because the start symbol may appear on a right
    side. The new rule is the only place an accept action can come from.
    """
    fresh = grammar.start + "'"
    while fresh in grammar.nonterminals:
        fresh += "'"
    return gr.Grammar(fresh, [(fresh, [grammar.start])] + grammar.rules)


def closure(grammar, items):
    """Complete an item set: if the dot is before `A`, add every rule of `A`.

    For LR(1) items the lookahead of the added items is `First` of what follows
    the dot in the parent item, falling back to the parent's own lookahead when
    that can vanish. That fallback is the entire difference between LR(1) and
    LR(0), and the reason LR(1) can have many more states.
    """
    first = ff.first_sets(grammar)
    result = set(items)
    changed = True

    while changed:
        changed = False
        for left, dot, right, lookahead in list(result):
            if dot >= len(right):
                continue
            symbol = right[dot]
            if symbol not in grammar.nonterminals:
                continue

            rest = list(right[dot + 1:]) + ([lookahead] if lookahead is not None else [])
            starters = ff._first_of_sequence(grammar, rest, first) if lookahead is not None \
                else {None}
            if ff.EPSILON in starters and lookahead is not None:
                starters = (starters - {ff.EPSILON}) | {lookahead}

            for production in grammar.rules_for(symbol):
                for symbol_ahead in starters:
                    item = (symbol, 0, tuple(production), symbol_ahead)
                    if item not in result:
                        result.add(item)
                        changed = True

    return frozenset(result)


def goto(grammar, items, symbol):
    """The state reached by shifting one symbol out of an item set."""
    moved = {(left, dot + 1, right, lookahead)
             for left, dot, right, lookahead in items
             if dot < len(right) and right[dot] == symbol}
    return closure(grammar, moved) if moved else frozenset()


def _build(grammar, lookahead):
    """The canonical collection of item sets, numbered in discovery order."""
    augmented = augment(grammar)
    start_item = (augmented.start, 0, tuple([grammar.start]),
                  END if lookahead else None)
    start = closure(augmented, {start_item})

    states = [start]
    numbers = {start: 0}
    transitions = {}
    index = 0

    while index < len(states):
        current = states[index]
        symbols = sorted({right[dot] for _, dot, right, _ in current if dot < len(right)})

        for symbol in symbols:
            target = goto(augmented, current, symbol)
            if not target:
                continue
            if target not in numbers:
                numbers[target] = len(states)
                states.append(target)
            transitions[(index, symbol)] = numbers[target]

        index += 1

    return Automaton(states, transitions, 0)


def lr0_automaton(grammar):
    """The LR(0) automaton: items without lookahead."""
    return _build(grammar, lookahead=False)


def lr1_automaton(grammar):
    """The canonical LR(1) automaton: items carrying one lookahead symbol."""
    return _build(grammar, lookahead=True)


def core(items):
    """An item set stripped of its lookaheads, which is its LR(0) core."""
    return frozenset((left, dot, right) for left, dot, right, _ in items)


def lalr_merges(grammar):
    """Groups of LR(1) states that share a core and are therefore merged."""
    automaton = lr1_automaton(grammar)
    groups = {}

    for number, items in enumerate(automaton.states):
        groups.setdefault(core(items), []).append(number)

    return sorted(groups.values())


def lalr_automaton(grammar):
    """Merge LR(1) states with equal cores, unioning their lookaheads.

    The state count drops to that of the LR(0) automaton, which is the point:
    the canonical LR(1) automaton for a real language has thousands of states
    that differ only in lookahead sets.

    Merging can introduce reduce-reduce conflicts, because two states that each
    reduced unambiguously may disagree once their lookaheads are pooled. It can
    never introduce a shift-reduce conflict, since the shiftable symbols depend
    only on the core.
    """
    automaton = lr1_automaton(grammar)
    groups = lalr_merges(grammar)

    representative = {}
    merged_states = []
    for index, group in enumerate(groups):
        union = set()
        for number in group:
            union |= automaton.states[number]
            representative[number] = index
        merged_states.append(frozenset(union))

    transitions = {}
    for (number, symbol), target in automaton.transitions.items():
        transitions[(representative[number], symbol)] = representative[target]

    return Automaton(merged_states, transitions, representative[automaton.start])


def conflicts(automaton, grammar):
    """Shift-reduce and reduce-reduce conflicts of an LR(1)-style automaton."""
    augmented = augment(grammar)
    found = []

    for number, items in enumerate(automaton.states):
        shiftable = {right[dot] for _, dot, right, _ in items
                     if dot < len(right) and right[dot] not in augmented.nonterminals}
        reductions = {}

        for left, dot, right, lookahead in items:
            if dot < len(right) or left == augmented.start:
                continue
            reductions.setdefault(lookahead, []).append((left, right))

        for lookahead, rules in reductions.items():
            if len(rules) > 1:
                found.append({"state": number, "kind": "reduce/reduce",
                              "lookahead": lookahead, "rules": rules})
            if lookahead in shiftable:
                found.append({"state": number, "kind": "shift/reduce",
                              "lookahead": lookahead, "rules": rules})

    return found


def slr_conflicts(automaton, grammar):
    """Conflicts of the SLR(1) table built on an LR(0) automaton.

    SLR takes the lookahead not from the items but from `Follow` of the reduced
    nonterminal, which is coarser: it allows a reduction wherever the
    nonterminal could ever be followed, not only where it could be followed
    here. That is why a grammar can be LR(1) and not SLR(1).
    """
    augmented = augment(grammar)
    follow = ff.follow_sets(augmented)
    found = []

    for number, items in enumerate(automaton.states):
        shiftable = {right[dot] for _, dot, right, _ in items
                     if dot < len(right) and right[dot] not in augmented.nonterminals}
        reductions = {}

        for left, dot, right, _ in items:
            if dot < len(right) or left == augmented.start:
                continue
            for lookahead in follow[left]:
                reductions.setdefault(lookahead, []).append((left, right))

        for lookahead, rules in reductions.items():
            unique = {(left, tuple(right)) for left, right in rules}
            if len(unique) > 1:
                found.append({"state": number, "kind": "reduce/reduce",
                              "lookahead": lookahead, "rules": sorted(unique)})
            if lookahead in shiftable:
                found.append({"state": number, "kind": "shift/reduce",
                              "lookahead": lookahead, "rules": sorted(unique)})

    return found


def state_depths(automaton):
    """Shortest number of transitions from the start state to each state."""
    depths = {automaton.start: 0}
    frontier = [automaton.start]

    while frontier:
        current = frontier.pop(0)
        for (number, _), target in automaton.transitions.items():
            if number == current and target not in depths:
                depths[target] = depths[current] + 1
                frontier.append(target)

    return depths


def format_item(item):
    """One item in the usual notation, with a dot and a lookahead."""
    left, dot, right, lookahead = item
    body = " ".join(list(right[:dot]) + ["."] + list(right[dot:]))
    if lookahead is None:
        return f"{left} ::= {body}"
    return f"[{left} ::= {body}, {lookahead}]"
