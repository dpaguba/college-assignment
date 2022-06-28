# Tuple calculus

The calculus describes the result instead of the way to it: a query is a
condition on a tuple variable, and the answer is every tuple satisfying it.
The module evaluates such a query directly and checks that it returns what
the corresponding algebra expression returns.

## Safety

`{t | ¬R(t)}` has no finite answer: it depends on which values are assumed to
exist. A query is called safe when its answer is bounded by the values in the
database, and `is_safe` rejects the plain negation for that reason.

The two quantifiers map onto the algebra in a way worth remembering: an
existential quantifier over another relation becomes a join, a universal one
becomes a division. The domain calculus moves the variables from tuples to
attribute values and has the same expressive power, which is the theorem the
lecture builds towards.
