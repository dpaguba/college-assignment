"""0/1 knapsack: pick items to maximise value without exceeding a weight limit."""

from __future__ import annotations

def knapsack_01(items, capacity):
    """Return the best total value and the items that give it.

    The 0/1 means each item is taken whole or not at all, which is what makes
    the problem hard: no greedy rule is correct. Sorting by value per weight
    and taking greedily is right for the fractional version, where items can be
    split, and wrong here. In the standard instance, weights 10, 20, 30 with
    values 60, 100, 120 and a capacity of 50, greedy takes the first two for
    160 while the answer is the last two for 220.

    The recurrence considers each item once against every capacity:

        best(i, c) = max(best(i-1, c), value[i] + best(i-1, c - weight[i]))

    Take it or leave it, and both branches are already solved. The table has
    n·capacity cells and each costs one comparison.

    **That is not polynomial time.** The input needs only log(capacity) bits to
    write down, so a table of size capacity is exponential in the input length.
    The problem is NP-complete, and this is a pseudo-polynomial algorithm: fast
    when the numbers are small, useless when they are large. That distinction is
    worth holding on to, because it is the one most people miss.

    The chosen items are read back by walking the rows upwards: an item was
    taken exactly where the value changed between one row and the next.
    """
    if capacity < 0:
        raise ValueError("a capacity cannot be negative")

    count = len(items)
    table = [[0] * (capacity + 1) for _ in range(count + 1)]

    for index in range(1, count + 1):
        weight, value = items[index - 1]
        for limit in range(capacity + 1):
            table[index][limit] = table[index - 1][limit]
            if weight <= limit:
                with_item = value + table[index - 1][limit - weight]
                if with_item > table[index][limit]:
                    table[index][limit] = with_item

    chosen = []
    limit = capacity
    for index in range(count, 0, -1):
        if table[index][limit] != table[index - 1][limit]:
            weight, value = items[index - 1]
            chosen.append(items[index - 1])
            limit -= weight

    return table[count][capacity], list(reversed(chosen))

def knapsack_01_rolling(items, capacity):
    """The same value using one row instead of the full table.

    Each row reads only the row above, so one array suffices. The catch is the
    direction: the capacities must be walked **downwards**. Going up would let
    an item be taken twice, because the cell it reads would already include
    itself, and the answer silently becomes the unbounded knapsack.

    One reversed loop is the entire difference between the two problems, which
    is why the unbounded version next door looks almost identical.

    The trade is that the chosen items can no longer be recovered: the
    information needed to walk back was in the rows that were overwritten.
    """
    if capacity < 0:
        raise ValueError("a capacity cannot be negative")

    best = [0] * (capacity + 1)
    for weight, value in items:
        for limit in range(capacity, weight - 1, -1):
            best[limit] = max(best[limit], value + best[limit - weight])
    return best[capacity]
