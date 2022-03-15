# Truth vectors and normal forms

A function of `n` variables is a vector of `2^n` bits, and every such vector is
a function. There are `2^(2^n)` of them, so a five-variable function has more
than four billion siblings.

The two canonical forms read the vector from opposite ends. The **disjunctive**
form lists the one-rows as conjunctions, the **conjunctive** form lists the
zero-rows as disjunctions of negated literals. Their sizes are complementary:
for the sheet's function with 10 one-rows out of 32, the DNF has 10 terms and
the CNF has 22 clauses.

Both are unique and both are usually far larger than necessary, which is what
[minimisation](../minimisation/) is for.

## Two properties worth computing

A function is **symmetric** when it depends only on how many inputs are one,
which makes it cheap to build from a counter and is why parity and majority get
special hardware.

A variable the function **does not depend on** costs a wire and nothing else.
Finding those is the first thing any minimiser does, and it is a two-line check
on the vector.
