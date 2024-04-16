"""Jump search: skip forward in fixed blocks, then walk back through one."""

from __future__ import annotations

from math import isqrt

def jump_search(items, target, key=None, step=None):
    """Return the index of `target` in a sorted sequence, or -1.

    Jump ahead in blocks until the block's last element is not smaller than the
    target, then scan that one block linearly. With a block size of b the cost
    is n/b jumps plus b steps, and calculus puts the minimum at b = √n, giving
    O(√n).

    Slower than binary search, and still useful in one situation: media where
    jumping backwards is expensive. On tape, or a singly linked list, binary
    search's habit of bouncing between distant positions costs far more than
    the extra comparisons here, because this one only ever moves forward.
    """
    of = key or (lambda item: item)
    size = len(items)
    if size == 0:
        return -1

    block = step or max(1, isqrt(size))

    previous, current = 0, block
    while current < size and of(items[current - 1]) < target:
        previous, current = current, current + block
    current = min(current, size)

    for index in range(previous, current):
        if of(items[index]) == target:
            return index

    return -1
