"""Context-free grammars, parse trees and derivations.

A grammar says which strings are programs; a parse tree says how one of them is
built. Everything a compiler does after scanning hangs off the tree, so the
question that matters is not whether a word is in the language but whether its
tree is unique.

The two derivation orders, leftmost and rightmost, are the same tree read in
two directions. They matter because the parsing methods split along exactly
that line: top-down parsers build a leftmost derivation forwards, bottom-up
parsers build a rightmost one backwards.
"""

from __future__ import annotations

import itertools


class Node:
    """A parse tree node: a grammar symbol and its children."""

    def __init__(self, symbol, children=None):
        """Create a node for a symbol, with its children if it has any."""
        self.symbol = symbol
        self.children = children if children is not None else []

    def is_leaf(self):
        """Whether the node has no children, which for a terminal is always."""
        return not self.children

    def __repr__(self):
        """Bracketed form, compact enough to compare small trees by eye."""
        if self.is_leaf():
            return self.symbol
        return f"{self.symbol}({' '.join(repr(child) for child in self.children)})"

    def __eq__(self, other):
        """Structural equality, used to count distinct trees."""
        return (isinstance(other, Node) and self.symbol == other.symbol
                and self.children == other.children)


class Grammar:
    """A context-free grammar as a start symbol and a list of rules.

    A rule is a pair of a left side and a list of symbols. Any symbol appearing
    on a left side is a nonterminal, everything else is a terminal, so the
    alphabet does not have to be declared and cannot disagree with the rules.
    """

    def __init__(self, start, rules):
        """Split the rules into nonterminals and terminals as they are stored."""
        self.start = start
        self.rules = [(left, list(right)) for left, right in rules]
        self.nonterminals = {left for left, _ in self.rules}
        self.terminals = {symbol for _, right in self.rules for symbol in right
                          if symbol not in self.nonterminals}

    def rules_for(self, nonterminal):
        """All right sides of one nonterminal, in the order they were given."""
        return [right for left, right in self.rules if left == nonterminal]

    def nullable(self):
        """The nonterminals that can derive the empty word.

        A least fixed point: start with those having an empty right side, then
        add any whose right side consists entirely of nullable nonterminals,
        until nothing changes. Needed by every later algorithm, because a
        nullable symbol lets what follows it show through.
        """
        result = set()
        changed = True

        while changed:
            changed = False
            for left, right in self.rules:
                if left in result:
                    continue
                if all(symbol in result for symbol in right):
                    result.add(left)
                    changed = True

        return result

    def __repr__(self):
        """The rules in the usual notation, one alternative per line."""
        lines = []
        for left in sorted(self.nonterminals):
            alternatives = " | ".join(" ".join(right) or "\u03b5"
                                      for right in self.rules_for(left))
            lines.append(f"{left} ::= {alternatives}")
        return "\n".join(lines)


EMPTY = ""
"""The child a nonterminal gets when it is expanded by an epsilon rule.

Without it a nonterminal that derived nothing would be indistinguishable from a
terminal leaf, and the yield of the tree would contain the nonterminal's own
name. Textbook drawings write an epsilon at that position for the same reason.
"""


def yield_of(node):
    """The terminals of a tree, left to right, which is the word it derives."""
    if node.is_leaf():
        return [] if node.symbol == EMPTY else [node.symbol]
    return [symbol for child in node.children for symbol in yield_of(child)]


def all_parse_trees(grammar, word, limit=64):
    """Every parse tree for a word, by a chart over spans.

    Deliberately a specification rather than a parsing algorithm: it is what
    the efficient parsers in the neighbouring folders are checked against. The
    limit stops an ambiguous grammar from producing an unbounded number of
    trees for a long word.

    The chart form is not a refinement of a recursive descent, it is a
    necessity. Naive top-down search does not terminate on a left-recursive
    rule such as `E ::= E + T`, because it re-enters `E` on the same input
    position; filling spans shortest-first means the recursive occurrence is
    always looked up on a span that is already finished.
    """
    word = list(word)
    length = len(word)
    chart = {}

    for size in range(length + 1):
        for start in range(length - size + 1):
            _fill_span(grammar, word, chart, start, start + size, limit)

    return chart.get((grammar.start, 0, length), [])


def _fill_span(grammar, word, chart, start, end, limit):
    """Fill one span, iterating until unit and nullable rules stop adding trees.

    Rules whose right side can be derived within the same span, `E ::= T` or
    anything with nullable neighbours, feed back into the span being computed.
    A single pass would miss them, so the span is repeated to a fixed point.
    """
    changed = True
    while changed:
        changed = False
        for left, right in grammar.rules:
            for children in _splits(grammar, word, chart, right, start, end, limit):
                tree = Node(left, children if children else [Node(EMPTY)])
                bucket = chart.setdefault((left, start, end), [])
                if tree not in bucket and len(bucket) < limit:
                    bucket.append(tree)
                    changed = True


def _splits(grammar, word, chart, symbols, start, end, limit):
    """Every way a sequence of symbols can cover the span exactly."""
    if not symbols:
        if start == end:
            yield []
        return

    first, rest = symbols[0], symbols[1:]

    if first not in grammar.nonterminals:
        if start < end and word[start] == first:
            for others in _splits(grammar, word, chart, rest, start + 1, end, limit):
                yield [Node(first)] + others
        return

    for middle in range(start, end + 1):
        for tree in chart.get((first, start, middle), []):
            for others in _splits(grammar, word, chart, rest, middle, end, limit):
                yield [tree] + others


def leftmost_derivation(tree):
    """The sentential forms of the leftmost derivation the tree encodes.

    At each step the leftmost nonterminal is replaced by its children. The
    result is what a top-down parser produces as it runs, which is why the two
    are the same thing seen from different sides.
    """
    return _derivation(tree, leftmost=True)


def rightmost_derivation(tree):
    """The sentential forms of the rightmost derivation the tree encodes.

    Read backwards, this is the sequence of reductions a shift-reduce parser
    performs. A bottom-up parser therefore constructs a rightmost derivation in
    reverse, which is where the name of the LR family comes from.
    """
    return _derivation(tree, leftmost=False)


def _derivation(tree, leftmost):
    """Expand one nonterminal at a time, from one end, recording each form."""
    form = [tree]
    steps = [[node.symbol for node in form if node.symbol != EMPTY]]

    while True:
        indices = [index for index, node in enumerate(form) if not node.is_leaf()]
        if not indices:
            break
        index = indices[0] if leftmost else indices[-1]
        node = form[index]
        form = form[:index] + list(node.children) + form[index + 1:]
        steps.append([entry.symbol for entry in form if entry.symbol != EMPTY])

    return steps


def is_one_step(grammar, before, after):
    """Whether one sentential form follows from another by a single rule.

    Used to check a derivation rather than trust it: every consecutive pair
    must differ by replacing exactly one nonterminal with the right side of one
    of its rules.
    """
    for index, symbol in enumerate(before):
        if symbol not in grammar.nonterminals:
            continue
        for right in grammar.rules_for(symbol):
            if before[:index] + right + before[index + 1:] == after:
                return True
    return False


def language(grammar, limit):
    """Every word up to a length the grammar generates, by breadth-first search.

    The termination argument is that a sentential form whose terminals already
    exceed the limit can be discarded, since rules only ever add symbols.
    """
    seen = set()
    results = []
    frontier = [[grammar.start]]

    while frontier:
        form = frontier.pop()
        key = tuple(form)
        if key in seen:
            continue
        seen.add(key)

        terminals = [symbol for symbol in form if symbol not in grammar.nonterminals]
        if len(terminals) > limit:
            continue

        if all(symbol not in grammar.nonterminals for symbol in form):
            if form not in results:
                results.append(form)
            continue

        for index, symbol in enumerate(form):
            if symbol in grammar.nonterminals:
                for right in grammar.rules_for(symbol):
                    frontier.append(form[:index] + right + form[index + 1:])

    return sorted(results, key=lambda word: (len(word), word))


def find_ambiguity(grammar, length):
    """A shortest word with two parse trees, or `None` if there is none.

    Ambiguity is undecidable in general, so this is a search and not a
    decision: finding a witness proves ambiguity, finding none proves only
    that no short witness exists.
    """
    symbols = sorted(grammar.terminals)

    for size in range(length + 1):
        for candidate in itertools.product(symbols, repeat=size):
            word = list(candidate)
            if len(all_parse_trees(grammar, word, limit=2)) > 1:
                return word

    return None
