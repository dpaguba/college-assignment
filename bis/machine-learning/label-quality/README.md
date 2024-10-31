# What bad labels do

The claim on the sheet is that faulty labels make the algorithm learn faulty
relationships. True, but not evenly, and the difference matters more than the
claim.

The experiment: two Gaussian clusters at (−2, 0) and (2, 0), a
nearest-centroid classifier, a fraction of the training labels flipped,
tested on clean data. Four thousand training points.

| Noise | Symmetric | One-sided |
|---:|---:|---:|
| 0 % | 0.977 | 0.976 |
| 10 % | 0.977 | 0.976 |
| 30 % | 0.977 | 0.964 |
| 45 % | 0.977 | 0.952 |
| 50 % | **0.045** | 0.951 |
| 80 % | 0.023 | 0.932 |

## The mechanism

Symmetric noise moves both centroids towards each other by the same amount.
The decision boundary is the midpoint between them, so it does not move at
all: measured at −0.013 with clean labels and −0.011 at 30 % noise. Accuracy
is flat until 45 % and then collapses at exactly 50 %, where the two
centroids coincide and the classifier is a coin toss.

One-sided noise, where only one class is mislabelled, moves one centroid
only. The boundary follows it: −0.22 at 10 % noise, −0.49 at 30 %, −0.77 at
60 %. Accuracy falls from the first percent and keeps falling.

## What this changes

The number to worry about is not how many labels are wrong but whether they
are wrong in one direction. Random error is survivable to a degree that is
genuinely surprising: nearly half the labels can be wrong with no measurable
loss. Systematic error costs from the first case.

So the question to ask about a labelled data set is not "how accurate are the
labellers" but "were they biased towards one class". For the spam filter of
the previous module that is the whole question: people who report aggressively
and people who never report produce very different filters from the same
mail.
