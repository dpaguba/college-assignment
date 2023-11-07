# Making a deep network trainable

Four problems and the standard answer to each.

**The vanishing gradient.** The derivative of the logistic function is at
most a quarter, so ten layers keep at most one part in a million of the
gradient. A rectifier keeps all of it where it is active, which is why the
change of activation mattered more than any change of architecture.

**Unscaled inputs.** Features on very different scales make the descent
zigzag, and the module counts the steps with and without normalising.

**A learning rate that is too large.** Above the curvature the iteration runs
away rather than converging, which the module shows at a rate of 1.5 and not
at 0.1.

**Overfitting.** Dropout lowers the gap between training and test accuracy,
and early stopping picks the epoch before the validation error turns upward.
Both give up training accuracy for the other kind, which is the same trade as
pruning a tree.
