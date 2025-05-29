"""Smoothsort: heapsort over Leonardo heaps, which likes ordered input.

The Leonardo numbers, L(0)=L(1)=1 and L(k)=L(k-1)+L(k-2)+1, are the only sizes
a heap in the forest is allowed to have.
"""

from __future__ import annotations

LEONARDO = [1, 1]
while LEONARDO[-1] < 2 ** 40:
    LEONARDO.append(LEONARDO[-1] + LEONARDO[-2] + 1)

def smoothsort(items, key=None):
    """Return a sorted copy of `items`.

    Heapsort takes n log n on every input, including one that was already in
    order. Dijkstra's answer was to replace the binary heap with a string of
    Leonardo heaps whose shape follows the data: on sorted input almost no
    element ever moves, and the run collapses to linear time.

    The bookkeeping is what makes this the least implemented of the classics.
    """
    result = list(items)
    of = key or (lambda item: item)
    size = len(result)
    if size < 2:
        return result

    orders: list[int] = []

    def sift(root, order):
        """Restore one Leonardo heap by pushing its root down."""
        while order > 1:
            right = root - 1
            left = right - LEONARDO[order - 2]
            child, child_order = (
                (left, order - 1) if of(result[left]) >= of(result[right]) else (right, order - 2)
            )
            if of(result[root]) >= of(result[child]):
                return
            result[root], result[child] = result[child], result[root]
            root, order = child, child_order

    def trinkle(root, index):
        """Walk left across the forest, moving a root into the right heap."""
        while index > 0:
            previous = root - LEONARDO[orders[index]]
            if of(result[previous]) <= of(result[root]):
                break
            if orders[index] > 1:
                right = root - 1
                left = right - LEONARDO[orders[index] - 2]
                if of(result[previous]) <= max(of(result[left]), of(result[right])):
                    break
            result[root], result[previous] = result[previous], result[root]
            root, index = previous, index - 1
        sift(root, orders[index])

    for position in range(size):
        if len(orders) >= 2 and orders[-2] == orders[-1] + 1:
            orders.pop()
            orders[-1] += 1
        elif orders and orders[-1] == 1:
            orders.append(0)
        else:
            orders.append(1)
        trinkle(position, len(orders) - 1)

    for position in range(size - 1, 0, -1):
        if orders[-1] <= 1:
            orders.pop()
            continue
        order = orders.pop()
        right = position - 1
        left = right - LEONARDO[order - 2]
        orders.append(order - 1)
        trinkle(left, len(orders) - 1)
        orders.append(order - 2)
        trinkle(right, len(orders) - 1)

    return result
