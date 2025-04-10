# Deciding against the dice

Three kinds of node: a leaf carries its value, a decision node takes the best
of its children, and a chance node averages them with their probabilities.
That third case is the whole difference from minimax; against dice there is
nothing to maximise, only to average.

The recursion is checked against a computation that shares nothing with it:
every fixed policy is enumerated, its expected value computed, and the best
taken. Over 200 random trees the two agree exactly.

## The average is not the best case

Two corners, one at 6 and 8 paying one card, one at 2 and 12 paying four:

| | expectation | best case |
|---|---:|---:|
| 6 and 8 | **0.278** | 1 |
| 2 and 12 | 0.222 | **4** |

Choosing by expectation takes the first, choosing by best case takes the
second, and whoever plays for the twelve waits 36 rolls for it on average.
That is the mistake a scoring function without probabilities makes, and it
looks like optimism rather than like an error.

## The seven belongs in the tree

The seven pays no hex, so it drops out of an income calculation without anyone
noticing. Put it back in, for a player holding nine cards:

| | value of a turn |
|---|---:|
| without the seven | **+0.333** |
| with the seven | **−0.389** |

The sign changes. A turn spent holding nine cards has a negative expected
value once the discard is counted, and a tree that omits the branch will
happily recommend accumulating.
