# View selection

Choose which aggregates to store, under a budget. The greedy rule takes the
view with the largest benefit, where the benefit is how much it lowers the
total query cost given what is already chosen.

The benefit falls as views are added, because the queries a view would have
helped are already cheap. That diminishing return is what makes the greedy
rule reasonable, and it is not enough to make it optimal: the module includes
a case where an exhaustive search over pairs beats it.

The rule also picks the view that is cheapest to use rather than the one that
covers the most, when both answer the same queries. On the example, the view
of size 50 beats the one of size 100 because both answer two queries and the
smaller one answers them for less.
