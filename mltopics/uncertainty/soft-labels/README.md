# What the majority label throws away

Two images, both labelled deer by the crowd:

| | votes | entropy of the votes |
|---|---|---:|
| clear | deer 48, dog 1, horse 1 | 0.28 |
| contested | deer 33, dog 13, horse 4 | **1.19** |

After aggregation the two are indistinguishable. The disagreement was
collected, paid for, and discarded.

## Which model is better depends on the label

On the contested image, a model that predicts the majority class with 97 %
confidence against one that reproduces the vote distribution:

| | loss against the soft label | loss against the hard label |
|---|---:|---:|
| confident model | **1.448** | **0.030** |
| hedging model | 0.827 | 0.416 |

The ranking reverses. Which model wins is decided entirely by which label was
used to measure, and that choice is rarely treated as a decision.

## Why this matters for uncertainty

Against aggregated labels, an uncertainty estimate can only be checked
indirectly, through its effect: every case is either right or wrong. With the
individual votes there is a measured uncertainty per case to compare against.

That is what makes datasets with preserved votes valuable out of proportion to
their size. The caveat belongs with it: the votes measure the disagreement of
people, which is not the same thing as the noise of the task.
