"""Greibach normal form: every rule starts with a terminal.

    A -> a alpha        with alpha a possibly empty string of variables

The consequence is what matters: every derivation step produces exactly one
terminal, so a word of length n is derived in exactly n steps. A top-down
parser can then read the input and never loop, because there is no rule that
consumes nothing.

The construction goes through
[Chomsky normal form](../chomsky-normal-form/) and has two parts:

- **substitution** in an order: number the variables and make sure that a rule
  for A_i never starts with an A_j for j < i, by substituting the rules of A_j
  in wherever it does
- **left recursion removal**: a rule ``A -> A beta`` can never start with a
  terminal, so it is replaced by a right-recursive helper variable

Left recursion is the real obstacle, and it is the same obstacle a recursive
descent parser hits, which is why the same transformation appears in
[LL(1)](../ll1-parsing/) preparation.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "context-free-grammars"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "chomsky-normal-form"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "grammar-cleanup"))

from chomsky_normal_form import to_chomsky_normal_form
from context_free_grammars import Grammar
from grammar_cleanup import remove_useless


def remove_left_recursion(grammar, name=None):
    """Replace every immediate left recursion by a right-recursive helper.

    ``A -> A b | c`` becomes ``A -> c | c A'`` and ``A' -> b | b A'``. The
    language is unchanged and the recursion now grows to the right, which is
    what both Greibach normal form and a top-down parser need.

    Only **immediate** left recursion is handled here. Indirect recursion,
    where A reaches itself through other variables, is removed by the ordered
    substitution in ``to_greibach_normal_form``.
    """
    rules = {variable: list(sides) for variable, sides in grammar.rules.items()}
    variables = set(grammar.variables)

    for variable in sorted(grammar.rules):
        recursive = [right[1:] for right in rules[variable]
                     if right and right[0] == variable]
        other = [right for right in rules[variable]
                 if not (right and right[0] == variable)]

        if not recursive:
            continue

        helper = f"{variable}'"
        while helper in variables:
            helper += "'"
        variables.add(helper)

        rules[variable] = [right for right in other] + \
                          [tuple(right) + (helper,) for right in other]
        rules[helper] = [tuple(right) for right in recursive] + \
                        [tuple(right) + (helper,) for right in recursive]

    return Grammar(variables, set(grammar.terminals), rules, grammar.start,
                   name or f"noleft({grammar.name})")


def to_greibach_normal_form(grammar, name=None):
    """Convert a grammar into Greibach normal form.

    Starts from Chomsky normal form, orders the variables, substitutes forward
    until no rule starts with an earlier variable, removes the left recursions
    that appear on the way, and finally substitutes backwards so every
    right-hand side begins with a terminal.

    The result is usually much larger than the input. Substitution multiplies
    rules, and that blow-up is the reason Greibach normal form is a theoretical
    tool rather than something a compiler uses.
    """
    normal = to_chomsky_normal_form(grammar)
    order = sorted(normal.rules)
    position = {variable: index for index, variable in enumerate(order)}

    rules = {variable: list(normal.rules[variable]) for variable in order}
    variables = set(normal.variables)

    for index, variable in enumerate(order):
        changed = True
        while changed:
            changed = False
            expanded = []

            for right in rules[variable]:
                head = right[0] if right else None
                if head in position and position[head] < index:
                    for replacement in rules[head]:
                        expanded.append(tuple(replacement) + right[1:])
                    changed = True
                else:
                    expanded.append(right)

            rules[variable] = _unique(expanded)

        recursive = [right[1:] for right in rules[variable]
                     if right and right[0] == variable]

        if recursive:
            helper = f"{variable}~"
            while helper in variables:
                helper += "~"
            variables.add(helper)

            other = [right for right in rules[variable]
                     if not (right and right[0] == variable)]
            rules[variable] = _unique(other + [tuple(right) + (helper,) for right in other])
            rules[helper] = _unique([tuple(right) for right in recursive]
                                    + [tuple(right) + (helper,) for right in recursive])

    for variable in reversed(order):
        rules[variable] = _substitute_leading(rules[variable], rules, normal.terminals)

    for helper in sorted(variables - set(order)):
        if helper in rules:
            rules[helper] = _substitute_leading(rules[helper], rules, normal.terminals)

    grammar_out = Grammar(set(rules), set(normal.terminals),
                          {head: sides for head, sides in rules.items() if sides},
                          normal.start, name or f"GNF({grammar.name})")

    return remove_useless(grammar_out, grammar_out.name)


def _substitute_leading(sides, rules, terminals, rounds=6):
    """Replace a leading variable by its rules until every side starts with a terminal."""
    current = list(sides)

    for _ in range(rounds):
        if all(not right or right[0] in terminals for right in current):
            break

        expanded = []
        for right in current:
            if right and right[0] not in terminals and right[0] in rules:
                for replacement in rules[right[0]]:
                    expanded.append(tuple(replacement) + right[1:])
            else:
                expanded.append(right)
        current = _unique(expanded)

    return current


def _unique(sides):
    """The right-hand sides without duplicates, in their original order."""
    seen = []
    for right in sides:
        if right not in seen:
            seen.append(right)
    return seen


def is_greibach_normal_form(grammar):
    """Check that every rule is a terminal followed by variables only."""
    problems = []

    for variable, sides in grammar.rules.items():
        for right in sides:
            if not right:
                if variable != grammar.start:
                    problems.append((variable, right, "empty right side"))
                continue
            if right[0] not in grammar.terminals:
                problems.append((variable, right, "does not start with a terminal"))
            elif any(symbol in grammar.terminals for symbol in right[1:]):
                problems.append((variable, right, "terminal after the first symbol"))

    return not problems, problems
