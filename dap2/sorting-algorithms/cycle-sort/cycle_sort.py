"""Cycle sort: move each element straight to its final position, once."""

from __future__ import annotations

def cycle_sort(items, key=None):
    """Return a sorted copy of `items`.

    Every other sort writes elements repeatedly. This one counts how many
    elements are smaller than the current value, which is exactly where that
    value belongs, and writes it there. Each element is written at most once,
    which makes the number of writes theoretically minimal.

    That matters for memory that wears out with every write, EEPROM and flash,
    where a write costs far more than the n² comparisons it takes to avoid one.

    Equal keys are skipped past so a value lands after them rather than among
    them, which keeps the write count minimal. One rotation of a cycle is
    rarely enough: the displaced value has its own home, and so does whatever
    sits there.
    """
    result = list(items)
    of = key or (lambda item: item)

    for start in range(len(result) - 1):
        value = result[start]

        position = start + sum(
            1 for index in range(start + 1, len(result)) if of(result[index]) < of(value)
        )
        if position == start:
            continue
        while of(value) == of(result[position]):
            position += 1
        result[position], value = value, result[position]

        while position != start:
            position = start + sum(
                1 for index in range(start + 1, len(result)) if of(result[index]) < of(value)
            )
            while of(value) == of(result[position]):
                position += 1
            result[position], value = value, result[position]

    return result
