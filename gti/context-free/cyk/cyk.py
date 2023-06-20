"""CYK: the word problem for context-free grammars, in cubic time.

Cocke, Younger and Kasami. The grammar must be in
[Chomsky normal form](../chomsky-normal-form/), and that requirement is what
makes the algorithm work: every rule is either ``A -> a`` or ``A -> B C``, so a
substring of length one is covered by a single rule, and a longer one splits
into exactly two parts whose covering variables are already known.

The table has one cell per substring. ``table[i][j]`` holds every variable that
derives the substring starting at ``i`` of length ``j+1``, filled by increasing
length, and the word is in the language when the start symbol is in the cell
for the whole word.

O(n³ · |G|) time and O(n²) space. That is the price of context-freeness: a
regular language is decided in linear time and this is the general bound for
the level above.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "context-free-grammars"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "chomsky-normal-form"))

from chomsky_normal_form import is_chomsky_normal_form, to_chomsky_normal_form
from context_free_grammars import Grammar


def table(grammar, word):
    """Fill the CYK table: which variables derive which substring.

    Rows are lengths and columns are starting positions, which is the layout
    the exercises draw. The bottom row comes from the terminal rules, and each
    row above tries every split of the substring into two non-empty parts.
    """
    correct, problems = is_chomsky_normal_form(grammar)
    if not correct:
        raise ValueError(f"the grammar is not in Chomsky normal form: {problems[:3]}")

    length = len(word)
    cells = [[set() for _ in range(length)] for _ in range(length)]

    for position, symbol in enumerate(word):
        for variable, sides in grammar.rules.items():
            if (symbol,) in sides:
                cells[0][position].add(variable)

    for span in range(2, length + 1):
        for start in range(length - span + 1):
            for split in range(1, span):
                left = cells[split - 1][start]
                right = cells[span - split - 1][start + split]

                for variable, sides in grammar.rules.items():
                    for production in sides:
                        if (len(production) == 2 and production[0] in left
                                and production[1] in right):
                            cells[span - 1][start].add(variable)

    return cells


def accepts(grammar, word):
    """Whether the grammar derives the word.

    The empty word is a special case: it is in the language exactly when the
    start symbol has an empty rule, since Chomsky normal form allows that rule
    and no other way of producing it.
    """
    if not word:
        return () in grammar.rules.get(grammar.start, [])

    cells = table(grammar, word)
    return grammar.start in cells[len(word) - 1][0]


def parse_tree(grammar, word):
    """One derivation tree for the word, or None.

    Built by walking the table back down: for the start symbol over the whole
    word, find a rule and a split whose two halves are covered, and recurse.
    Any choice gives a valid tree, and which one comes out depends on the
    order the rules are tried, which is exactly the freedom an ambiguous
    grammar leaves.
    """
    if not word:
        return (grammar.start, []) if accepts(grammar, word) else None

    cells = table(grammar, word)
    if grammar.start not in cells[len(word) - 1][0]:
        return None

    def build(variable, start, span):
        """The parse tree for one variable over one span of the word."""
        if span == 1:
            return (variable, [word[start]])

        for split in range(1, span):
            left_cell = cells[split - 1][start]
            right_cell = cells[span - split - 1][start + split]

            for production in grammar.rules.get(variable, []):
                if (len(production) == 2 and production[0] in left_cell
                        and production[1] in right_cell):
                    return (variable, [build(production[0], start, split),
                                       build(production[1], start + split, span - split)])

        return None

    return build(grammar.start, 0, len(word))


def count_parses(grammar, word, limit=10 ** 9):
    """How many derivation trees the word has.

    Counting instead of enumerating is what makes an ambiguity check
    affordable: the number of trees can grow exponentially while the table
    stays cubic. More than one tree means the grammar is ambiguous for this
    word.
    """
    if not word:
        return 1 if () in grammar.rules.get(grammar.start, []) else 0

    length = len(word)
    counts = [[{} for _ in range(length)] for _ in range(length)]

    for position, symbol in enumerate(word):
        for variable, sides in grammar.rules.items():
            if (symbol,) in sides:
                counts[0][position][variable] = counts[0][position].get(variable, 0) + 1

    for span in range(2, length + 1):
        for start in range(length - span + 1):
            cell = counts[span - 1][start]
            for split in range(1, span):
                left = counts[split - 1][start]
                right = counts[span - split - 1][start + split]

                for variable, sides in grammar.rules.items():
                    for production in sides:
                        if len(production) != 2:
                            continue
                        first = left.get(production[0], 0)
                        second = right.get(production[1], 0)
                        if first and second:
                            cell[variable] = min(limit, cell.get(variable, 0) + first * second)

    return counts[length - 1][0].get(grammar.start, 0)


def show_table(grammar, word):
    """The table as text, the way the exercise draws it: longest span on top."""
    cells = table(grammar, word)
    length = len(word)
    rows = []

    for span in range(length, 0, -1):
        entries = []
        for start in range(length - span + 1):
            content = ",".join(sorted(cells[span - 1][start])) or "-"
            entries.append(f"{content:^12}")
        rows.append(f"  len {span}: " + " ".join(entries))

    rows.append("          " + " ".join(f"{symbol:^12}" for symbol in word))
    return "\n".join(rows)


def language(grammar, max_length, alphabet=None):
    """Every word up to a length, decided by running CYK on each candidate.

    Slower than deriving forwards and completely reliable, which makes it the
    reference the grammar module's own enumeration is checked against.
    """
    alphabet = sorted(alphabet or grammar.terminals)
    found = []
    queue = [""]

    while queue:
        word = queue.pop(0)
        if accepts(grammar, word):
            found.append(word)
        if len(word) < max_length:
            queue.extend(word + symbol for symbol in alphabet)

    return found
