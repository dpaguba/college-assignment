# Cross-validation

The data are split into parts that do not overlap and cover everything, so
each sample is validated exactly once and used for training in every other
round. Checked as a partition for every combination of 2 to 39 samples and 2
to 9 parts.

## The warning on the slide, demonstrated

The lecture says that error rates from validation generally do not carry over
to unseen data. The module shows what that means with data that carry no
signal at all: 120 points of noise with coin-flip labels.

| k | validation error |
|---:|---:|
| 1 | 0.492 |
| 7 | 0.467 |
| 15 | 0.442 |
| **21** | **0.442** |

Choosing the best k gives 0.442, which looks like something. On fresh data
drawn the same way, that same k scores **0.500**, which is what it should be,
because there is nothing to learn.

Nothing went wrong in the procedure. The number 0.442 measures the choice of k
as much as the method, and the choice was made on the same data. A third
untouched set is the only thing that separates the two.

## The base rate

Before any of this: what does guessing give? Always answering the most
frequent category is right as often as that category occurs. Every measured
error rate is held against that number and not against zero.
