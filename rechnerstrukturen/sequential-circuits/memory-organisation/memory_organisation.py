"""Memory organisation: cells, decoders, and the SRAM against DRAM trade.

A memory of `n` words needs `log2 n` address bits and a decoder turning them
into one word line. A flat decoder for a million words needs a million output
lines, which is why real memories are two-dimensional: rows and columns, each
decoded separately, with the cell at the intersection.

The cell itself is the other decision. An SRAM cell is six transistors and
holds its value as long as it is powered. A DRAM cell is one transistor and a
capacitor, and the charge leaks, so every row must be read and rewritten every
few milliseconds. Six times the area against a refresh controller and a slower
access, which is why caches are SRAM and main memory is DRAM.
"""

from __future__ import annotations

import math


def address_bits(words):
    """How many address bits a memory of a given size needs."""
    return max(0, math.ceil(math.log2(words))) if words > 1 else 0


class Memory:
    """A word-addressed memory of fixed width."""

    def __init__(self, words, width):
        """Allocate the words and record the width in bits."""
        self.words = words
        self.width = width
        self.cells = [0] * words

    def read(self, address):
        """Read one word."""
        self._check(address)
        return self.cells[address]

    def write(self, address, value):
        """Write one word, rejecting an out-of-range value."""
        self._check(address)
        if not 0 <= value < (1 << self.width):
            raise ValueError(f"{value} does not fit in {self.width} bits")
        self.cells[address] = value

    def _check(self, address):
        """Reject an address outside the memory."""
        if not 0 <= address < self.words:
            raise IndexError(f"address {address} outside 0..{self.words - 1}")


def decoder_lines(words, dimensions=1):
    """How many decoder output lines an organisation needs.

    One dimension needs one line per word. Two dimensions need a row decoder
    and a column decoder, so the count drops from `n` to about `2 * sqrt(n)`:
    for a million words, from a million lines to two thousand.
    """
    if dimensions == 1:
        return words
    side = round(words ** (1 / dimensions))
    return dimensions * side


def needs_refresh(kind):
    """Whether a memory technology loses its contents without refreshing."""
    return kind == "dram"


def transistors_per_cell(kind):
    """Transistors in one storage cell.

    Six against one, which is the whole reason main memory is DRAM. The
    capacitor in a DRAM cell is not free either, but it is built in the third
    dimension and costs no area.
    """
    return {"sram": 6, "dram": 1}[kind]


def refresh_overhead(rows, refresh_period_ms, row_time_ns):
    """Fraction of time a DRAM spends refreshing rather than serving.

    Small, a few percent, and not zero: while a row is being refreshed the bank
    cannot answer. It is one of the reasons DRAM latency is quoted as a range.
    """
    total = rows * row_time_ns
    return total / (refresh_period_ms * 1_000_000)


def access_time(kind, row_hit):
    """Relative access cost, in arbitrary units.

    A DRAM read that hits an already-open row is much cheaper than one that
    does not, because opening a row destroys it and it has to be written back.
    That asymmetry is why memory controllers reorder requests, and why a
    sequential access pattern is worth so much more than a random one.
    """
    if kind == "sram":
        return 1
    return 2 if row_hit else 5
