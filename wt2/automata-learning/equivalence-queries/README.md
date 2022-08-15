# Equivalence queries

Three ways to ask whether a learned model is right.

**Exhaustive** enumerates every word up to a length. Complete up to that
length, and the count grows geometrically: 15 words up to length 3 over two
letters, 40 over three.

**Random sampling** is cheap and guarantees nothing. The module builds a case
where the model and the target differ on exactly one word of length 5:
the ordered search finds `aaaaa`, and 200 random words of length at most 3
find nothing at all.

**The W-method** combines a set that reaches every state, words up to the
number of assumed extra states, and a set that tells any two states apart. It
is complete under an assumption about the state count and it is smaller: 27
tests against 31 words for a three-state machine, and the gap widens quickly.

In practice the oracle is the running system, and a gap in the model is found
when someone uses the path that was never tried.
