"""Huffman coding: shorter codes for commoner symbols, and it is provably optimal."""

from __future__ import annotations

import heapq
from collections import Counter

def build_codes(frequencies):
    """Return a code per symbol, built from a frequency count.

    A fixed-width encoding spends the same number of bits on every symbol,
    which is wasteful when some appear far more often than others. Huffman
    spends fewer bits on the common ones.

    The construction is greedy and takes two lines: repeatedly take the two
    **least** frequent items and merge them into one whose frequency is their
    sum. The tree that results assigns each symbol a code by the path to it,
    and the rarest symbols end up deepest.

    The codes are automatically **prefix-free**, meaning no code is a prefix of
    another, because symbols sit only at the leaves. That is what makes the
    stream decodable without separators: reading bit by bit, the moment a code
    matches it can only be that symbol.

    Huffman proved in 1952 that this is optimal among prefix-free codes, which
    is unusual: most greedy algorithms are heuristics, and this one is provably
    the best possible for its problem. Arithmetic coding beats it only by
    abandoning the requirement that each symbol occupy a whole number of bits.

    A counter is carried alongside the frequency so that heap comparisons never
    reach the symbols themselves, which keeps the result deterministic and
    avoids comparing types that have no ordering.

    An alphabet of one symbol is the special case: it still needs one bit, or
    the encoding would be empty and nothing could be decoded.
    """
    if not frequencies:
        return {}
    if len(frequencies) == 1:
        return {next(iter(frequencies)): "0"}

    counter = 0
    heap: list = []
    for symbol, count in frequencies.items():
        heapq.heappush(heap, (count, counter, {symbol: ""}))
        counter += 1

    while len(heap) > 1:
        left_count, _, left = heapq.heappop(heap)
        right_count, _, right = heapq.heappop(heap)

        merged = {symbol: "0" + code for symbol, code in left.items()}
        merged.update({symbol: "1" + code for symbol, code in right.items()})

        heapq.heappush(heap, (left_count + right_count, counter, merged))
        counter += 1

    return heap[0][2]

def encode(text, codes):
    """The text as a string of bits."""
    return "".join(codes[symbol] for symbol in text)

def decode(bits, codes):
    """The bits back into text, using the prefix-free property.

    Walk the stream accumulating bits and emit a symbol the moment the
    accumulated string is a code. No separators and no lookahead are needed,
    and that is entirely because no code is a prefix of another.
    """
    lookup = {code: symbol for symbol, code in codes.items()}
    output = []
    buffer = ""
    for bit in bits:
        buffer += bit
        if buffer in lookup:
            output.append(lookup[buffer])
            buffer = ""
    return "".join(output)

def encoded_length(frequencies, codes):
    """Total bits for the whole text, which is what the optimality is about."""
    return sum(count * len(codes[symbol]) for symbol, count in frequencies.items())
