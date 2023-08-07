# Learning classifier systems

A rule is a condition over 0, 1 and the wildcard `#`, an action, and a
fitness. Every rule that matches votes for its action with its fitness, so a
set of rules decides rather than a single path, and the rules may contradict
each other. After the outcome, matching rules gain or lose fitness.

## The whole question is the wildcards

A rule without wildcards is a memorised case and helps with no other. A rule
of nothing but wildcards matches everything and says nothing. Generalisation
lies between, and the fitness finds the balance without anybody specifying it.

## Parity has no balance

The module learns whether the number of ones is even. Every bit matters, so
every generalisation is wrong, and the system is forced to find the complete
conditions. Measured: it reaches about 66 % on four bits, and the highest-rated
rules have **no wildcards at all**.

That is the case where a rule-based system meets its limit, and it is the same
case where a shallow decision tree fails and, in the explainability block,
where the decision stump lost 44 points to nearest neighbours.
