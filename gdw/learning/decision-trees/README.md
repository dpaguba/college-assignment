# Decision trees

Choose the attribute with the largest information gain, split, repeat. The
procedure is greedy, so a different first split can produce a smaller tree,
and it stops only when the leaves are pure, so it fits the training data
exactly.

On two hundred noisy rows with ten percent flipped labels:

| | training | test |
|---|---:|---:|
| unlimited depth | 0.99 | 0.81 |
| depth two | 0.92 | 0.84 |

The unlimited tree learns the noise: it reaches 99 percent on the data it saw
and 81 on data it did not. Limiting the depth loses seven points of training
accuracy and gains three of test accuracy, which is the trade pruning makes
and the reason a perfect training score is a warning rather than a result.
