# Random forests

Bagging plus a second randomisation: each split may use only a random subset
of the features.

Without it the trees are correlated, because a dominant feature is chosen
first by nearly every tree and the bootstrap samples barely change that. The
module measures how often the trees agree on their first split, with and
without the subsets, and the agreement falls.

That matters because averaging correlated predictions removes less variance
than averaging independent ones. The subsets buy independence at the cost of
each tree being slightly worse, and the average of many decorrelated weak
trees beats the average of a few similar strong ones.

The out-of-bag estimate is the third ingredient: each tree is tested on the
third of the data it never saw, so the forest evaluates itself without a
separate test set, and the module checks the estimate against one.
