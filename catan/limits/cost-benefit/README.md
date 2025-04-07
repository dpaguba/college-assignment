# Choosing the operating point

Given a cost for each of the four outcomes, the best threshold is the one with
the lowest expected cost. The module finds it by search, and only afterwards
checks it against the rule.

## The rule

For calibrated probabilities, raising an alarm pays exactly when the
probability times the cost of a miss exceeds the cost of the alarm, so the
threshold is `alarm / (alarm + miss)`. With costs 1 and 4 that is 0.2.

| | threshold | expected cost |
|---|---:|---:|
| by rule | 0.200 | 0.29418 |
| by search | 0.2125 | 0.29340 |

The thresholds differ and the costs do not: the rule is 0.26 % more expensive.
The cost curve is very flat around its minimum, so the searched threshold moves
with the sample while the cost hardly reacts. Comparing thresholds makes this
look like a disagreement; comparing costs shows it is not.

The rule assumes calibrated probabilities, which is an assumption about the
model and not about the costs. That is why the search stays in the module.

## Accuracy is a cost matrix in disguise

Maximising accuracy means setting both kinds of error to the same cost. On the
same data, with a miss nine times as expensive as a false alarm:

| chosen by | threshold |
|---|---:|
| accuracy | 0.505 |
| cost | **0.085** |

Nobody wrote down the accuracy cost matrix, and it was still applied. The
decision is made either way; the only question is whether it is made on
purpose.

## For a game AI

An AI that scores moves picks an operating point every turn: how good does a
move have to look before it gets played. The costs here are not a table but
the course of the game, and they move with the position, since a player who is
ahead pays more for a failed gamble. A fixed threshold across a whole game is
as wrong as fixed weights in the evaluation function.
