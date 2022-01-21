"""Dynamic array: fixed storage that pretends to grow, by doubling when it fills."""

from __future__ import annotations

INITIAL_CAPACITY = 4

class DynamicArray:
    """The structure behind Python's list, Java's ArrayList and C++'s vector.

    Memory comes in fixed blocks, so an array cannot actually grow. What a
    dynamic array does is allocate a larger block and copy, and the only
    interesting question is how much larger.

    Growing by a constant, say four slots at a time, makes n appends cost
    O(n²): each of the n/4 reallocations copies everything so far, and the sum
    of 4 + 8 + 12 + ... is quadratic. **Doubling** makes the same n appends
    cost O(n): the copies are 1 + 2 + 4 + ... + n, a geometric series that sums
    to less than 2n. So an append is O(1) amortised, even though one append in
    every n is O(n).

    That is the standard example of amortised analysis, and the reason it
    matters: the worst case per operation is bad, and the worst case per
    sequence of operations is not.

    Shrinking is deliberately lazy, at a quarter full rather than a half. If it
    halved at half, a sequence of append, pop, append, pop at the boundary
    would reallocate on every single call.
    """

    def __init__(self, values=None):
        """An array holding the given values."""
        self._capacity = INITIAL_CAPACITY
        self._slots: list = [None] * self._capacity
        self._count = 0
        for value in values or ():
            self.append(value)

    @property
    def capacity(self):
        """How many slots are allocated, which is at least the number in use."""
        return self._capacity

    def _resize(self, capacity):
        """Moves the entries into an array of the given capacity."""
        capacity = max(INITIAL_CAPACITY, capacity)
        moved = [None] * capacity
        for index in range(self._count):
            moved[index] = self._slots[index]
        self._slots = moved
        self._capacity = capacity

    def _check(self, index):
        """Rejects an index outside the entries currently stored."""
        if not 0 <= index < self._count:
            raise IndexError(f"index {index} is outside an array of {self._count}")

    def append(self, value):
        """Add at the end, doubling the storage when it is full.

        O(1) amortised: the doubling makes the total cost of n appends linear.
        """
        if self._count == self._capacity:
            self._resize(self._capacity * 2)
        self._slots[self._count] = value
        self._count += 1

    def insert(self, index, value):
        """Insert at a position, shifting the tail right. O(n)."""
        if not 0 <= index <= self._count:
            raise IndexError(f"index {index} is outside an array of {self._count}")
        if self._count == self._capacity:
            self._resize(self._capacity * 2)
        for position in range(self._count, index, -1):
            self._slots[position] = self._slots[position - 1]
        self._slots[index] = value
        self._count += 1

    def pop(self):
        """Remove and return the last value. O(1) amortised."""
        if self._count == 0:
            raise IndexError("pop from an empty array")
        return self.remove_at(self._count - 1)

    def remove_at(self, index):
        """Remove the value at a position, shifting the tail left.

        Shrinking happens at a quarter full, not a half: halving at half would
        thrash, resizing on every operation for a sequence of appends and pops
        around the boundary.
        """
        self._check(index)
        value = self._slots[index]
        for position in range(index, self._count - 1):
            self._slots[position] = self._slots[position + 1]
        self._slots[self._count - 1] = None
        self._count -= 1
        if 0 < self._count <= self._capacity // 4:
            self._resize(self._capacity // 2)
        return value

    def __getitem__(self, index):
        """The value at the index."""
        self._check(index)
        return self._slots[index]

    def __setitem__(self, index, value):
        """Writes the value at the index."""
        self._check(index)
        self._slots[index] = value

    def __iter__(self):
        """The values, in order."""
        for index in range(self._count):
            yield self._slots[index]

    def __len__(self):
        """How many entries the structure holds."""
        return self._count
