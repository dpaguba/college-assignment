# Entropy

The eighth sheet derives the entropy from three requirements and then asks
for a concrete case: a fair die and a fair coin, with X their sum.

| value | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| probability | 1/12 | 1/6 | 1/6 | 1/6 | 1/6 | 1/6 | 1/12 |

Only one of the twelve outcomes gives 1 and only one gives 7, which is why
the ends are half as likely. The entropy is **2.7516 bits**, against 2.585
for the die alone.

Adding a fair coin adds one bit of information, and the sum carries only
0.167 of it. The rest is lost because the sum forgets which of the twelve
outcomes occurred: knowing X = 4 leaves two possibilities.

## Information gain

The same quantity applied to a split: the entropy before, minus the weighted
entropy of the parts. A split that separates the classes completely gains one
bit on a balanced binary problem; a split that leaves both parts as mixed as
the whole gains exactly zero. Both are checked, and the second is the case
that stops a decision tree from splitting on a useless attribute.
