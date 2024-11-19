# Decision trees

Recursive binary splits, each chosen to lower the impurity of the labels most.
Both measures are here: the Gini index, which is the chance of mislabelling a
randomly drawn element by guessing from the class distribution, and the
entropy in bits.

## Checking the split

The module tries thresholds at the midpoints between neighbouring values,
because no other threshold produces a different partition. An independent
search over 400 evenly spaced thresholds across each feature's range finds the
same feature and the same gain.

The comparison is on the gain and on the partition, not on the threshold
itself: two thresholds between the same pair of neighbouring values split the
same points while being different numbers. An earlier version of the check
compared the thresholds and quietly copied the answer from the thing it was
supposed to be checking; mutation testing found that.

## What one mislabelled point does

A tree grown to purity has to separate that point too, so it adds cuts that
have nothing to do with the real boundary. On the example data, one flipped
label takes the tree from 6 leaves to 7, and the extra cut distorts the
decision for every point near it. That is why trees are pruned rather than
grown out.

## What a tree gives that a number does not

A path from the root to a leaf is a rule in words: it can be read aloud and
argued with. For the project that connects the two milestones directly, since
a hand-written rule-based AI is a decision tree that was written instead of
learned. The price is that a single tree is weaker than an ensemble.
