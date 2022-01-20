"""Binary heap: a tree kept in an array, where the parent is always smaller."""

from __future__ import annotations

class BinaryHeap:
    """A priority queue: the smallest element is always one step away.

    A sorted array gives the minimum instantly but costs n per insert. An
    unsorted array inserts instantly but costs n to find the minimum. A heap
    gives log n for both, which is the compromise that made Dijkstra's
    algorithm practical.

    The trick is that a heap is not fully sorted, only partially: a parent is
    smaller than its children, and that is all. No relation between siblings is
    maintained, and maintaining none is exactly what makes both operations
    logarithmic.

    There are no nodes and no pointers. The tree lives in a flat array with
    children of i at 2i+1 and 2i+2, so the structure is arithmetic rather than
    allocation, and the whole thing is contiguous in memory.

    Building from an existing list costs O(n), not O(n log n). The proof is a
    sum over levels: most nodes are leaves and sift down no distance at all,
    and that surprising bound is a standard exam question.
    """

    def __init__(self, values=None, key=None):
        """A heap over the given values, built in linear time."""
        self._of = key or (lambda item: item)
        self._items = list(values) if values else []
        for root in range(len(self._items) // 2 - 1, -1, -1):
            self._sift_down(root)

    def _sift_up(self, index):
        """Moves a value towards the root until the heap condition holds."""
        while index > 0:
            parent = (index - 1) // 2
            if self._of(self._items[index]) >= self._of(self._items[parent]):
                return
            self._items[index], self._items[parent] = (
                self._items[parent],
                self._items[index],
            )
            index = parent

    def _sift_down(self, index):
        """Moves a value towards the leaves until it holds."""
        size = len(self._items)
        while True:
            smallest = index
            for child in (2 * index + 1, 2 * index + 2):
                if child < size and self._of(self._items[child]) < self._of(
                    self._items[smallest]
                ):
                    smallest = child
            if smallest == index:
                return
            self._items[index], self._items[smallest] = (
                self._items[smallest],
                self._items[index],
            )
            index = smallest

    def push(self, item):
        """Add an item and let it rise to its place. O(log n)."""
        self._items.append(item)
        self._sift_up(len(self._items) - 1)

    def pop(self):
        """Remove and return the smallest item.

        Removal moves the last element to the root and sinks it, which is why
        it costs log n rather than the n a shift would.
        """
        if not self._items:
            raise IndexError("pop from an empty heap")
        smallest = self._items[0]
        last = self._items.pop()
        if self._items:
            self._items[0] = last
            self._sift_down(0)
        return smallest

    def peek(self):
        """Smallest item without removing it.

        O(1), since it is always at the root.
        """
        return self._items[0] if self._items else None

    def is_a_heap(self):
        """Every parent is no larger than its children."""
        return all(
            self._of(self._items[parent]) <= self._of(self._items[child])
            for parent in range(len(self._items))
            for child in (2 * parent + 1, 2 * parent + 2)
            if child < len(self._items)
        )

    def __len__(self):
        """How many entries the structure holds."""
        return len(self._items)
