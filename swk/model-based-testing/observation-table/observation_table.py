"""The observation table: what a learner knows about a system it cannot see.

Rows are input words that lead somewhere, columns are input words asked from
there, and a cell holds what the system answered. For Mealy machines the
lecture keeps only the **last** output symbol of running ``u . v``, which is
enough to tell states apart and keeps the table readable.

    U     is the set of access words, one per state of the hypothesis
    U . A is the same words extended by one symbol, the fringe
    V     is the set of suffixes, the experiments that distinguish states

Two properties make a table usable:

- **closed**: every fringe row already appears in the upper part, so every
  transition of the hypothesis has a target
- **consistent**: rows that look equal stay equal after one more symbol, so
  the transitions are well defined

Both are repaired by adding a row or a column, and each repair costs queries.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mealy-machines"))

from mealy_machines import MealyMachine


@dataclass
class ObservationTable:
    """Rows, columns and cells, filled by asking membership queries."""

    alphabet: tuple
    membership: object
    prefixes: list = field(default_factory=lambda: [""])
    suffixes: list = field(default_factory=list)
    cells: dict = field(default_factory=dict)
    queries: int = 0

    def __post_init__(self):
        """Starts with the alphabet as suffixes and fills the table."""
        if not self.suffixes:
            self.suffixes = list(self.alphabet)
        self.fill()

    @property
    def fringe(self):
        """The words of U extended by one symbol that are not already in U."""
        found = []
        for prefix in self.prefixes:
            for symbol in self.alphabet:
                word = prefix + symbol
                if word not in self.prefixes and word not in found:
                    found.append(word)
        return found

    def fill(self):
        """Ask a membership query for every cell that is still empty.

        Every query is a run of the real system, which is the expensive
        resource the algorithm is measured by. Cells are cached, so a word is
        never asked twice.
        """
        for prefix in self.prefixes + self.fringe:
            for suffix in self.suffixes:
                if (prefix, suffix) not in self.cells:
                    self.cells[(prefix, suffix)] = self.membership(prefix + suffix)
                    self.queries += 1

    def row(self, prefix):
        """The row of a word: what the system answers for each suffix."""
        return tuple(self.cells[(prefix, suffix)] for suffix in self.suffixes)

    def closed(self):
        """Return a fringe word whose row is missing from the upper part, or None."""
        known = {self.row(prefix) for prefix in self.prefixes}
        for word in self.fringe:
            if self.row(word) not in known:
                return word
        return None

    def consistent(self):
        """Return a witness of inconsistency, or None.

        A witness is two upper rows that agree, a symbol, and a suffix on which
        their extensions disagree. The fix is to add ``symbol + suffix`` as a
        new column, which splits the two rows that should never have been
        equal.
        """
        for first in self.prefixes:
            for second in self.prefixes:
                if first >= second or self.row(first) != self.row(second):
                    continue
                for symbol in self.alphabet:
                    left, right = first + symbol, second + symbol
                    for index, suffix in enumerate(self.suffixes):
                        if self.cells[(left, suffix)] != self.cells[(right, suffix)]:
                            return first, second, symbol, suffix
        return None

    def add_prefix(self, word):
        """Move a fringe word into the upper part and refill."""
        if word not in self.prefixes:
            self.prefixes.append(word)
            self.fill()

    def add_suffix(self, word):
        """Add a column and refill."""
        if word not in self.suffixes:
            self.suffixes.append(word)
            self.fill()

    def close(self):
        """Add rows until the table is closed, returning how many were added."""
        added = 0
        while True:
            word = self.closed()
            if word is None:
                return added
            self.add_prefix(word)
            added += 1

    def make_consistent(self):
        """Add columns until the table is consistent, returning how many were added."""
        added = 0
        while True:
            witness = self.consistent()
            if witness is None:
                return added
            _, _, symbol, suffix = witness
            self.add_suffix(symbol + suffix)
            added += 1

    def hypothesis(self):
        """Build the Mealy machine the table describes.

        States are the distinct rows of the upper part. The transition for a
        symbol goes from the row of ``u`` to the row of ``u . symbol``, and the
        output is the cell ``(u, symbol)``, which is why the suffix set always
        contains the single symbols: without them the outputs would be unknown.
        """
        names = {}
        for prefix in self.prefixes:
            names.setdefault(self.row(prefix), f"s{len(names)}")

        access = {}
        for prefix in self.prefixes:
            access.setdefault(self.row(prefix), prefix)

        transitions = {}
        for row, name in names.items():
            prefix = access[row]
            transitions[name] = {}
            for symbol in self.alphabet:
                target_row = self.row(prefix + symbol)
                if target_row not in names:
                    raise ValueError("the table is not closed, no hypothesis exists")
                transitions[name][symbol] = (names[target_row],
                                             self.cells[(prefix, symbol)])

        return MealyMachine(transitions, names[self.row("")], name="H")

    def __str__(self):
        """The table with its two halves, as the lecture draws it."""
        width = max(len(word) for word in self.prefixes + self.fringe + [""]) + 2
        header = " " * (width + 8) + " | ".join(f"{suffix or 'eps':>4}" for suffix in self.suffixes)
        lines = [header, "-" * len(header)]

        for prefix in self.prefixes:
            cells = " | ".join(f"{self.cells[(prefix, suffix)]:>4}" for suffix in self.suffixes)
            lines.append(f"  U     {prefix or 'eps':<{width}} {cells}")
        lines.append("-" * len(header))
        for prefix in self.fringe:
            cells = " | ".join(f"{self.cells[(prefix, suffix)]:>4}" for suffix in self.suffixes)
            lines.append(f"  U.A   {prefix:<{width}} {cells}")

        return "\n".join(lines)
