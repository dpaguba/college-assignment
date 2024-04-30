# Decision trees

The exercise's table has 24 people described by gender, glasses, age, hair
colour, beard and accessory. Two rows are both called Tina, so there are 23
distinct names and the entropy of the target is 4.5016 bits, just under the
4.5236 of 23 equally likely names.

## Gender

| value | people | entropy |
|---|---|---|
| f | 7 | 2.5216 |
| m | 17 | 4.0875 |

Weighted remainder 3.6308, information gain **0.8709** bits, the smallest of
the six attributes.

## Which attribute is best

| attribute | gain |
|---|---|
| hair colour | 2.2894 |
| accessory | 1.9591 |
| beard | 1.2410 |
| age | 0.9544 |
| glasses | 0.9183 |
| gender | 0.8709 |

Hair colour wins, and the reason is visible in its split: five values, none
of them holding more than six people, so the uncertainty falls furthest in
one step. Gender splits 17 against 7 and barely helps. Information gain
rewards attributes with many values, which is also its known weakness and the
reason the gain ratio exists.

## Not every person can be identified

Two pairs share their entire attribute vector: Philipp and Hannes, and Tina
and Ute. No tree can separate them, whatever attribute it tests, because the
data does not distinguish them. The ID3 tree built here classifies 22 of the
24 rows correctly, and the two it misses are exactly one from each pair.

A tree tests one attribute per node, so the regions it produces are bounded
by axis-parallel cuts. A boundary at an angle has to be approximated by a
staircase, which is why a tree can need many levels for something a single
line would separate.
