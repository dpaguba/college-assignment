# Evaluating a return list

## The slide reproduced exactly

For the list `[1,0,1,1,1,0,1,0,0,0,1,1,0,0,1]` with 10 relevant items in the
dataset:

| | |
|---|---:|
| precision | 8/15 ≈ 0.533 |
| recall | 0.800 |
| average precision | (1 + 2/3 + 3/4 + 4/5 + 5/7 + 6/11 + 7/12 + 8/15)/10 = **0.5593** |

which rounds to the 0.56 on the slide. The implementation is also checked
against the area under the step-wise precision-recall curve, computed
independently, over 500 random lists.

## What average precision adds

Precision and recall do not see the order. `[1,1,0,0]` and `[0,0,1,1]` have the
same precision and different average precision, and for a return list the
order is the product.

## The denominator is the dataset

Divided by the number of relevant items in the dataset, not by the length of
the list. A list that puts 8 of 10 relevant items at the front, perfectly
ordered, scores **0.8** and not 1.0. That is deliberate: a short list should
not look good by leaving most of the answer out.

## Fifty per cent overlap of what

The slide sets the relevance threshold at 50 % overlap with the ground truth
and leaves open what the percentage is of. A window containing the whole word
and three times too large covers the ground truth completely:

| reading | value | relevant at 0.5 |
|---|---:|---|
| intersection over union | 0.333 | no |
| intersection over ground truth | 1.000 | yes |

The same detection, the same threshold, opposite verdicts, and a different mAP
at the end. Comparing numbers between two pieces of work requires knowing which
reading each used. The overlap is checked against a pixel count over 400
random box pairs in both readings.
