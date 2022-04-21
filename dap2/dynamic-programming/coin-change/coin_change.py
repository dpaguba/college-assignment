"""Coin change: the fewest coins for an amount, and how many ways there are."""

from __future__ import annotations


def fewest_coins(amount, coins):
    """Return the smallest number of coins making `amount`, and which ones.

    The obvious greedy method, take the largest coin that fits and repeat,
    works for the euro and the dollar and fails in general. With coins
    1, 5, 10, 21, 25 and an amount of 63, greedy takes 25 + 25 + 10 + 1 + 1 + 1,
    six coins, where three 21s do it. **That failure is the reason this problem
    is taught**: it is the cleanest demonstration that a locally best choice is
    not always part of a globally best solution.

    The recurrence fixes it by considering every coin at every amount:
    `best(a) = 1 + min over coins c of best(a - c)`. Every subproblem is an
    amount, so there are only `amount` of them, and each costs one pass over
    the coins.
    """
    if amount < 0:
        raise ValueError("an amount cannot be negative")

    unreachable = float("inf")
    best = [0] + [unreachable] * amount
    used = [None] * (amount + 1)

    for total in range(1, amount + 1):
        for coin in coins:
            if coin <= total and best[total - coin] + 1 < best[total]:
                best[total] = best[total - coin] + 1
                used[total] = coin

    if best[amount] == unreachable:
        return None, []

    chosen = []
    remaining = amount
    while remaining > 0:
        chosen.append(used[remaining])
        remaining -= used[remaining]
    return best[amount], chosen


def count_ways(amount, coins):
    """How many distinct combinations make `amount`, ignoring order.

    The same table, one difference that decides everything: the **loop order**.

    Coins outside and amounts inside counts combinations, because each coin is
    considered once for all amounts, so 2 + 1 and 1 + 2 are never both counted.
    Swap the loops and the same code counts permutations instead, which is a
    different question with a much larger answer.

    Nothing in the recurrence says which is meant. The loop order is the
    specification, and that is the most common way to get this problem wrong.
    """
    if amount < 0:
        raise ValueError("an amount cannot be negative")

    ways = [1] + [0] * amount
    for coin in coins:
        for total in range(coin, amount + 1):
            ways[total] += ways[total - coin]
    return ways[amount]
