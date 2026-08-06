"""First and Follow sets, the tables every predictive parser is built from.

`First(alpha)` is the set of terminals that can begin a string derived from
`alpha`, plus epsilon if `alpha` can derive nothing at all. `Follow(A)` is the
set of terminals that can appear immediately after `A` in some sentential form.

Both are least fixed points, computed by iterating until nothing changes, and
both are needed for the same reason: a top-down parser has to choose a rule
from one lookahead symbol, and the choice is exactly "which rule can start with
this symbol, or is nullable and followed by it".

The lecture writes the end of input as epsilon rather than as a separate
`$` symbol, and this module follows that convention: `EPSILON` appears in
`Follow` sets to mean end of input, and in `First` sets to mean nullable.
"""

from __future__ import annotations

EPSILON = "\u03b5"
"""The symbol standing both for nullability and for the end of the input.

Written as the Greek letter rather than as the ASCII `e`, because `e` is a
perfectly ordinary terminal: the dangling-else grammar uses it for `else`, and
a marker colliding with a real symbol would silently corrupt the parse table.
"""


def first_sets(grammar):
    """First sets for every nonterminal, as a least fixed point."""
    return first_iterations(grammar)[-1]


def first_iterations(grammar):
    """Every round of the First computation, including the initial one.

    The rounds are kept because the published solution shows them, and
    reproducing them needs the lecture's formulation rather than the textbook
    one. The lecture reads First as the first symbols of the words derivable
    **so far**, so a right side containing a nonterminal whose set is still
    empty contributes nothing at all, even when it starts with a terminal:
    `B ::= b B c` adds nothing in the first round, because `B` derives no word
    yet and therefore neither does `b B c`.

    The rounds are computed from the previous round throughout, never in place.
    That is a choice the exercise leaves open, and it costs one round on this
    grammar: the published table has `First(A)` complete after round 2, which
    requires reading `First(B)` as it is being updated in the same round. The
    final sets are identical either way, and the number of rounds is the same.
    """
    current = {nonterminal: set() for nonterminal in grammar.nonterminals}
    rounds = [dict((key, set(value)) for key, value in current.items())]

    while True:
        following = {key: set(value) for key, value in current.items()}

        for left, right in grammar.rules:
            following[left] |= _first_so_far(grammar, right, current)

        if following == current:
            return rounds

        current = following
        rounds.append({key: set(value) for key, value in current.items()})


def _first_so_far(grammar, symbols, first):
    """First of a sequence under the lecture's reading, during the iteration.

    A nonterminal with an empty set derives nothing yet, so the whole sequence
    derives nothing yet. Once the fixed point is reached and every nonterminal
    is productive, this agrees with `_first_of_sequence` exactly; the two only
    differ while the computation is still running, and for grammars containing
    a nonterminal that derives no word at all.
    """
    if any(symbol in grammar.nonterminals and not first[symbol] for symbol in symbols):
        return set()
    return _first_of_sequence(grammar, symbols, first)


def _first_of_sequence(grammar, symbols, first):
    """First of a symbol sequence, given the First sets computed so far.

    Walk left to right, adding each symbol's First set minus epsilon, and stop
    at the first symbol that cannot vanish. Epsilon is added only if every
    symbol in the sequence can vanish, which is also why the empty sequence
    maps to epsilon rather than to the empty set.
    """
    result = set()

    for symbol in symbols:
        if symbol not in grammar.nonterminals:
            result.add(symbol)
            return result

        result |= first[symbol] - {EPSILON}
        if EPSILON not in first[symbol]:
            return result

    result.add(EPSILON)
    return result


def first_of(grammar, symbols):
    """First of an arbitrary symbol sequence, with the fixed point computed."""
    return _first_of_sequence(grammar, symbols, first_sets(grammar))


def follow_sets(grammar):
    """Follow sets for every nonterminal, as a least fixed point."""
    return follow_iterations(grammar)[-1]


def follow_iterations(grammar):
    """Every round of the Follow computation, including the initial one.

    Two rules generate everything. For a rule `A ::= alpha B beta`, everything
    in `First(beta)` except epsilon belongs to `Follow(B)`; and if `beta` can
    vanish, everything in `Follow(A)` belongs to `Follow(B)` as well. The
    second rule is what makes the computation iterative, since it propagates
    information backwards through the grammar.

    The start symbol is initialised with epsilon, which here means end of input.
    """
    first = first_sets(grammar)
    current = {nonterminal: set() for nonterminal in grammar.nonterminals}
    current[grammar.start].add(EPSILON)
    rounds = [{key: set(value) for key, value in current.items()}]

    while True:
        following = {key: set(value) for key, value in current.items()}

        for left, right in grammar.rules:
            for index, symbol in enumerate(right):
                if symbol not in grammar.nonterminals:
                    continue
                rest = _first_of_sequence(grammar, right[index + 1:], first)
                following[symbol] |= rest - {EPSILON}
                if EPSILON in rest:
                    following[symbol] |= current[left]

        if following == current:
            return rounds

        current = following
        rounds.append({key: set(value) for key, value in current.items()})


def nullable_nonterminals(grammar):
    """The nonterminals whose First set contains epsilon."""
    first = first_sets(grammar)
    return {name for name, symbols in first.items() if EPSILON in symbols}


def report(grammar):
    """First and Follow side by side, the form the exercise asks for."""
    first, follow = first_sets(grammar), follow_sets(grammar)
    lines = []

    for nonterminal in sorted(grammar.nonterminals):
        lines.append({
            "nonterminal": nonterminal,
            "first": sorted(first[nonterminal]),
            "follow": sorted(follow[nonterminal]),
        })

    return lines
