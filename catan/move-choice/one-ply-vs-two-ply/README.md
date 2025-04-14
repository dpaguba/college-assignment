# How far to look ahead

A game tree with known leaf values, and a heuristic that is wrong in a
specific way. The heuristic prefers A at the root, and A is correct: the ten
lies there. One level down, B looks better, because a node with an estimate of
nine sits under it with nothing behind it.

| | move chosen | true value |
|---|---|---:|
| depth 1 | A | **10** |
| depth 2 | B | **0** |

The deeper search loses everything. This is not a constructed exception; it is
what happens whenever the estimate does not get better closer to the leaves.
Searching deeper only helps under that assumption, and for a hand-written
evaluation function the assumption is a hope.

## What it costs

| depth | nodes |
|---:|---:|
| 1 | 3 |
| 2 | 7 |
| 3 | 11 |

And in Catan there is a second branching factor: after every move the dice
open eleven cases. One move of lookahead therefore costs eleven times the
number of own moves, not twice.

## The order the project uses is the right one

Milestone 2 asks for an evaluation function and milestone 3 for a learned one;
search over the top comes last if at all. Given the result above, that is the
correct order: depth is only worth its cost once the evaluation is worth
trusting near the leaves.
