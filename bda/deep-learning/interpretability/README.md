# Interpretability

Permutation importance shuffles one feature and measures the drop in
accuracy. A feature the model relies on costs accuracy when destroyed; an
irrelevant one costs nothing, and the module measures both.

A local surrogate fits a simple model near one point. The black box here is a
threshold on a product, which no straight line describes globally and a line
describes well in a neighbourhood, so the local surrogate agrees far more
often than the global one. That gap is the reason local explanations exist.

## The case the accuracy cannot see

The module builds a data set with a spurious feature that predicts the label
perfectly during training. The model reaches full accuracy and uses only the
spurious feature, and the importance measure says so: the shortcut has all
the importance and the real feature has none.

Accuracy is silent about this. An interpretability method is the only thing
in the pipeline that can say which feature the accuracy came from.
