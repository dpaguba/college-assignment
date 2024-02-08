# Apriori

One property does all the work: a subset of a frequent itemset is frequent.
So a set can only be frequent if all of its subsets are, and candidates whose
subsets are not can be discarded before they are counted.

On the five transactions here with a support threshold of two, the algorithm
counts 8 candidates where the full lattice has 15, and finds the same 7
frequent itemsets that brute force finds. The saving grows with the number of
items, since the lattice grows as a power of two and the candidates do not.

The property has a name and a direction worth keeping straight: support is
**anti-monotone**, falling as an itemset grows, which is what allows the
pruning. A measure that rose with the itemset would allow none.
