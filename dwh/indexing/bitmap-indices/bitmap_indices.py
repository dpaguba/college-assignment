"""One bitmap per value, and a query that becomes a bitwise operation.

A bitmap index stores, for each distinct value of a column, a bit per row
saying whether that row has it. A predicate is then a lookup, a disjunction
is a bitwise or, and a conjunction across columns is a bitwise and, which is
why the index suits the star join of the previous block.

The size is rows times distinct values, so the index is small for a column
with five values and larger than the table for a column with a million. That
is the whole rule for when to use it, and the module computes both sides.
"""


def build(column):
    """One bitmap per distinct value."""
    values = sorted(set(column))
    return {value: [1 if entry == value else 0 for entry in column]
            for value in values}


def union(first, second):
    """The bitwise or of two bitmaps."""
    return [a | b for a, b in zip(first, second)]


def intersection(first, second):
    """The bitwise and."""
    return [a & b for a, b in zip(first, second)]


def complement(bitmap):
    """The bitwise not."""
    return [1 - bit for bit in bitmap]


def size(rows, distinct):
    """The uncompressed size of the index in bits."""
    return rows * distinct


def is_suitable(rows, distinct, factor=0.1):
    """Whether the index is smaller than a fraction of the table's rows."""
    return distinct <= rows * factor / 8


def rows_matching(bitmap):
    """The row numbers a bitmap selects."""
    return [index for index, bit in enumerate(bitmap) if bit]
