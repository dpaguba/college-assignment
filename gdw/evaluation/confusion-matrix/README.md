# The confusion matrix

Four counts, and every measure is a ratio of them.

Accuracy is the diagonal over the total, and on an unbalanced problem it is
dominated by the large class. A classifier that predicts the majority class
for a condition affecting one in a hundred reaches:

| | |
|---|---:|
| accuracy | 0.99 |
| recall | 0.00 |

It finds nothing and scores 99 percent. That is the standard argument for
reporting the matrix rather than a single number, and the module builds the
example rather than describing it.
