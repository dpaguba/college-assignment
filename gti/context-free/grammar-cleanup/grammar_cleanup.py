"""Removing the parts of a grammar that cannot contribute.

Two kinds of variable are useless, and the order they are removed in matters:

- **non-generating**: no derivation from it reaches a word of terminals
- **unreachable**: no derivation from the start symbol mentions it

Generating first, then reachable. The other order leaves rubbish behind:
deleting a non-generating variable can make another variable unreachable, so
reachability has to be computed on the already cleaned grammar. Doing it the
other way round is the standard mistake, and it produces a grammar that is
correct but not clean.

This is step CNF1 of the course's normal form algorithm.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "context-free-grammars"))

from context_free_grammars import Grammar


def generating(grammar):
    """Variables from which some string of terminals can be derived.

    A least fixed point: a variable is generating if it has a rule whose right
    side consists only of terminals and already-generating variables. Start
    with none and add until nothing changes.
    """
    found = set()
    changed = True

    while changed:
        changed = False
        for variable, sides in grammar.rules.items():
            if variable in found:
                continue
            for right in sides:
                if all(symbol in grammar.terminals or symbol in found for symbol in right):
                    found.add(variable)
                    changed = True
                    break

    return found


def reachable(grammar):
    """Variables that appear in some sentential form derived from the start."""
    found = {grammar.start}
    queue = [grammar.start]

    while queue:
        variable = queue.pop()
        for right in grammar.rules.get(variable, []):
            for symbol in right:
                if grammar.is_variable(symbol) and symbol not in found:
                    found.add(symbol)
                    queue.append(symbol)

    return found


def remove_non_generating(grammar, name=None):
    """Drop variables that derive no terminal string, and the rules using them."""
    keep = generating(grammar)
    return _restrict(grammar, keep, name or f"gen({grammar.name})")


def remove_unreachable(grammar, name=None):
    """Drop variables the start symbol cannot reach."""
    keep = reachable(grammar)
    return _restrict(grammar, keep, name or f"reach({grammar.name})")


def _restrict(grammar, keep, name):
    """The grammar with only the variables that are kept."""
    rules = {}
    for variable in grammar.rules:
        if variable not in keep:
            continue
        sides = [right for right in grammar.rules[variable]
                 if all(symbol in grammar.terminals or symbol in keep for symbol in right)]
        if sides:
            rules[variable] = sides

    terminals = {symbol for sides in rules.values() for right in sides
                 for symbol in right if symbol not in keep}

    return Grammar(set(rules), terminals, rules, grammar.start, name)


def remove_useless(grammar, name=None):
    """CNF1: remove non-generating variables, then unreachable ones.

    The order is the content of this step. Doing reachability first can leave a
    variable that is reachable only through a rule which is about to be deleted
    for mentioning a non-generating variable.
    """
    return remove_unreachable(remove_non_generating(grammar),
                              name or f"CNF1({grammar.name})")


def nullable(grammar):
    """Variables from which the empty word can be derived.

    Another least fixed point, and the set the course calls V'. A variable is
    nullable if some rule has an empty right side or a right side made only of
    nullable variables.
    """
    found = set()
    changed = True

    while changed:
        changed = False
        for variable, sides in grammar.rules.items():
            if variable in found:
                continue
            for right in sides:
                if all(symbol in found for symbol in right):
                    found.add(variable)
                    changed = True
                    break

    return found


def remove_epsilon_rules(grammar, name=None):
    """CNF4: remove empty right-hand sides, compensating for what they allowed.

    For each rule, every subset of its nullable occurrences is dropped, which
    is how the words those rules used to produce are still derivable. That is
    exponential in the number of nullable symbols in one rule, and in practice
    each rule has one or two.

    The empty word itself is lost unless the start symbol is nullable, in which
    case the course keeps a single rule for it. The exercises use grammars
    where that does not arise, and this keeps the rule so the language is
    preserved.
    """
    empties = nullable(grammar)
    rules = {}

    for variable, sides in grammar.rules.items():
        for right in sides:
            for variant in _drop_nullable(right, empties):
                if variant or variable == grammar.start:
                    rules.setdefault(variable, [])
                    if tuple(variant) not in rules[variable]:
                        rules[variable].append(tuple(variant))

    if grammar.start in empties:
        rules.setdefault(grammar.start, [])
        if () not in rules[grammar.start]:
            rules[grammar.start].append(())
    else:
        for variable in rules:
            rules[variable] = [right for right in rules[variable] if right]

    return Grammar(set(rules), set(grammar.terminals), rules, grammar.start,
                   name or f"CNF4({grammar.name})")


def _drop_nullable(right, empties):
    """Every way of deleting some of the nullable symbols of a right-hand side."""
    variants = [()]

    for symbol in right:
        extended = []
        for variant in variants:
            extended.append(variant + (symbol,))
            if symbol in empties:
                extended.append(variant)
        variants = extended

    seen = []
    for variant in variants:
        if variant not in seen:
            seen.append(variant)
    return seen


def unit_pairs(grammar):
    """Pairs (A, B) such that A derives B using only unit rules.

    The set the course calls U. It is the reflexive transitive closure of the
    unit rules, and computing it first is what makes their removal a single
    pass instead of a fixed point.
    """
    pairs = {(variable, variable) for variable in grammar.variables}
    changed = True

    while changed:
        changed = False
        for left, middle in list(pairs):
            for right in grammar.rules.get(middle, []):
                if len(right) == 1 and grammar.is_variable(right[0]):
                    if (left, right[0]) not in pairs:
                        pairs.add((left, right[0]))
                        changed = True

    return pairs


def remove_unit_rules(grammar, name=None):
    """CNF5: replace every unit rule by the rules it stands for.

    For each pair (A, B) in the closure, every non-unit rule of B becomes a
    rule of A. Afterwards some variables may have become unreachable, and the
    course removes them in the same step, which is why this ends with a
    reachability pass.
    """
    pairs = unit_pairs(grammar)
    rules = {}

    for left, middle in sorted(pairs):
        for right in grammar.rules.get(middle, []):
            if len(right) == 1 and grammar.is_variable(right[0]):
                continue
            rules.setdefault(left, [])
            if tuple(right) not in rules[left]:
                rules[left].append(tuple(right))

    cleaned = Grammar(set(rules), set(grammar.terminals), rules, grammar.start,
                      name or f"CNF5({grammar.name})")
    return remove_unreachable(cleaned, cleaned.name)
