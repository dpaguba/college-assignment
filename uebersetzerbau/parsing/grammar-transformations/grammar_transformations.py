"""Making a grammar fit a parsing method without changing its language.

A top-down parser cannot handle left recursion, because predicting `E ::= E + T`
means calling `E` again on the same input and never consuming anything. It also
cannot handle two rules with a common prefix, because one lookahead symbol
cannot tell them apart.

Both are properties of the **grammar**, not of the language, and both can be
removed mechanically. What cannot be removed mechanically is ambiguity: left
factoring the dangling-else grammar makes its table conflict-free and leaves
the grammar just as ambiguous as before.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "grammars"))
import grammars as gr


def left_recursive_nonterminals(grammar):
    """Nonterminals with a rule whose right side starts with themselves."""
    return {left for left, right in grammar.rules if right and right[0] == left}


def indirect_left_recursive(grammar):
    """Nonterminals that reach themselves through a chain of leftmost symbols.

    Direct recursion is visible in one rule; indirect recursion needs the
    transitive closure of "can appear leftmost". A nullable leading symbol
    makes the next one leftmost too, which is why the closure has to look past
    it rather than only at the first position.
    """
    nullable = grammar.nullable()
    edges = {name: set() for name in grammar.nonterminals}

    for left, right in grammar.rules:
        for symbol in right:
            if symbol in grammar.nonterminals:
                edges[left].add(symbol)
            if symbol not in nullable:
                break

    reachable = {name: set(targets) for name, targets in edges.items()}
    changed = True
    while changed:
        changed = False
        for name in reachable:
            grown = set(reachable[name])
            for target in reachable[name]:
                grown |= reachable[target]
            if grown != reachable[name]:
                reachable[name] = grown
                changed = True

    return {name for name in reachable if name in reachable[name]}


def remove_left_recursion(grammar):
    """Paull's algorithm: substitute earlier nonterminals, then remove directly.

    Fix an order of the nonterminals. For each in turn, replace any rule whose
    right side begins with an earlier nonterminal by that nonterminal's rules,
    which turns indirect recursion into direct recursion, then remove the
    direct recursion in the standard way:

        A ::= A alpha | beta      becomes      A ::= beta A'
                                               A' ::= alpha A' | e

    The new nonterminal collects what used to be the recursive tail, so the
    parser consumes `beta` first and then loops. The language is unchanged and
    the associativity of the tree is not, which is why a compiler using this
    transformation has to rebuild the shape it wanted afterwards.
    """
    order = _order(grammar)
    rules = {name: [list(right) for right in grammar.rules_for(name)] for name in order}

    for index, name in enumerate(order):
        for earlier in order[:index]:
            expanded = []
            for right in rules[name]:
                if right and right[0] == earlier:
                    for substitute in rules[earlier]:
                        expanded.append(list(substitute) + right[1:])
                else:
                    expanded.append(right)
            rules[name] = expanded

        recursive = [right[1:] for right in rules[name] if right and right[0] == name]
        others = [right for right in rules[name] if not (right and right[0] == name)]

        if recursive:
            tail = _fresh(name, rules)
            rules[name] = [right + [tail] for right in others] or [[tail]]
            rules[tail] = [right + [tail] for right in recursive] + [[]]

    ordered = []
    for name in list(rules):
        for right in rules[name]:
            ordered.append((name, right))

    return gr.Grammar(grammar.start, ordered)


def _order(grammar):
    """A fixed nonterminal order with the start symbol first."""
    rest = sorted(grammar.nonterminals - {grammar.start})
    return [grammar.start] + rest


def _fresh(name, rules):
    """A nonterminal name not yet in use."""
    candidate = name + "2"
    while candidate in rules:
        candidate += "2"
    return candidate


def longest_common_prefix(rights):
    """The longest prefix shared by at least two of the given right sides.

    Two is the threshold because a prefix shared by one rule is not a conflict.
    The longest one is chosen so that factoring terminates: a shorter prefix
    would leave the longer one to be factored again next round.
    """
    best = []

    for index, first in enumerate(rights):
        for second in rights[index + 1:]:
            shared = []
            for a, b in zip(first, second):
                if a != b:
                    break
                shared.append(a)
            if len(shared) > len(best):
                best = shared

    return best


def left_factor(grammar):
    """Pull out common prefixes until no two rules of a nonterminal share one.

        A ::= alpha beta | alpha gamma     becomes     A ::= alpha A'
                                                       A' ::= beta | gamma

    The parser then decides after reading `alpha` rather than before, which is
    exactly the amount of extra information it needed. Nothing about the
    language changes, and neither does ambiguity: the dangling-else grammar is
    still ambiguous afterwards, because the ambiguity is in which `if` an
    `else` belongs to and not in how the rules are written.
    """
    rules = {name: [list(right) for right in grammar.rules_for(name)]
             for name in grammar.nonterminals}

    changed = True
    while changed:
        changed = False
        for name in list(rules):
            prefix = longest_common_prefix(rules[name])
            if not prefix:
                continue

            sharing = [right for right in rules[name] if right[:len(prefix)] == prefix]
            if len(sharing) < 2:
                continue

            tail = _fresh(name, rules)
            rest = [right for right in rules[name] if right[:len(prefix)] != prefix]
            rules[name] = rest + [prefix + [tail]]
            rules[tail] = [right[len(prefix):] for right in sharing]
            changed = True

    ordered = []
    for name in list(rules):
        for right in rules[name]:
            ordered.append((name, right))

    return gr.Grammar(grammar.start, ordered)


def remove_useless(grammar):
    """Drop nonterminals that derive no word or that nothing reaches.

    Both transformations above can leave such rules behind, and a parser
    generator that keeps them reports conflicts in cells that can never be
    entered. Productivity first, reachability second: doing it the other way
    round can leave a rule mentioning a symbol that was just removed.
    """
    productive = set()
    changed = True
    while changed:
        changed = False
        for left, right in grammar.rules:
            if left in productive:
                continue
            if all(symbol not in grammar.nonterminals or symbol in productive
                   for symbol in right):
                productive.add(left)
                changed = True

    kept = [(left, right) for left, right in grammar.rules
            if left in productive
            and all(symbol not in grammar.nonterminals or symbol in productive
                    for symbol in right)]

    reachable = {grammar.start}
    changed = True
    while changed:
        changed = False
        for left, right in kept:
            if left not in reachable:
                continue
            for symbol in right:
                if symbol in grammar.nonterminals and symbol not in reachable:
                    reachable.add(symbol)
                    changed = True

    return gr.Grammar(grammar.start,
                      [(left, right) for left, right in kept if left in reachable])
