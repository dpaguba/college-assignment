# Recursive algorithms

Three examples from chapter five, chosen because they recurse in three
different shapes.

| | |
|---|---|
| the pots | two calls, producing a sequence of moves |
| the stairs | two calls, producing a count |
| loading the ship | branching with abandonment, producing an answer |

**The pots.** The towers of Hanoi in the lecture's telling. Ten discs need
1023 moves, and the count and the move list are produced by different code, so
each checks the other: the moves are replayed onto three stacks and the rule
that no disc rests on a smaller one is verified for five discs.

**The stairs.** Steps of one or two give the Fibonacci numbers, so twenty
steps have 10 946 ways. With steps of up to three the same twenty steps have
121 415, because the recursion branches three ways instead of two. Neither
number is small enough to check by hand, which is the point of writing the
recursion rather than reasoning about the count.

**Loading the ship.** Each container goes to port or to starboard, and the
divergence is the running difference. A branch is abandoned as soon as the
divergence exceeds what the ship tolerates, and that abandonment is what makes
this backtracking rather than enumeration.

## The tolerance is decided during loading, not at the end

For containers of 3, 5, 2 and 8, no tolerance below four admits a solution,
even though the final imbalance could in principle be as low as two. The first
container placed tilts the ship by its own weight, and the check applies after
every container, so the smallest tolerable value is bounded below by what
happens in the middle of the work rather than by the outcome.

The fifth sheet asks for two variants. Requiring exactly zero at the end
(`existsTotalBalance`) is a different question, since it constrains only the
result, and adding a third, central hold that does not affect the balance
turns the binary search tree ternary and makes the per-hold limit the only
thing that prunes it.

Every answer is checked against brute force over all sign patterns on 80
random inputs, which is the point of having an oracle for a backtracking
search: the pruning is where these algorithms go wrong, and pruning a branch
that had a solution in it produces a plausible-looking wrong answer.
