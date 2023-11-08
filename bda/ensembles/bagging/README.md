# Bagging

Draw bootstrap samples, fit a model to each, average the predictions.

Each sample has the same size and is drawn with replacement, so about a third
of the data is missing from each one: the module measures 0.368 against the
theoretical 1/e = 0.3679. Those left-out rows are what the out-of-bag
estimate uses.

Averaging lowers the variance and leaves the bias alone, which the module
measures separately. That is the whole rule for when bagging helps: an
unstable model such as a deep tree gains, and a stable one such as a linear
fit gains nothing, because there was no variance to average away.
