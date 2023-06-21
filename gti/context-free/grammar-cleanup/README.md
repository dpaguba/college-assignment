# Grammar cleanup

Removing the parts of a grammar that cannot contribute. This is step CNF1 of
the course's normal form algorithm, plus the two removals that come later.

## The order is the content

- **non-generating** first: variables from which no terminal string can be
  derived
- **unreachable** second: variables the start symbol cannot reach

The other order leaves rubbish behind. Deleting a non-generating variable can
make another variable unreachable, so reachability has to be computed on the
already cleaned grammar.

Verified against the marked solution of sheet 5: generating set
`{S, A, B, C, D, G}`, then reachable `{S, A, B, D}`, and the resulting grammar
matches rule for rule.

## Epsilon rules

`remove_epsilon_rules` computes the nullable set and then, for each rule, adds
every variant with some nullable occurrences dropped. That is exponential in
the number of nullable symbols **in one rule**, which in practice is one or
two.

Removing epsilon rules **creates** unit rules: dropping the nullable `B` from
`A -> B C` leaves `A -> C`. That is why unit removal comes after, and not the
other way round.

## Unit rules

The closure `U` of pairs `(A, B)` where A derives B by unit rules alone is
computed first, and then every non-unit rule of B becomes a rule of A. The
course removes newly unreachable variables in the same step, so this ends with
a reachability pass.
