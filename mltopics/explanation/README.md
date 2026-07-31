# Explanation and its limits

| Module | Topic |
|---|---|
| [counterfactuals](counterfactuals/) | the nearest different answer |
| [permutation-importance](permutation-importance/) | what shuffling measures |
| [interval-bounds](interval-bounds/) | sound, and how loose |
| [offline-evaluation](offline-evaluation/) | judging a policy from someone else's log |

Four ways of making a claim about a model, and four things each claim does not
cover. The nearest counterfactual changes the one feature that cannot be
changed. Permutation importance splits between two copies of the same feature
until both look worthless. An interval bound at depth eight is 2.7 times wider
than the truth and answers the question it was asked with a shrug. And an
unbiased off-policy estimate has a spread of 0.73 on a quantity of 0.8.
