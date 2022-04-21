# Coin change

The fewest coins for an amount, and how many ways there are.

| | |
|---|---|
| Time | O(n · amount) |
| Space | O(amount) |
| Table shape | linear |

## The idea

Greedy, take the largest coin that fits and repeat, works for the euro and the
dollar and fails in general. With coins 1, 5, 10, 21, 25 and an amount of 63, greedy
takes 25 + 25 + 10 + 1 + 1 + 1, six coins, where three 21s do it.

**That failure is why the problem is taught.** It is the cleanest demonstration that
a locally best choice need not belong to a globally best solution, which is exactly
the boundary between greedy algorithms and dynamic programming.

## The recurrence

```
fewest(a) = 1 + min over coins c of fewest(a - c)
```

## What is worth noticing

Counting the ways is the same table with one difference that decides everything:
**the loop order**.

Coins outside and amounts inside counts combinations, because each coin is
considered once for all amounts, so 2+1 and 1+2 are never both counted. Swap the
loops and the identical code counts permutations, a different question with a much
larger answer. Nothing in the recurrence says which is meant; the loop order is the
specification.
