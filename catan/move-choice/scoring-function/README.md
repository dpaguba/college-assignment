# The scoring function

The rule-based AI scores a move as a weighted sum of features: expected yield,
resource variety, victory points, and how much it blocks an opponent. Only the
ratios of the weights matter; multiplying all of them by 7.5 leaves every
ordering unchanged.

## The weights move with the game

| | early | middle | late |
|---|---:|---:|---:|
| expected yield | 10.0 | 5.0 | 1.0 |
| variety | 3.0 | 1.5 | 0.5 |
| points | 1.0 | 3.0 | 10.0 |
| blocks | 0.5 | 1.5 | 3.0 |

The answer to the slide's question about how the weighting shifts is in the
winning condition: the game is won with points and not with cards. Early, the
yield pays for every later point; late, only a point counts, even from a move
that ruins the economy.

## What a weighted sum cannot say

Three corners: one with a lot of lumber and no brick, one with a lot of brick
and no lumber, one with half of each. Building needs both, so the balanced
corner is the best one. No linear scoring function can express that.

The proof is one line. With features (1,0), (0,1) and (0.5, 0.5), preferring
the third over the first requires `w₂ > w₁`, and preferring it over the second
requires `w₁ > w₂`. A grid search over **4 225** weight vectors finds none
that works, as it must. A single product term of the two features solves it
immediately.

This is the concrete reason a hand-written scoring function for Catan needs
interactions and not just weights, and it is the same reason the second AI in
the project is not simply a tuned version of the first.

## Why the rule-based AI matters even though it never learns

It generates the training data, and the slide is blunt about the consequence:
better data give a better AI. A weak rule-based AI produces games in which
nothing sensible ever happens, and sensible play cannot be learned from them.

It also fixes which features get measured at all: what is not a feature here
is invisible to the learner later. And its speed is the size of the dataset.
