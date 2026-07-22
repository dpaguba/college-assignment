# Two kinds of uncertainty

The entropy of the averaged prediction is the total. The average of the
individual entropies is the part no amount of information removes. The
difference is the mutual information between prediction and model choice, that
is, the disagreement among the members.

## The identity, and why it is not enough on its own

Total = noise + disagreement holds by construction here, because the second
part is computed as the remainder. Mutation testing showed that checking only
the identity catches nothing: scaling the first part by 0.98 leaves the
identity intact. Both parts are therefore recomputed independently in the
verification, and only then does the check bite.

## What more data remove

Twelve models, each fitted on its own draw from a coin with p = 0.7:

| sample size | total | noise | disagreement |
|---:|---:|---:|---:|
| 5 | 0.940 | 0.879 | **0.0614** |
| 100 | 0.908 | 0.902 | 0.0059 |
| 1000 | 0.882 | 0.882 | **0.0004** |

The disagreement falls by a factor of 140. The noise stays at 0.88 bits, which
is the entropy of a 0.7 coin: no dataset turns a coin into a certainty.

## Why the distinction is practical

High disagreement says that collecting more data in this region is worth
something, and that is the whole basis of active learning. High noise says
that more data in this region will change nothing, and the answer is to
refuse the prediction or to change the features.

A single model cannot separate the two: with no members there is no
disagreement, and the second part is zero by definition.
