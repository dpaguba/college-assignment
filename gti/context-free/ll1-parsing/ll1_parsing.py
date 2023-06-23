"""LL(1): parsing left to right with one symbol of lookahead.

A top-down parser reads the input from the left and expands the leftmost
variable. With one symbol of lookahead it must be able to choose the right rule
from that symbol alone, and two sets decide whether it can:

    FIRST(alpha)  the terminals that can start a string derived from alpha,
                  plus eps if alpha derives the empty word
    FOLLOW(A)     the terminals that can appear directly after A in some
                  sentential form

A grammar is LL(1) when neither conflict occurs:

- **first/first**: two rules for the same variable whose right-hand sides can
  start with the same terminal
- **first/follow**: a variable that can derive the empty word and whose FIRST
  meets its FOLLOW, so the parser cannot tell "expand" from "skip"

The course computes FOLLOW without an end marker, so ``FOLLOW(S)`` of a start
symbol that never appears inside a rule is empty. Adding the marker is the
other common convention and changes nothing about which grammars are LL(1)
here; the sets are just printed differently.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "context-free-grammars"))

from context_free_grammars import Grammar

EPSILON = "eps"


def first_sets(grammar):
    """FIRST for every variable, as a least fixed point.

    A terminal contributes itself. A variable contributes its own FIRST, and
    the scan continues past it only while it can derive the empty word, which
    is what makes ``FIRST(BA)`` contain eps only when both B and A do.
    """
    first = {variable: set() for variable in grammar.variables}
    changed = True

    while changed:
        changed = False
        for variable, sides in grammar.rules.items():
            for right in sides:
                before = len(first[variable])
                first[variable] |= first_of(right, first, grammar)
                if len(first[variable]) != before:
                    changed = True

    return first


def first_of(sequence, first, grammar):
    """FIRST of a string of symbols, given the FIRST sets of the variables."""
    if not sequence:
        return {EPSILON}

    result = set()
    for symbol in sequence:
        if not grammar.is_variable(symbol):
            result.add(symbol)
            return result

        result |= first.get(symbol, set()) - {EPSILON}
        if EPSILON not in first.get(symbol, set()):
            return result

    result.add(EPSILON)
    return result


def follow_sets(grammar, first=None, end_marker=None):
    """FOLLOW for every variable, as a least fixed point.

    For every rule ``A -> alpha B beta``: everything in FIRST(beta) except eps
    goes into FOLLOW(B), and if beta can vanish, so does everything in
    FOLLOW(A).

    ``end_marker`` adds a symbol to FOLLOW of the start variable. The course
    leaves it out, which is why the default is None.
    """
    first = first or first_sets(grammar)
    follow = {variable: set() for variable in grammar.variables}

    if end_marker is not None:
        follow[grammar.start].add(end_marker)

    changed = True
    while changed:
        changed = False

        for variable, sides in grammar.rules.items():
            for right in sides:
                for position, symbol in enumerate(right):
                    if not grammar.is_variable(symbol):
                        continue

                    rest = first_of(right[position + 1:], first, grammar)
                    addition = rest - {EPSILON}

                    if EPSILON in rest:
                        addition |= follow[variable]

                    if not addition <= follow[symbol]:
                        follow[symbol] |= addition
                        changed = True

    return follow


def conflicts(grammar):
    """Every LL(1) conflict, named by kind, with the sets that cause it."""
    first = first_sets(grammar)
    follow = follow_sets(grammar, first)
    found = []

    for variable, sides in sorted(grammar.rules.items()):
        firsts = [first_of(right, first, grammar) for right in sides]

        for index, left in enumerate(firsts):
            for other in range(index + 1, len(firsts)):
                shared = (left & firsts[other]) - {EPSILON}
                if shared:
                    found.append({
                        "kind": "first/first",
                        "variable": variable,
                        "rules": (sides[index], sides[other]),
                        "shared": sorted(shared),
                    })

        if EPSILON in first[variable]:
            shared = first[variable] & follow[variable]
            if shared:
                found.append({
                    "kind": "first/follow",
                    "variable": variable,
                    "first": sorted(first[variable]),
                    "follow": sorted(follow[variable]),
                    "shared": sorted(shared),
                })

    return found


def is_ll1(grammar):
    """Whether the grammar is LL(1), with the conflicts when it is not."""
    found = conflicts(grammar)
    return not found, found


def parse_table(grammar):
    """The table a predictive parser looks up: (variable, terminal) to rule.

    An entry holding two rules is exactly a conflict, so building the table is
    the same test as ``conflicts`` seen from the parser's side.
    """
    first = first_sets(grammar)
    follow = follow_sets(grammar, first)
    table = {}

    for variable, sides in grammar.rules.items():
        for right in sides:
            starters = first_of(right, first, grammar)

            for terminal in starters - {EPSILON}:
                table.setdefault((variable, terminal), []).append(right)

            if EPSILON in starters:
                for terminal in follow[variable]:
                    table.setdefault((variable, terminal), []).append(right)

    return table


def parse(grammar, word, table=None):
    """Run the predictive parser and return the leftmost derivation, or None.

    A stack holds what is still expected. A variable on top is replaced by the
    rule the table selects for the current lookahead; a terminal on top must
    match and is consumed. No backtracking anywhere, which is the whole point:
    the parser is linear in the length of the input.
    """
    table = table or parse_table(grammar)
    stack = [grammar.start]
    position = 0
    steps = []

    while stack:
        top = stack.pop()

        if not grammar.is_variable(top):
            if position < len(word) and word[position] == top:
                position += 1
                continue
            return None

        lookahead = word[position] if position < len(word) else None
        options = table.get((top, lookahead), [])

        if not options:
            return None
        if len(options) > 1:
            raise ValueError(f"the grammar is not LL(1): {top} on {lookahead} has "
                             f"{len(options)} rules")

        rule = options[0]
        steps.append((top, rule))
        stack.extend(reversed(rule))

    return steps if position == len(word) else None


def report(grammar):
    """FIRST, FOLLOW, the FIRST of every right-hand side, and the verdict.

    This is the shape the exercise asks for: the sets, then the reason.
    """
    first = first_sets(grammar)
    follow = follow_sets(grammar, first)

    rows = {
        "FIRST": {variable: sorted(first[variable]) for variable in sorted(first)},
        "FOLLOW": {variable: sorted(follow[variable]) for variable in sorted(follow)},
        "FIRST of right-hand sides": {
            f"{variable} -> {''.join(right) if right else 'eps'}":
                sorted(first_of(right, first, grammar))
            for variable in sorted(grammar.rules)
            for right in grammar.rules[variable]
        },
        "LL(1)": not conflicts(grammar),
        "conflicts": conflicts(grammar),
    }
    return rows
