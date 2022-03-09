# Propositions

Truth tables, and the connective everyone argues with once.

```
p     q     p -> q
F     F       T
F     T       T
T     F       F
T     T       T
```

A false premise makes an implication true whatever the conclusion says. That
is a definition rather than a discovery, and it is the right one because the
alternative would make "every element of the empty set is red" false, which
no proof would survive.

The same asymmetry appears in the quantifiers. A universal statement over an
empty universe is true and an existential one is false, and the two are linked
by negation: the negation of "all are even" is "some is not even", checked
here by evaluating both sides over the same finite universe rather than by
citing the rule.

## Two rules that look alike

| | valid |
|---|---|
| from p and p implies q, conclude q | yes |
| from q and p implies q, conclude p | no |

The second is affirming the consequent, and the truth table refutes it in one
row: p false, q true. Everything the lecture proves about proofs rests on
being able to tell those two apart mechanically, which is what
`is_tautology` does.
