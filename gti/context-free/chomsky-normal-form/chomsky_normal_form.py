"""Chomsky normal form, in the five steps the course names CNF1 to CNF5.

A grammar is in Chomsky normal form when every rule is

    A -> B C      two variables
    A -> a        one terminal

and, if the empty word is in the language, the single rule ``S -> eps``.

The point of the form is [CYK](../cyk/): with every rule of that shape, a
parser can fill a table over substrings and never has to guess how far a rule
reaches.

    CNF1  remove useless variables, generating before reachable
    CNF2  replace terminals in right-hand sides by fresh variables
    CNF3  shorten right-hand sides to length two
    CNF4  remove epsilon rules
    CNF5  remove unit rules

The order matters at both ends. CNF2 before CNF3 keeps the shortening from
having to deal with terminals, and CNF4 before CNF5 matters because removing
epsilon rules **creates** unit rules: dropping the nullable B from ``A -> B C``
leaves ``A -> C``.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "context-free-grammars"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "grammar-cleanup"))

from context_free_grammars import Grammar
from grammar_cleanup import remove_epsilon_rules, remove_unit_rules, remove_useless


def replace_terminals(grammar, name=None):
    """CNF2: give every terminal its own variable and use that in the rules.

    ``W_a -> a`` is added for each terminal, and every occurrence of ``a`` in a
    right-hand side becomes ``W_a``. The course replaces terminals everywhere,
    including in rules that are a single terminal, so ``B -> b`` becomes the
    unit rule ``B -> W_b``, which CNF5 later turns back into ``B -> b``.
    """
    used = {symbol for sides in grammar.rules.values() for right in sides
            for symbol in right if symbol in grammar.terminals}

    names = {terminal: f"W{terminal}" for terminal in sorted(used)}
    rules = {}

    for variable, sides in grammar.rules.items():
        for right in sides:
            replaced = tuple(names.get(symbol, symbol) for symbol in right)
            rules.setdefault(variable, [])
            if replaced not in rules[variable]:
                rules[variable].append(replaced)

    for terminal, variable in names.items():
        rules[variable] = [(terminal,)]

    return Grammar(set(rules), set(grammar.terminals), rules, grammar.start,
                   name or f"CNF2({grammar.name})")


def shorten_rules(grammar, prefix="X", name=None):
    """CNF3: break right-hand sides longer than two into a chain of pairs.

    ``C -> B A A C W`` becomes ``C -> B X1``, ``X1 -> A X2``, ``X2 -> A X3``,
    ``X3 -> C W``: right-associative, one fresh variable per removed position.

    The fresh names are arbitrary. The published solution uses a different
    letter per source rule, U for one and V for another; nothing depends on the
    choice, and the grammars are the same up to renaming.
    """
    rules = {variable: [] for variable in grammar.rules}
    counter = 0

    for variable in sorted(grammar.rules):
        for right in grammar.rules[variable]:
            if len(right) <= 2:
                if right not in rules[variable]:
                    rules[variable].append(right)
                continue

            current = variable
            remaining = list(right)

            while len(remaining) > 2:
                counter += 1
                fresh = f"{prefix}{counter}"
                rules.setdefault(current, [])
                pair = (remaining[0], fresh)
                if pair not in rules[current]:
                    rules[current].append(pair)
                rules[fresh] = []
                current = fresh
                remaining = remaining[1:]

            rules.setdefault(current, [])
            if tuple(remaining) not in rules[current]:
                rules[current].append(tuple(remaining))

    rules = {variable: sides for variable, sides in rules.items() if sides}
    return Grammar(set(rules), set(grammar.terminals), rules, grammar.start,
                   name or f"CNF3({grammar.name})")


def to_chomsky_normal_form(grammar, trace=False):
    """Run all five steps and return the grammar in Chomsky normal form.

    With ``trace`` the intermediate grammar after each step is returned as
    well, which is what the exercise asks to be written out by hand.
    """
    steps = []

    first = remove_useless(grammar, "G1")
    steps.append(("CNF1", first))

    second = replace_terminals(first, "G2")
    steps.append(("CNF2", second))

    third = shorten_rules(second, name="G3")
    steps.append(("CNF3", third))

    fourth = remove_epsilon_rules(third, "G4")
    steps.append(("CNF4", fourth))

    fifth = remove_unit_rules(fourth, "G5")
    steps.append(("CNF5", fifth))

    result = _repair_terminals(fifth, f"CNF({grammar.name})")

    return (result, steps) if trace else result


def _repair_terminals(grammar, name):
    """After unit removal, make sure every rule is a pair or a single terminal.

    Removing unit rules can leave a right-hand side of two symbols where one is
    a terminal, such as ``A -> W_b W_c`` collapsing into ``A -> b W_c``. Those
    are put back through a terminal variable, which is the same repair CNF2
    does and is needed again here.
    """
    rules = {variable: list(sides) for variable, sides in grammar.rules.items()}
    extra = {}

    for variable in list(rules):
        repaired = []
        for right in rules[variable]:
            if len(right) == 2:
                fixed = []
                for symbol in right:
                    if symbol in grammar.terminals:
                        helper = extra.setdefault(symbol, f"T{symbol}")
                        fixed.append(helper)
                    else:
                        fixed.append(symbol)
                repaired.append(tuple(fixed))
            else:
                repaired.append(right)
        rules[variable] = repaired

    for terminal, helper in extra.items():
        rules[helper] = [(terminal,)]

    return Grammar(set(rules), set(grammar.terminals), rules, grammar.start, name)


def is_chomsky_normal_form(grammar):
    """Check the shape of every rule, and say which one breaks it."""
    problems = []

    for variable, sides in grammar.rules.items():
        for right in sides:
            if not right:
                if variable != grammar.start:
                    problems.append((variable, right, "empty right side outside the start"))
            elif len(right) == 1:
                if right[0] not in grammar.terminals:
                    problems.append((variable, right, "unit rule"))
            elif len(right) == 2:
                if any(symbol in grammar.terminals for symbol in right):
                    problems.append((variable, right, "terminal in a pair"))
            else:
                problems.append((variable, right, "longer than two"))

    return not problems, problems
