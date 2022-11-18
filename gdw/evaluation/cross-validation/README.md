# Cross validation

Testing on the training data measures memory, not prediction. The module
makes the gap extreme with a model that memorises:

| | |
|---|---:|
| training accuracy | 1.00 |
| cross validated accuracy | 0.40 |

Perfect on what it saw, worse than chance on what it did not.

Splitting into folds and testing each against a model trained on the rest
uses every observation exactly once for testing, and the module checks both
halves of that: the union of the test parts is the whole data, and no fold
overlaps its own training set.

More folds mean more training data per fit and therefore a less variable
estimate, at the cost of more fits. Leaving one out is the extreme of both.
