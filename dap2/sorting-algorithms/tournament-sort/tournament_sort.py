"""Tournament sort: a knockout bracket that replays only the winner's path."""

from __future__ import annotations

def tournament_sort(items, key=None):
    """Return a sorted copy of `items`.

    Play every element against its neighbour, winners advance, and the final
    winner is the smallest. Removing it invalidates only the log n matches it
    played, so the next winner costs log n rather than another full round.

    Comparing by (key, arrival order) is what keeps it stable: two equal keys
    are decided by which one entered the bracket first.
    """
    result = list(items)
    of = key or (lambda item: item)
    if len(result) < 2:
        return result

    size = 1
    while size < len(result):
        size *= 2

    leaves = [None] * size
    for arrival, value in enumerate(result):
        leaves[arrival] = (of(value), arrival, value)

    def better(left, right):
        """The smaller of two competitors, treating absence as a loss."""
        if left is None:
            return right
        if right is None:
            return left
        return left if left[:2] <= right[:2] else right

    tree = [None] * size + leaves
    for node in range(size - 1, 0, -1):
        tree[node] = better(tree[2 * node], tree[2 * node + 1])

    ordered = []
    for _ in range(len(result)):
        winner = tree[1]
        ordered.append(winner[2])

        node = size + winner[1]
        tree[node] = None
        node //= 2
        while node:
            tree[node] = better(tree[2 * node], tree[2 * node + 1])
            node //= 2

    return ordered
